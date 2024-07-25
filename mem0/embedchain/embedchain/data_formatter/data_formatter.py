# 从 importlib 这个库中导入 import_module 这个工具。
# 这个工具可以让我们在运行时动态地导入其他模块。
from importlib import import_module

# 从 typing 库里导入 Optional 类型提示。
# Optional 可以用来表示某个变量可能是某种类型，也可能是 None。
from typing import Optional

# 从 embedchain.chunkers 模块下的 base_chunker 文件中导入 BaseChunker 类。
# BaseChunker 是所有文本分块器的基础类。
from embedchain.chunkers.base_chunker import BaseChunker

# 从 embedchain.config 模块中直接导入 AddConfig 类。
# AddConfig 是一个配置类，用于控制添加数据的行为。
from embedchain.config import AddConfig

# 从 embedchain.config.add_config 模块中导入 ChunkerConfig 和 LoaderConfig 类。
# ChunkerConfig 用于配置如何将文档分割成块，
# LoaderConfig 用于配置如何加载数据。
from embedchain.config.add_config import ChunkerConfig, LoaderConfig

# 从 embedchain.helpers.json_serializable 模块中导入 JSONSerializable 类。
# JSONSerializable 是一个帮助类，可以让对象序列化为 JSON 格式，方便存储或传输。
from embedchain.helpers.json_serializable import JSONSerializable

# 从 embedchain.loaders 模块下的 base_loader 文件中导入 BaseLoader 类。
# BaseLoader 是所有数据加载器的基础类。
from embedchain.loaders.base_loader import BaseLoader

# 从 embedchain.models.data_type 模块中导入 DataType 类。
# DataType 定义了支持的数据类型，比如文本、网页等。
from embedchain.models.data_type import DataType

class DataFormatter(JSONSerializable):

