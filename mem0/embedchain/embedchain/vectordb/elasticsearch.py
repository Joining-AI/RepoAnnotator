# 导入日志模块，这可以帮助我们在程序运行时记录信息或错误。
import logging

# 这里导入一些类型提示工具，帮助我们更好地理解和使用变量。
from typing import Any, Optional, Union

# 尝试从 elasticsearch 模块导入 Elasticsearch 类和 bulk 函数，
# 这些是用于和 Elasticsearch 数据库交互的工具。
try:
    from elasticsearch import Elasticsearch
    from elasticsearch.helpers import bulk
except ImportError:
    # 如果没有安装 elasticsearch 相关的库，会在这里抛出错误。
    # 提示用户需要额外安装依赖，告诉他们如何通过 pip 命令安装。
    raise ImportError(
        "要使用 Elasticsearch，你需要安装额外的库。"
        "你可以通过命令 `pip install --upgrade embedchain[elasticsearch]` 来安装。"
    ) from None

# 导入一个配置类，这个类包含了使用 Elasticsearch 数据库的一些设置。
from embedchain.config import ElasticsearchDBConfig

# 导入一个装饰器，它可以帮助类在序列化和反序列化时更加智能。
from embedchain.helpers.json_serializable import register_deserializable

# 导入一个工具函数，用于将数据分割成更小的部分，这在处理大量数据时很有用。
from embedchain.utils.misc import chunks

# 导入一个基类，所有向量数据库的实现都应该继承自这个基类。
from embedchain.vectordb.base import BaseVectorDB

# 创建一个日志记录器，用来记录关于这个模块的信息。
logger = logging.getLogger(__name__)

# 使用装饰器注册一个类，这样这个类就可以被序列化和反序列化了。
@register_deserializable

class ElasticsearchDB(BaseVectorDB):

