# 这里我们从typing模块导入了Optional这个类，它帮助我们在定义函数参数时，可以指定参数可以是某种类型或者None。
from typing import Optional

# 导入RecursiveCharacterTextSplitter这个类，它可以帮助我们将一大段文字拆分成小块。
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 导入BaseChunker这个类，我们的PostgresChunker类会继承它，继承的意思就是PostgresChunker将会拥有BaseChunker的所有功能。
from embedchain.chunkers.base_chunker import BaseChunker

# 导入ChunkerConfig这个类，它用来配置如何拆分文本，比如每块文本的大小等。
from embedchain.config.add_config import ChunkerConfig

# 导入register_deserializable这个装饰器，装饰器就像是给函数或类穿上一件特别的衣服，让它们具有额外的功能。
from embedchain.helpers.json_serializable import register_deserializable

# 使用register_deserializable这个装饰器，这样PostgresChunker类就可以被序列化和反序列化，简单说就是可以变成字符串保存起来，也可以从字符串恢复成原来的类。
@register_deserializable
class PostgresChunker(BaseChunker):
    # 这是PostgresChunker类的定义，它是用来处理来自PostgreSQL数据库的数据，将数据切分成更小的部分。
    """Chunker for postgres."""

    # 定义PostgresChunker类的构造函数，当我们创建PostgresChunker的一个实例时，这个函数会被自动调用。
    def __init__(self, config: Optional[ChunkerConfig] = None):
        # 如果没有传入配置信息config，我们就创建一个新的ChunkerConfig实例，设置默认的文本块大小为1000个字符，重叠部分为0个字符。
        if config is None:
            config = ChunkerConfig(chunk_size=1000, chunk_overlap=0, length_function=len)
        
        # 创建一个RecursiveCharacterTextSplitter实例，用来根据配置信息将文本拆分成小块。chunk_size表示每块文本的大小，chunk_overlap表示相邻文本块之间的重叠部分，length_function表示计算文本长度的方式。
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            length_function=config.length_function,
        )
        
        # 调用父类BaseChunker的构造函数，将创建好的text_splitter传入，这样PostgresChunker就有了拆分文本的能力。
        super().__init__(text_splitter)

