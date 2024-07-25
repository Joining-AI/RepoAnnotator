# 导入并行处理模块中的 futures 工具
import concurrent.futures
# 导入日志模块
import logging
# 导入环境变量模块
import os
# 导入字符串模板工具
from string import Template
# 导入类型定义模块（为了类型提示）
from typing import Optional

# 导入 numpy 库
import numpy as np
# 导入 OpenAI 的 Python 客户端
from openai import OpenAI
# 导入进度条库
from tqdm import tqdm

# 导入自定义配置类
from embedchain.config.evaluation.base import AnswerRelevanceConfig
# 导入自定义基类
from embedchain.evaluation.base import BaseMetric
# 导入自定义评估数据和指标工具
from embedchain.utils.evaluation import EvalData, EvalMetric

# 初始化日志记录器
logger = logging.getLogger(__name__)

# 定义一个类，用于评估答案的相关性
class AnswerRelevance(BaseMetric):
    # 初始化方法
    def __init__(self, config: Optional[AnswerRelevanceConfig] = AnswerRelevanceConfig()):
        # 调用父类的初始化方法
        super().__init__(name=EvalMetric.ANSWER_RELEVANCY.value)
        # 设置配置
        self.config = config
        # 获取 API 密钥，如果配置里没有就从环境变量获取
        api_key = self.config.api_key or os.getenv("OPENAI_API_KEY")
        # 如果密钥为空，则抛出异常
        if not api_key:
            raise ValueError("API key not found. Set 'OPENAI_API_KEY' or pass it in the config.")
        # 使用密钥创建 OpenAI 的客户端对象
        self.client = OpenAI(api_key=api_key)

    # 生成提示信息的方法
    def _generate_prompt(self, data: EvalData) -> str:
        # 根据提供的数据生成提示信息
        return Template(self.config.prompt).substitute(
            num_gen_questions=self.config.num_gen_questions, answer=data.answer
        )

    # 生成问题的方法
    def _generate_questions(self, prompt: str) -> list[str]:
        # 从提示信息中生成问题列表
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[{"role": "user", "content": prompt}],
        )
        # 将生成的问题按行分割返回
        return response.choices[0].message.content.strip().split("\n")

    # 生成问题向量表示的方法
    def _generate_embedding(self, question: str) -> np.ndarray:
        # 生成一个问题的向量表示
        response = self.client.embeddings.create(
            input=question,
            model=self.config.embedder,
        )
        # 返回向量化后的结果
        return np.array(response.data[0].embedding)

    # 计算两个向量之间的余弦相似度的方法
    def _compute_similarity(self, original: np.ndarray, generated: np.ndarray) -> float:
        # 将原始向量调整形状
        original = original.reshape(1, -1)
        # 计算两个向量的模长乘积
        norm = np.linalg.norm(original) * np.linalg.norm(generated, axis=1)
        # 计算点积然后除以模长乘积得到余弦相似度
        return np.dot(generated, original.T).flatten() / norm

    # 计算给定数据的相关性得分的方法
    def _compute_score(self, data: EvalData) -> float:
        # 生成提示信息
        prompt = self._generate_prompt(data)
        # 生成问题
        generated_questions = self._generate_questions(prompt)
        # 生成原始问题的向量表示
        original_embedding = self._generate_embedding(data.question)
        # 生成生成问题的向量表示
        generated_embeddings = np.array([self._generate_embedding(q) for q in generated_questions])
        # 计算相似度
        similarities = self._compute_similarity(original_embedding, generated_embeddings)
        # 返回平均相似度作为得分
        return np.mean(similarities)

    # 评估数据集并返回平均相关性得分的方法
    def evaluate(self, dataset: list[EvalData]) -> float:
        # 创建一个空列表存储结果
        results = []
        
        # 创建线程池执行器
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 为每个数据项创建一个任务并提交到线程池
            future_to_data = {executor.submit(self._compute_score, data): data for data in dataset}
            # 遍历所有已完成的任务
            for future in tqdm(
                concurrent.futures.as_completed(future_to_data), total=len(dataset), desc="Evaluating Answer Relevancy"
            ):
                # 获取当前完成任务对应的数据
                data = future_to_data[future]
                try:
                    # 尝试获取任务的结果并添加到结果列表中
                    results.append(future.result())
                except Exception as e:
                    # 如果出现异常，则记录错误信息
                    logger.error(f"Error evaluating answer relevancy for {data}: {e}")

        # 如果有结果则返回平均得分，否则返回0.0
        return np.mean(results) if results else 0.0

