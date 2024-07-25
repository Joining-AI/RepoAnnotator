# 导入需要的库和模块
import os
# 导入类型提示，用于帮助理解变量类型
from typing import Optional, Union

# 从chromadb库导入我们需要的类
from chromadb import EmbeddingFunction, Embeddings

# 从embedchain的config模块导入配置类
from embedchain.config import BaseEmbedderConfig
# 从embedchain的embedder模块导入基类
from embedchain.embedder.base import BaseEmbedder
# 从embedchain.models模块导入向量维度模型
from embedchain.models import VectorDimensions

# 定义一个名为MistralAIEmbeddingFunction的新类，它继承自EmbeddingFunction
class MistralAIEmbeddingFunction(EmbeddingFunction):
    # 初始化方法
    def __init__(self, config: BaseEmbedderConfig) -> None:
        # 调用父类的初始化方法
        super().__init__()
        # 尝试从langchain_mistralai库导入MistralAIEmbeddings类
        try:
            from langchain_mistralai import MistralAIEmbeddings
        # 如果没有找到这个库，就抛出错误
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "你需要的MistralAI相关库没有安装。"
                '请使用命令 `pip install --upgrade "embedchain[mistralai]"` 来安装'
            ) from None
        # 保存传入的配置信息
        self.config = config
        # 获取API密钥，如果配置里没有，则尝试从环境变量中获取
        api_key = self.config.api_key or os.getenv("MISTRAL_API_KEY")
        # 使用API密钥创建MistralAIEmbeddings对象
        self.client = MistralAIEmbeddings(mistral_api_key=api_key)
        # 设置模型名称
        self.client.model = self.config.model

    # 这个方法用来计算文本的嵌入向量
    def __call__(self, input: Union[list[str], str]) -> Embeddings:
        # 如果输入是单个字符串，把它变成列表
        if isinstance(input, str):
            input_ = [input]
        # 否则直接使用输入的列表
        else:
            input_ = input
        # 使用客户端计算嵌入向量
        response = self.client.embed_documents(input_)
        # 返回结果
        return response

