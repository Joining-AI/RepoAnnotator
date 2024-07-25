# 导入一些需要的库和类
from typing import Iterable, Optional, Union

# 导入回调管理器和两个处理标准输出的回调类
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.stdout import StdOutCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import VLLM as BaseVLLM

# 导入自定义配置类和帮助类
from embedchain.config import BaseLlmConfig
from embedchain.helpers.json_serializable import register_deserializable
from embedchain.llm.base import BaseLlm

# 使用装饰器来注册这个类，使其可序列化
@register_deserializable
class VLLM(BaseLlm):  # 定义一个名为 VLLM 的类，它继承自 BaseLlm
    def __init__(self, config: Optional[BaseLlmConfig] = None):  # 构造函数
        super().__init__(config=config)  # 调用父类的构造函数
        if self.config.model is None:  # 如果没有指定模型
            self.config.model = "mosaicml/mpt-7b"  # 设置默认模型

    def get_llm_model_answer(self, prompt):  # 获取答案的方法
        return self._get_answer(prompt=prompt, config=self.config)  # 调用私有方法获取答案

    @staticmethod
    def _get_answer(prompt: str, config: BaseLlmConfig) -> Union[str, Iterable]:  # 私有静态方法，用于获取答案
        callback_manager = [StreamingStdOutCallbackHandler()] if config.stream else [StdOutCallbackHandler()]  # 根据是否启用流式输出选择回调处理器

        # 准备参数以创建 BaseVLLM 实例
        llm_args = {  # 创建一个字典来存储参数
            "model": config.model,  # 模型名称
            "temperature": config.temperature,  # 温度值
            "top_p": config.top_p,  # top_p 参数
            "callback_manager": CallbackManager(callback_manager),  # 回调管理器
        }

        # 如果有额外的模型参数，则添加到参数字典中
        if config.model_kwargs is not None:
            llm_args.update(config.model_kwargs)  # 更新参数字典

        llm = BaseVLLM(**llm_args)  # 创建 BaseVLLM 实例
        return llm.invoke(prompt)  # 使用实例来获取答案并返回

