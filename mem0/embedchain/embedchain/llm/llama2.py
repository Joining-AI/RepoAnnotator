# 这里导入了一些需要的工具包
import importlib
import os
from typing import Optional

# 导入了Replicate模型，这个模型是用于语言生成的
from langchain_community.llms.replicate import Replicate

# 这里导入了自定义配置文件的类
from embedchain.config import BaseLlmConfig

# 导入了一个帮助类，用于处理json格式的数据
from embedchain.helpers.json_serializable import register_deserializable

# 这是基类，所有语言模型都会继承它
from embedchain.llm.base import BaseLlm

# 这个装饰器告诉系统，这个类可以被反序列化成json格式
@register_deserializable

# 定义了一个新的类，叫做Llama2Llm，它是基于BaseLlm的
class Llama2Llm(BaseLlm):

    # 这是构造函数，当创建一个Llama2Llm对象时会被调用
    def __init__(self, config: Optional[BaseLlmConfig] = None):

        # 尝试导入Replicate模块，如果找不到会抛出错误
        try:
            importlib.import_module("replicate")
        except ModuleNotFoundError:

            # 如果没有找到Replicate模块，这里会告诉用户如何安装所需的依赖
            raise ModuleNotFoundError(
                "缺少Llama2所需的库。请用`pip install --upgrade 'embedchain[llama2]'`命令来安装"
            ) from None

        # 如果没有传入配置信息，就创建一个新的BaseLlmConfig实例作为默认配置
        if not config:
            config = BaseLlmConfig()

            # 设置默认的配置值，比如最大生成的令牌数量和温度（控制随机性）
            config.max_tokens = 500
            config.temperature = 0.75

        # 如果模型名称没有设置，给它一个默认值
        if not config.model:
            config.model = (
                "a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5"
            )

        # 调用父类的构造函数，传递配置信息
        super().__init__(config=config)

        # 检查API密钥是否设置，如果没有设置，会抛出错误
        if not self.config.api_key and "REPLICATE_API_TOKEN" not in os.environ:
            raise ValueError("请设置REPLICATE_API_TOKEN环境变量或在配置中提供它。")

    # 这个方法用于获取模型的回答
    def get_llm_model_answer(self, prompt):

        # 如果系统提示语被设置了，这里会抛出错误，因为Llama2不支持这个功能
        if self.config.system_prompt:
            raise ValueError("Llama2不支持`system_prompt`")

        # 获取API密钥，优先从配置中取，如果没有则从环境变量中取
        api_key = self.config.api_key or os.getenv("REPLICATE_API_TOKEN")

        # 创建一个Replicate实例，传入模型、API密钥和一些输入参数
        llm = Replicate(
            model=self.config.model,
            replicate_api_token=api_key,
            input={
                "temperature": self.config.temperature,
                "max_length": self.config.max_tokens,
                "top_p": self.config.top_p,
            },
        )

        # 调用模型，传入提示语，返回模型的响应
        return llm.invoke(prompt)

