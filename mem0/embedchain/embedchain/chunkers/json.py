# 引入 "Optional" 类型提示，用于表示函数参数可以接受指定类型的值或者 None。
from typing import Optional

# 引入 "RecursiveCharacterTextSplitter" 类，它能帮助我们按字符递归地分割文本。
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 引入自定义的 "BaseChunker" 类，这个类提供了基础的文本分割功能。
from embedchain.chunkers.base_chunker import BaseChunker

# 引入 "ChunkerConfig" 配置类，用来设置文本分割时的一些参数。
from embedchain.config.add_config import ChunkerConfig

# 引入 "register_deserializable" 装饰器，用于标记类以便后续序列化/反序列化操作。
from embedchain.helpers.json_serializable import register_deserializable

