# 导入了处理JSON数据的库
import json
# 导入一些类型提示相关的类，方便理解变量的类型
from typing import Dict, List, Optional

# 尝试从groq这个库导入Groq类
try:
    from groq import Groq
# 如果导入失败，则抛出错误并告诉用户如何安装这个库
except ImportError:
    raise ImportError("Groq requires extra dependencies. Install with `pip install groq`") from None

# 导入基类和配置类
from mem0.llms.base import LLMBase
from mem0.configs.llms.base import BaseLlmConfig


# 定义了一个名为GroqLLM的类，它继承自LLMBase
class GroqLLM(LLMBase):
    # 初始化方法，当创建对象时会被调用
    def __init__(self, config: Optional[BaseLlmConfig] = None):
        # 调用父类的初始化方法
        super().__init__(config)

        # 如果config.model没有值，那么设置默认模型名称
        if not self.config.model:
            self.config.model="llama3-70b-8192"
        # 创建一个Groq客户端实例
        self.client = Groq()

    # 这个方法用来处理从API获取到的响应
    def _parse_response(self, response, tools):
        """
        根据是否使用工具来处理响应内容。
        """
        # 如果有提供工具
        if tools:
            # 创建一个字典来存放处理后的响应
            processed_response = {
                "content": response.choices[0].message.content,
                "tool_calls": []
            }
            
            # 如果响应中有工具调用信息
            if response.choices[0].message.tool_calls:
                # 遍历每个工具调用
                for tool_call in response.choices[0].message.tool_calls:
                    # 把工具调用的信息加入到processed_response中
                    processed_response["tool_calls"].append({
                        "name": tool_call.function.name,
                        "arguments": json.loads(tool_call.function.arguments)
                    })
            
            # 返回处理后的响应
            return processed_response
        else:
            # 如果没有提供工具，直接返回文本内容
            return response.choices[0].message.content

    # 生成响应的方法
    def generate_response(
        self,
        messages: List[Dict[str, str]],  # 消息列表
        response_format=None,  # 响应格式
        tools: Optional[List[Dict]] = None,  # 可选的工具列表
        tool_choice: str = "auto",  # 工具选择方式
    ):
        """
        使用Groq生成响应。
        """
        # 创建一个参数字典
        params = {
            "model": self.config.model,  # 模型名称
            "messages": messages,  # 消息列表
            "temperature": self.config.temperature,  # 温度参数
            "max_tokens": self.config.max_tokens,  # 最大token数量
            "top_p": self.config.top_p  # top_p参数
        }
        # 如果指定了响应格式，则添加到参数字典中
        if response_format:
            params["response_format"] = response_format
        # 如果提供了工具列表，则添加到参数字典中
        if tools:
            params["tools"] = tools
            params["tool_choice"] = tool_choice

        # 使用Groq客户端发送请求并获取响应
        response = self.client.chat.completions.create(**params)
        # 处理响应并返回
        return self._parse_response(response, tools)

