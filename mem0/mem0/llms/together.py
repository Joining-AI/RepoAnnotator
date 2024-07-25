# 引入了Python的标准库json模块，用于处理JSON数据。
import json

# 引入类型提示相关的模块，帮助理解变量的类型。
from typing import Dict, List, Optional

# 尝试导入together模块，如果找不到这个模块，会告诉用户需要安装额外的依赖包。
try:
    from together import Together
except ImportError:
    # 如果找不到together模块，会抛出错误信息，指导用户如何安装。
    raise ImportError("Together requires extra dependencies. Install with `pip install together`") from None

# 从mem0的llms子目录的base模块中导入LLMBase类，这是一个基础的语言模型类。
from mem0.llms.base import LLMBase

# 从mem0的configs子目录的llms子目录的base模块中导入BaseLlmConfig类，这是配置语言模型的基础类。
from mem0.configs.llms.base import BaseLlmConfig

# 定义了一个名为TogetherLLM的类，继承自LLMBase。
class TogetherLLM(LLMBase):
    # 初始化方法，创建一个TogetherLLM实例时会被调用。
    def __init__(self, config: Optional[BaseLlmConfig] = None):
        # 调用父类的初始化方法。
        super().__init__(config)

        # 如果配置中的model属性没有值，就给它设定一个默认值。
        if not self.config.model:
            self.config.model="mistralai/Mixtral-8x7B-Instruct-v0.1"
        
        # 创建一个Together客户端对象，用于和TogetherAI服务通信。
        self.client = Together()

    # 这个方法用于解析从TogetherAI服务返回的响应。
    def _parse_response(self, response, tools):
        """
        根据是否使用了工具，处理返回的响应。

        参数：
            response: 直接从API得到的原始响应。
            tools: 请求中提供的工具列表。

        返回：
            字符串或字典：处理后的响应。
        """
        # 如果请求中包含了工具...
        if tools:
            # 创建一个空的字典来存放处理后的响应。
            processed_response = {
                "content": response.choices[0].message.content,
                "tool_calls": []
            }
            
            # 如果响应中包含了工具调用的信息...
            if response.choices[0].message.tool_calls:
                # 遍历每个工具调用的信息。
                for tool_call in response.choices[0].message.tool_calls:
                    # 将工具调用的信息添加到processed_response字典中。
                    processed_response["tool_calls"].append({
                        "name": tool_call.function.name,
                        "arguments": json.loads(tool_call.function.arguments)
                    })
            
            # 返回处理后的响应。
            return processed_response
        else:
            # 如果没有使用工具，直接返回响应的内容。
            return response.choices[0].message.content

    # 这个方法用于生成一个基于给定消息的响应。
    def generate_response(
        self,
        messages: List[Dict[str, str]],
        response_format=None,
        tools: Optional[List[Dict]] = None,
        tool_choice: str = "auto",
    ):
        """
        使用TogetherAI生成一个基于给定消息的响应。

        参数：
            messages (list): 包含'role'和'content'的消息字典列表。
            response_format (str or object, optional): 响应格式，默认为"text"。
            tools (list, optional): 可供模型调用的工具列表，默认为None。
            tool_choice (str, optional): 工具选择方式，默认为"auto"。

        返回：
            字符串：生成的响应。
        """
        # 创建一个字典，包含生成响应所需的所有参数。
        params = {
            "model": self.config.model, 
            "messages": messages, 
            "temperature": self.config.temperature, 
            "max_tokens": self.config.max_tokens, 
            "top_p": self.config.top_p
        }
        # 如果指定了响应格式，将其加入到参数字典中。
        if response_format:
            params["response_format"] = response_format
        
        # 如果有工具列表，也加入到参数字典中。
        if tools:
            params["tools"] = tools
            params["tool_choice"] = tool_choice

        # 使用Together客户端发送请求并获取响应。
        response = self.client.chat.completions.create(**params)
        
        # 调用_parse_response方法处理响应，并返回处理后的结果。
        return self._parse_response(response, tools)

