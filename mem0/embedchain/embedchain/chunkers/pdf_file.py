# 这里我们从typing模块导入了Optional这个工具，它帮助我们在定义函数参数时可以指定参数可选。
from typing import Optional

# 导入RecursiveCharacterTextSplitter类，这是一个用于将大文本分割成小块的工具。
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 导入BaseChunker类，这是处理文件并将其拆分成更小部分的基本框架。
from embedchain.chunkers.base_chunker import BaseChunker

# 导入ChunkerConfig类，这用来配置如何拆分文件，比如每块的大小和重叠的部分。
from embedchain.config.add_config import ChunkerConfig

# 导入一个工具，用于帮助我们的类能够在某些情况下自动转换为JSON格式，方便存储和传输。
from embedchain.helpers.json_serializable import register_deserializable

# 使用register_deserializable装饰器，告诉系统PdfFileChunker这个类可以被序列化成JSON。
@register_deserializable

# 定义PdfFileChunker类，继承自BaseChunker，专门用于处理PDF文件。
class PdfFileChunker(BaseChunker):
    # 这是PdfFileChunker类的构造函数，当我们创建这个类的一个实例时，会自动调用它。
    def __init__(self, config: Optional[ChunkerConfig] = None):
        # 检查传入的config参数是否为None，如果是，则创建一个新的ChunkerConfig实例。
        if config is None:
            # 创建ChunkerConfig实例，设置每块的大小为1000个字符，没有重叠，并使用len函数计算长度。
            config = ChunkerConfig(chunk_size=1000, chunk_overlap=0, length_function=len)
        
        # 使用前面的配置信息创建RecursiveCharacterTextSplitter实例，它将根据配置来分割文本。
        text_splitter = RecursiveCharacterTextSplitter(
            # 设置每块的大小、重叠的部分以及长度计算方式。
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            length_function=config.length_function,
        )
        
        # 调用父类BaseChunker的构造函数，传入我们刚刚创建的text_splitter实例。
        super().__init__(text_splitter)

