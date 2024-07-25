# 导入操作系统相关的工具，用于访问环境变量。
import os

# 导入用于处理可迭代对象的抽象基类。
from collections.abc import Iterable

# 导入类型提示，帮助代码更清晰地表明数据类型。
from typing import Any, Optional, Union

# 导入回调管理器和两个具体的回调处理器，用于处理输出。
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.stdout import StdOutCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# 尝试导入NVIDIA AI端点的聊天模型，如果失败则给出错误信息，告诉用户如何安装必要的依赖包。
try:
    from langchain_nvidia_ai_endpoints import ChatNVIDIA
except ImportError:
    # 如果找不到ChatNVIDIA，抛出错误并指示用户如何安装额外的依赖。
    raise ImportError(
        "NVIDIA AI endpoints requires extra dependencies. Install with `pip install langchain-nvidia-ai-endpoints`"
    ) from None

# 导入配置类，用于设置模型参数。
from embedchain.config import BaseLlmConfig

# 导入帮助序列化JSON的装饰器和基础LLM类。
from embedchain.helpers.json_serializable import register_deserializable
from embedchain.llm.base import BaseLlm

# 使用装饰器注册一个可序列化的类。
@register_deserializable
class NvidiaLlm(BaseLlm):
    # 初始化方法，接受一个可选的配置对象。
    def __init__(self, config: Optional[BaseLlmConfig] = None):
        # 调用父类的初始化方法。
        super().__init__(config=config)
        
        # 检查API密钥是否已设置，要么在配置中，要么作为环境变量。
        if not self.config.api_key and "NVIDIA_API_KEY" not in os.environ:
            # 如果未找到API密钥，抛出错误。
            raise ValueError("Please set the NVIDIA_API_KEY environment variable or pass it in the config.")

    # 方法用于获取模型的回答和可能的令牌信息。
    def get_llm_model_answer(self, prompt) -> tuple[str, Optional[dict[str, Any]]]:
        # 如果需要计算令牌使用情况，则进行以下操作。
        if self.config.token_usage:
            # 调用内部方法获取回答和令牌信息。
            response, token_info = self._get_answer(prompt, self.config)
            
            # 设置模型名称。
            model_name = "nvidia/" + self.config.model
            
            # 检查模型价格映射中是否有此模型。
            if model_name not in self.config.model_pricing_map:
                # 如果没有，抛出错误。
                raise ValueError(
                    f"Model {model_name} not found in `model_prices_and_context_window.json`. \
                    You can disable token usage by setting `token_usage` to False."
                )
            
            # 计算总成本。
            total_cost = (
                self.config.model_pricing_map[model_name]["input_cost_per_token"] * token_info["input_tokens"]
            ) + self.config.model_pricing_map[model_name]["output_cost_per_token"] * token_info["output_tokens"]
            
            # 创建一个字典来存储令牌信息和成本。
            response_token_info = {
                "prompt_tokens": token_info["input_tokens"],
                "completion_tokens": token_info["output_tokens"],
                "total_tokens": token_info["input_tokens"] + token_info["output_tokens"],
                "total_cost": round(total_cost, 10),
                "cost_currency": "USD",
            }
            
            # 返回回答和令牌信息。
            return response, response_token_info
        
        # 如果不需要计算令牌使用情况，则直接返回回答。
        return self._get_answer(prompt, self.config)

    # 静态方法，用于获取回答。
    @staticmethod
    def _get_answer(prompt: str, config: BaseLlmConfig) -> Union[str, Iterable]:
        # 根据配置决定使用哪种类型的回调处理器。
        callback_manager = [StreamingStdOutCallbackHandler()] if config.stream else [StdOutCallbackHandler()]
        
        # 准备模型参数。
        model_kwargs = config.model_kwargs or {}
        labels = model_kwargs.get("labels", None)
        
        # 构建请求参数。
        params = {"model": config.model, "nvidia_api_key": config.api_key or os.getenv("NVIDIA_API_KEY")}
        
        # 如果有系统提示，添加到参数中。
        if config.system_prompt:
            params["system_prompt"] = config.system_prompt
        
        # 如果有温度值，添加到参数中。
        if config.temperature:
            params["temperature"] = config.temperature
        
        # 如果有top_p值，添加到参数中。
        if config.top_p:
            params["top_p"] = config.top_p
        
        # 如果有标签，添加到参数中。
        if labels:
            params["labels"] = labels
        
        # 创建一个NVIDIA的聊天模型实例。
        llm = ChatNVIDIA(**params, callback_manager=CallbackManager(callback_manager))
        
        # 调用模型获取回答，如果有标签则传入。
        chat_response = llm.invoke(prompt) if labels is None else llm.invoke(prompt, labels=labels)
        
        # 如果需要计算令牌使用情况，则返回回答内容和令牌使用信息。
        if config.token_usage:
            return chat_response.content, chat_response.response_metadata["token_usage"]
        
        # 否则，只返回回答内容。
        return chat_response.content

