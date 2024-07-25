# 导入一些必要的库
import importlib
import os
from typing import Any, Optional

# 尝试导入 `langchain_together` 这个库
try:
    from langchain_together import ChatTogether
# 如果导入失败，告诉用户需要安装这个库
except ImportError:
    raise ImportError(
        "请通过运行 `pip install langchain_together==0.1.3` 来安装 `langchain_together` 包."
    )

# 导入其他需要的配置类和工具
from embedchain.config import BaseLlmConfig
from embedchain.helpers.json_serializable import register_deserializable
from embedchain.llm.base import BaseLlm

# 使用装饰器注册一个可反序列化的类
@register_deserializable
# 定义了一个名为 `TogetherLlm` 的类，继承自 `BaseLlm`
class TogetherLlm(BaseLlm):
    # 初始化方法
    def __init__(self, config: Optional[BaseLlmConfig] = None):
        # 尝试导入 `together` 这个库
        try:
            importlib.import_module("together")
        # 如果找不到该库，告诉用户怎么安装
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "使用 Together 所需的依赖没有安装."
                '请通过 `pip install --upgrade "embedchain[together]"` 来安装.'
            ) from None
        
        # 调用父类的初始化方法
        super().__init__(config=config)
        
        # 检查 `TOGETHER_API_KEY` 是否已经设置
        if not self.config.api_key and "TOGETHER_API_KEY" not in os.environ:
            raise ValueError("请设置 `TOGETHER_API_KEY` 环境变量或在配置中提供它.")

    # 用于获取模型回答的方法
    def get_llm_model_answer(self, prompt) -> tuple[str, Optional[dict[str, Any]]]:
        # 如果设置了系统提示（这里不支持）
        if self.config.system_prompt:
            raise ValueError("TogetherLlm 不支持 `system_prompt`")
        
        # 如果启用了令牌计数功能
        if self.config.token_usage:
            # 获取回答和令牌信息
            response, token_info = self._get_answer(prompt, self.config)
            
            # 设置模型名称
            model_name = "together/" + self.config.model
            
            # 检查模型是否在价格映射中
            if model_name not in self.config.model_pricing_map:
                raise ValueError(
                    f"模型 {model_name} 在 `model_prices_and_context_window.json` 中未找到. \
                    可以通过将 `token_usage` 设为 False 来禁用令牌计数."
                )
            
            # 计算总成本
            total_cost = (
                self.config.model_pricing_map[model_name]["input_cost_per_token"] * token_info["prompt_tokens"]
            ) + self.config.model_pricing_map[model_name]["output_cost_per_token"] * token_info["completion_tokens"]
            
            # 创建令牌信息字典
            response_token_info = {
                "prompt_tokens": token_info["prompt_tokens"],
                "completion_tokens": token_info["completion_tokens"],
                "total_tokens": token_info["prompt_tokens"] + token_info["completion_tokens"],
                "total_cost": round(total_cost, 10),
                "cost_currency": "USD",
            }
            
            # 返回回答和令牌信息
            return response, response_token_info
        # 如果没有启用令牌计数功能
        return self._get_answer(prompt, self.config)

    # 静态方法，用于获取回答
    @staticmethod
    def _get_answer(prompt: str, config: BaseLlmConfig) -> str:
        # 获取 API 密钥
        api_key = config.api_key or os.environ["TOGETHER_API_KEY"]
        
        # 设置参数
        kwargs = {
            "model_name": config.model or "mixtral-8x7b-32768",
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            "together_api_key": api_key,
        }
        
        # 创建 `ChatTogether` 实例
        chat = ChatTogether(**kwargs)
        
        # 发送请求并获取响应
        chat_response = chat.invoke(prompt)
        
        # 如果启用了令牌计数功能
        if config.token_usage:
            # 返回内容和令牌使用情况
            return chat_response.content, chat_response.response_metadata["token_usage"]
        # 如果没有启用令牌计数功能
        return chat_response.content

