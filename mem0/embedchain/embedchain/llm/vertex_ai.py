# 导入一些我们需要的库和模块
import importlib
import logging
from typing import Any, Optional

# 导入用于处理实时输出的回调处理器
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# 导入与Google Vertex AI聊天相关的类
from langchain_google_vertexai import ChatVertexAI

# 导入自定义配置类
from embedchain.config import BaseLlmConfig
# 导入帮助序列化JSON的装饰器
from embedchain.helpers.json_serializable import register_deserializable
# 导入基语言模型类
from embedchain.llm.base import BaseLlm

# 初始化日志记录器
logger = logging.getLogger(__name__)

