# 导入所需的模块和类
from typing import Optional  # 这行代码导入了Optional类型，用于表示某个变量可以是某种类型或者为None。
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 导入RecursiveCharacterTextSplitter类，它用来将文本分成小块。
from embedchain.chunkers.base_chunker import BaseChunker  # 导入BaseChunker类，这是所有chunker类的基础。
from embedchain.config.add_config import ChunkerConfig  # 导入ChunkerConfig类，它用来配置如何分块。
from embedchain.helpers.json_serializable import register_deserializable  # 导入装饰器，让类支持JSON序列化。

# 使用装饰器注册这个类，以便能够被序列化成JSON
@register_deserializable
class UnstructuredFileChunker(BaseChunker):
    """Chunker for Unstructured file."""  # 这是一个文档字符串，简要说明了这个类的作用：它是用来处理非结构化文件的chunker。
    
    def __init__(self, config: Optional[ChunkerConfig] = None):  # 定义初始化方法，接收一个可选的配置参数config。
        if config is None:  # 如果没有传入配置，则创建一个默认的配置。
            config = ChunkerConfig(chunk_size=1000, chunk_overlap=0, length_function=len)  # 创建默认配置：每个块大小为1000个字符，块之间没有重叠，并且用len函数计算长度。
        text_splitter = RecursiveCharacterTextSplitter(  # 创建一个RecursiveCharacterTextSplitter实例，传入配置信息。
            chunk_size=config.chunk_size,  # 设置块的大小。
            chunk_overlap=config.chunk_overlap,  # 设置块之间的重叠部分。
            length_function=config.length_function,  # 设置长度计算函数。
        )
        super().__init__(text_splitter)  # 调用父类BaseChunker的初始化方法，并传递给它刚刚创建的text_splitter实例。

