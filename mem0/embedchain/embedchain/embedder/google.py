# 引入需要的类型定义，用于代码提示和检查。
from typing import Optional, Union

# 导入Google的人工智能模块，它包含了生成文本嵌入的方法。
import google.generativeai as genai

# 导入ChromaDB库中用于创建嵌入函数的部分。
from chromadb import EmbeddingFunction, Embeddings

# 导入我们自定义的配置类，用于设置Google AI嵌入器的参数。
from embedchain.config.embedder.google import GoogleAIEmbedderConfig

# 导入我们自定义的基础嵌入器类，用于提供基本的嵌入功能。
from embedchain.embedder.base import BaseEmbedder

# 导入我们定义的向量维度模型，用于指定向量的大小。
from embedchain.models import VectorDimensions

