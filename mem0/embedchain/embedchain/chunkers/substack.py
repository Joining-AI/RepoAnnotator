# 导入必要的库和模块
from typing import Optional  # 导入 Optional 类型提示，用于表示某个变量可以是某种类型或 None。
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 导入 RecursiveCharacterTextSplitter 类，用于分割文本。
from embedchain.chunkers.base_chunker import BaseChunker  # 导入基类 BaseChunker。
from embedchain.config.add_config import ChunkerConfig  # 导入配置类 ChunkerConfig，用来设置分割文本时的一些参数。
from embedchain.helpers.json_serializable import register_deserializable  # 导入装饰器，让这个类支持 JSON 序列化。

# 使用 @register_deserializable 装饰器来标记这个类，意味着这个类可以被转换成 JSON 格式保存。
@register_deserializable
class SubstackChunker(BaseChunker):
    """Chunker for Substack."""
    # 这个类是用来专门处理 Substack 平台的文章内容的，它会把文章分成若干个小段落。

    def __init__(self, config: Optional[ChunkerConfig] = None):
        # 初始化函数，当创建 SubstackChunker 的对象时会被调用。
        if config is None:
            # 如果在创建对象的时候没有提供配置信息，那么就使用默认配置。
            config = ChunkerConfig(chunk_size=1000, chunk_overlap=0, length_function=len)
            # 设置默认配置：每个文本块大小为 1000 个字符，块之间没有重叠，计算长度的方式就是数字符数量。

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            # 设置每个文本块的大小。
            chunk_overlap=config.chunk_overlap,
            # 设置文本块之间的重叠部分有多少字符。
            length_function=config.length_function,
            # 设置如何计算文本长度的方法。
        )
        # 创建 RecursiveCharacterTextSplitter 对象，这个对象负责实际的文本分割工作。

        super().__init__(text_splitter)
        # 调用父类 BaseChunker 的初始化方法，并传入刚刚创建的 RecursiveCharacterTextSplitter 对象。
        # 这样就把具体的文本分割逻辑传递给了父类处理。

