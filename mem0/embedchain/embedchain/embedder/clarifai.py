# 导入需要的操作系统相关功能，比如获取环境变量。
import os
# 从typing模块导入Optional和Union，用于类型提示，让代码更容易理解。
from typing import Optional, Union

# 从embedchain.config模块导入BaseEmbedderConfig类，这是配置类的基础。
from embedchain.config import BaseEmbedderConfig
# 从embedchain.embedder.base模块导入BaseEmbedder类，这是嵌入器（一种转换文本到向量的方法）的基础类。
from embedchain.embedder.base import BaseEmbedder

# 从chromadb模块导入EmbeddingFunction和Embeddings，它们是用于定义和操作嵌入向量的。
from chromadb import EmbeddingFunction, Embeddings

