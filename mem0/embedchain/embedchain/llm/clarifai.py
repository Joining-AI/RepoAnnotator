# 导入日志模块，用于记录程序运行的信息
import logging
# 导入操作系统的模块，可以读取环境变量
import os
# 导入类型提示模块，帮助代码编辑器更好地理解代码
from typing import Optional

# 导入自定义配置类，用于设置模型参数
from embedchain.config import BaseLlmConfig
# 导入序列化帮助类，让类可以被转换成JSON格式
from embedchain.helpers.json_serializable import register_deserializable
# 导入基础的语言模型类，提供通用功能
from embedchain.llm.base import BaseLlm


# 使用装饰器注册这个类，让它可以被序列化
@register_deserializable
# 定义一个继承自BaseLlm的类，专门用于Clarifai语言模型
class ClarifaiLlm(BaseLlm):
    # 初始化函数，创建对象时会自动调用
    def __init__(self, config: Optional[BaseLlmConfig] = None):
        # 调用父类的初始化方法，传入配置参数
        super().__init__(config=config)
        # 检查API密钥是否设置，如果没有抛出错误
        if not self.config.api_key and "CLARIFAI_PAT" not in os.environ:
            raise ValueError("请设置环境变量CLARIFAI_PAT。")

    # 方法：获取模型的回答
    def get_llm_model_answer(self, prompt):
        # 调用私有方法获取回答
        return self._get_answer(prompt=prompt, config=self.config)

    # 静态方法：实际获取回答的逻辑
    @staticmethod
    def _get_answer(prompt: str, config: BaseLlmConfig) -> str:
        # 尝试导入Clarifai的Model类
        try:
            from clarifai.client.model import Model
        # 如果没有安装Clarifai库，抛出错误并告诉用户如何安装
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "缺少Clarifai的依赖库，请使用`pip install clarifai==10.0.1`安装。"
            ) from None

        # 获取模型名称
        model_name = config.model
        # 记录日志，显示正在使用的模型名
        logging.info(f"正在使用clarifai LLM模型: {model_name}")
        # 获取API密钥，优先从配置中获取，否则从环境变量获取
        api_key = config.api_key or os.getenv("CLARIFAI_PAT")
        # 创建模型实例
        model = Model(url=model_name, pat=api_key)
        # 获取模型参数
        params = config.model_kwargs

        # 尝试预测回答
        try:
            # 如果没有设置参数，则使用空字典
            params = {} if config.model_kwargs is None else config.model_kwargs
            # 调用模型的预测方法
            predict_response = model.predict_by_bytes(
                bytes(prompt, "utf-8"),  # 将问题转换为字节流
                input_type="text",  # 设置输入类型为文本
                inference_params=params,  # 设置预测参数
            )
            # 从响应中提取文本答案
            text = predict_response.outputs[0].data.text.raw
            # 返回答案
            return text

        # 如果预测失败，记录错误信息
        except Exception as e:
            logging.error(f"预测失败，异常：{e}")

