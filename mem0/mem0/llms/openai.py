# 导入json模块，用于处理数据格式
import json
# 导入类型提示模块中的Dict、List和Optional类，帮助理解变量类型
from typing import Dict, List, Optional
# 导入OpenAI库中的OpenAI类，用来调用OpenAI API
from openai import OpenAI
# 导入自定义的基础大模型类LLMBase，继承其功能
from mem0.llms.base import LLMBase
# 导入配置基类BaseLlmConfig，用来设置模型参数

# 定义一个名为OpenAILLM的类，继承自LLMBase
class OpenAILLM(LLMBase):
    # 初始化方法，用于创建对象时设定配置
    def __init__(self, config: Optional[BaseLlmConfig] = None):
        # 调用父类的初始化方法
        super().__init__(config)

        # 如果配置中的模型没有设置，则默认使用"gpt-4o"这个模型
        if not self.config.model:
            self.config.model="gpt-4o"
        # 创建一个OpenAI客户端实例，用于与OpenAI API通信
        self.client = OpenAI()
    
    # 定义一个私有方法，用于解析API返回的结果
    def _parse_response(self, response, tools):
        """
        根据是否使用了工具来处理API返回的数据。

        参数：
            response: API返回的原始数据。
            tools: 请求中提供的工具列表。

        返回值：
            字符串或字典：处理后的结果。
        """
        # 如果请求中提供了工具
        if tools:
            # 初始化处理后的响应内容
            processed_response = {
                "content": response.choices[0].message.content,
                "tool_calls": []
            }
            
            # 如果响应中有工具调用的信息
            if response.choices[0].message.tool_calls:
                # 遍历工具调用信息
                for tool_call in response.choices[0].message.tool_calls:
                    # 将每个工具调用的信息添加到处理后的响应中
                    processed_response["tool_calls"].append({
                        "name": tool_call.function.name,
                        "arguments": json.loads(tool_call.function.arguments)
                    })
            
            # 返回处理后的响应
            return processed_response
        else:
            # 如果没有提供工具，直接返回响应的内容部分
            return response.choices[0].message.content

    # 定义一个方法，根据给定的消息生成响应
    def generate_response(
        self,
        messages: List[Dict[str, str]],  # 消息列表，每个消息是一个包含角色和内容的字典
        response_format=None,  # 响应格式，默认为"text"
        tools: Optional[List[Dict]] = None,  # 可选的工具列表，默认为None
        tool_choice: str = "auto",  # 工具选择方式，默认为"auto"
    ):
        """
        使用OpenAI生成响应。

        参数：
            messages (列表): 包含角色和内容的消息列表。
            response_format (字符串或对象, 可选): 响应格式，默认为"text"。
            tools (列表, 可选): 模型可以调用的工具列表，默认为None。
            tool_choice (字符串, 可选): 工具选择方法，默认为"auto"。

        返回值：
            字符串: 生成的响应。
        """
        # 构建请求参数
        params = {
            "model": self.config.model,  # 使用哪个模型
            "messages": messages,  # 提供的消息列表
            "temperature": self.config.temperature,  # 温度参数，控制随机性
            "max_tokens": self.config.max_tokens,  # 最大生成的令牌数
            "top_p": self.config.top_p  # top_p参数，控制多样性和质量
        }
        # 如果指定了响应格式，则加入参数
        if response_format:
            params["response_format"] = response_format
        # 如果指定了工具，则加入参数
        if tools:
            params["tools"] = tools
            params["tool_choice"] = tool_choice

        # 发送请求并获取响应
        response = self.client.chat.completions.create(**params)
        # 解析响应并返回
        return self._parse_response(response, tools)

