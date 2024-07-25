# 导入pytest库，这是一个用于编写测试用例的库。
import pytest
# 导入GPT4All模型，这是我们要用来创建聊天机器人的具体模型。
from langchain_community.llms.gpt4all import GPT4All as LangchainGPT4All
# 导入自定义配置类，用于设置聊天机器人的参数。
from embedchain.config import BaseLlmConfig
# 导入我们自己创建的GPT4All聊天机器人类。
from embedchain.llm.gpt4all import GPT4ALLLlm

