# 引入日志记录模块，用于打印信息或错误
import logging

# 引入一些处理数据集合的工具
from collections.abc import Iterable

# 引入类型提示相关的模块，帮助理解变量的类型
from typing import Optional, Union

# 引入与LangChain框架相关的回调管理器和处理器，用于控制模型的输出行为
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.stdout import StdOutCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# 引入Ollama模型的封装，便于使用
from langchain_community.llms.ollama import Ollama

# 尝试引入Ollama客户端，如果失败则提示用户安装必要的依赖包
try:
    from ollama import Client
except ImportError:
    # 如果没有找到ollama模块，告诉用户如何安装
    raise ImportError("Ollama 需要额外的依赖。请用 `pip install ollama` 安装") from None

# 引入配置类和可序列化帮助类，用于设置模型参数和数据交换
from embedchain.config import BaseLlmConfig
from embedchain.helpers.json_serializable import register_deserializable
from embedchain.llm.base import BaseLlm

# 创建日志记录器，用于记录程序运行过程中的信息
logger = logging.getLogger(__name__)

# 使用装饰器注册可序列化的类，以便于数据交换
@register_deserializable
class OllamaLlm(BaseLlm):
    # 初始化方法，当创建OllamaLlm对象时会被调用
    def __init__(self, config: Optional[BaseLlmConfig] = None):
        # 调用父类的初始化方法，传递配置信息
        super().__init__(config=config)
        
        # 如果没有指定模型，默认使用 "llama2"
        if self.config.model is None:
            self.config.model = "llama2"

        # 创建Ollama客户端，连接到指定的服务器地址
        client = Client(host=config.base_url)
        
        # 获取本地已有的模型列表
        local_models = client.list()["models"]
        
        # 检查模型是否已经存在于本地，如果没有则从Ollama拉取
        if not any(model.get("name") == self.config.model for model in local_models):
            logger.info(f"正在从 Ollama 拉取 {self.config.model} 模型！")
            client.pull(self.config.model)

    # 提供一个接口，用于获取模型对某个问题的回答
    def get_llm_model_answer(self, prompt):
        # 调用私有方法获取回答
        return self._get_answer(prompt=prompt, config=self.config)

    # 静态方法，用于实际生成回答
    @staticmethod
    def _get_answer(prompt: str, config: BaseLlmConfig) -> Union[str, Iterable]:
        # 根据配置决定是否启用流式输出
        if config.stream:
            # 流式输出时使用的回调处理器
            callbacks = config.callbacks if config.callbacks else [StreamingStdOutCallbackHandler()]
        else:
            # 非流式输出时使用的回调处理器
            callbacks = [StdOutCallbackHandler()]

        # 创建Ollama模型实例，传入各种配置参数
        llm = Ollama(
            model=config.model,
            system=config.system_prompt,
            temperature=config.temperature,
            top_p=config.top_p,
            callback_manager=CallbackManager(callbacks),
            base_url=config.base_url,
        )
        
        # 使用模型处理问题，返回答案
        return llm.invoke(prompt)

