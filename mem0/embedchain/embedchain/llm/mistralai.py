# 导入操作系统相关的功能，比如获取环境变量。
import os
# 导入一些类型定义，帮助理解变量的数据类型。
from typing import Any, Optional

# 导入配置类，用于设置语言模型的一些参数。
from embedchain.config import BaseLlmConfig
# 导入一个帮助类，让对象可以被序列化成JSON格式。
from embedchain.helpers.json_serializable import register_deserializable
# 导入基类，这是所有语言模型都需要继承的基础类。
from embedchain.llm.base import BaseLlm

# 使用装饰器标记这个类可以被序列化。
@register_deserializable
# 定义一个名为MistralAILlm的类，它继承自BaseLlm。
class MistralAILlm(BaseLlm):
    # 初始化方法，创建这个类的实例时会被调用。
    def __init__(self, config: Optional[BaseLlmConfig] = None):
        # 调用父类的初始化方法，传递配置信息。
        super().__init__(config)
        # 如果没有提供API密钥，而且环境变量中也没有找到密钥，则抛出错误。
        if not self.config.api_key and "MISTRAL_API_KEY" not in os.environ:
            raise ValueError("请设置MISTRAL_API_KEY环境变量或在配置中传入。")

    # 这个方法用来从语言模型获取答案。
    def get_llm_model_answer(self, prompt) -> tuple[str, Optional[dict[str, Any]]]:
        # 如果启用了token计数功能，则计算成本并返回答案和成本信息。
        if self.config.token_usage:
            response, token_info = self._get_answer(prompt, self.config)
            # 指定模型名称。
            model_name = "mistralai/" + self.config.model
            # 如果模型不在定价表中，则抛出错误。
            if model_name not in self.config.model_pricing_map:
                raise ValueError(
                    f"模型 {model_name} 在 `model_prices_and_context_window.json` 中未找到。\
                    您可以通过将 `token_usage` 设置为False来禁用token计数功能。"
                )
            # 计算总成本。
            total_cost = (
                self.config.model_pricing_map[model_name]["input_cost_per_token"] * token_info["prompt_tokens"]
            ) + self.config.model_pricing_map[model_name]["output_cost_per_token"] * token_info["completion_tokens"]
            # 创建一个字典存储token信息和成本。
            response_token_info = {
                "prompt_tokens": token_info["prompt_tokens"],
                "completion_tokens": token_info["completion_tokens"],
                "total_tokens": token_info["prompt_tokens"] + token_info["completion_tokens"],
                "total_cost": round(total_cost, 10),
                "cost_currency": "USD",
            }
            # 返回答案和成本信息。
            return response, response_token_info
        # 如果没有启用token计数功能，则直接返回答案。
        return self._get_answer(prompt, self.config)

    # 静态方法，用于从模型获取答案。
    @staticmethod
    def _get_answer(prompt: str, config: BaseLlmConfig):
        # 尝试导入必要的库。
        try:
            from langchain_core.messages import HumanMessage, SystemMessage
            from langchain_mistralai.chat_models import ChatMistralAI
        # 如果缺少依赖库，则抛出错误提示用户安装。
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "MistralAI所需的依赖项未安装。\
                请通过 `pip install --upgrade \"embedchain[mistralai]\"` 命令安装。"
            ) from None

        # 获取API密钥，优先使用配置中的密钥，否则从环境变量获取。
        api_key = config.api_key or os.getenv("MISTRAL_API_KEY")
        # 创建客户端实例。
        client = ChatMistralAI(mistral_api_key=api_key)
        # 初始化消息列表。
        messages = []
        # 如果有系统提示信息，则添加到消息列表。
        if config.system_prompt:
            messages.append(SystemMessage(content=config.system_prompt))
        # 添加用户的提问。
        messages.append(HumanMessage(content=prompt))
        # 创建参数字典。
        kwargs = {
            "model": config.model or "mistral-tiny",
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            "top_p": config.top_p,
        }

        # TODO: 后续增加支持流式回答的功能。
        # 如果启用流式回答，则分块接收答案。
        if config.stream:
            answer = ""
            for chunk in client.stream(**kwargs, input=messages):
                answer += chunk.content
            return answer
        # 如果不是流式回答，则一次性获取完整答案。
        else:
            chat_response = client.invoke(**kwargs, input=messages)
            # 如果启用了token计数功能，则返回内容和token使用情况。
            if config.token_usage:
                return chat_response.content, chat_response.response_metadata["token_usage"]
            # 如果没有启用token计数功能，则只返回内容。
            return chat_response.content

