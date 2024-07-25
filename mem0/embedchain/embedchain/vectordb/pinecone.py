# 导入日志记录模块
import logging
# 导入获取操作系统信息的模块
import os
# 导入类型提示相关的模块，用于定义函数参数或返回值的数据类型
from typing import Optional, Union

# 尝试导入 pinecone 模块，这个模块是用来连接 Pinecone 数据库的
try:
    import pinecone
# 如果 pinecone 模块没有安装，就会引发 ImportError
except ImportError:
    # 抛出错误信息，告诉用户需要额外安装依赖项才能使用 Pinecone
    raise ImportError(
        "Pinecone 需要额外的依赖项。请通过运行 `pip install pinecone-text pinecone-client` 来安装这些依赖项"
    ) from None

# 导入 BM25 编码器模块，这是一种文本处理技术，用于计算文档的相关性
from pinecone_text.sparse import BM25Encoder

# 导入 Pinecone 数据库配置类
from embedchain.config.vector_db.pinecone import PineconeDBConfig
# 导入一个装饰器，用于注册类为可序列化的，方便在 JSON 格式中保存和读取
from embedchain.helpers.json_serializable import register_deserializable
# 导入一个工具函数，用于将列表切分成多个小列表
from embedchain.utils.misc import chunks
# 导入一个基础向量数据库类，这里是一个抽象基类
from embedchain.vectordb.base import BaseVectorDB

# 初始化一个日志记录器
logger = logging.getLogger(__name__)

# 使用装饰器 @register_deserializable 注册类为可序列化
@register_deserializable

class PineconeDB(BaseVectorDB):

