# 导入一些类型定义，这些类型定义帮助理解变量可以是哪些类型。
from typing import Any, Dict, List, Optional, Union

# 导入 pyarrow 库，这是一个用来处理数据的库。
import pyarrow as pa

# 尝试导入 lancedb 这个库。
try:
    import lancedb
# 如果 lancedb 没有安装，就告诉用户需要安装它，并给出安装命令。
except ImportError:
    raise ImportError('LanceDB is required. Install with pip install "embedchain[lancedb]"') from None

# 导入 LanceDBConfig 类，这个类是用来配置 LanceDB 数据库的。
from embedchain.config.vector_db.lancedb import LanceDBConfig
# 导入 json_serializable 模块里的 register_deserializable 装饰器，
# 这个装饰器让某些类可以更容易地被转换成 JSON 格式。
from embedchain.helpers.json_serializable import register_deserializable
# 导入 BaseVectorDB 类，这是所有向量数据库类的基础。
from embedchain.vectordb.base import BaseVectorDB

# 使用 register_deserializable 装饰器，标记下面的类可以被转换成 JSON。
@register_deserializable

class LanceDB(BaseVectorDB):

