# 导入需要的模块，让程序知道如何处理类型提示
from typing import Optional

# 导入一个可以将文本按照字符递归分割的工具
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 导入自定义的基类Chunker，它用于处理数据块
from embedchain.chunkers.base_chunker import BaseChunker

# 导入配置类，用于设置如何分割数据块
from embedchain.config.add_config import ChunkerConfig

# 导入一个帮助器，使类可以被序列化成JSON格式
from embedchain.helpers.json_serializable import register_deserializable

# 使用装饰器注册这个类，让它可以被序列化
@register_deserializable

# 定义一个类，专门用来处理Excel文件的数据分割
class ExcelFileChunker(BaseChunker):
    # 这个类的构造函数，初始化时可以传入配置参数
    def __init__(self, config: Optional[ChunkerConfig] = None):
        # 如果没有传入配置参数，就创建一个新的配置，设置每块数据的大小为1000个字符，没有重叠
        if config is None:
            config = ChunkerConfig(chunk_size=1000, chunk_overlap=0, length_function=len)
        
        # 创建一个文本分割器对象，使用之前设定的配置参数
        text_splitter = RecursiveCharacterTextSplitter(
            # 设置每块数据的大小
            chunk_size=config.chunk_size,
            # 设置块之间的重叠部分，这里是不重叠
            chunk_overlap=config.chunk_overlap,
            # 设置如何计算长度的方法，这里用的是内置的len函数
            length_function=config.length_function,
        )
        
        # 调用父类的构造函数，传入我们创建的文本分割器对象
        super().__init__(text_splitter)

