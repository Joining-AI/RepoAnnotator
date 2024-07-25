# 导入必要的库和类
from typing import Optional  # 导入Optional类型，用于表示某些参数可以为空
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 导入RecursiveCharacterTextSplitter类，用于分隔文本
from embedchain.chunkers.base_chunker import BaseChunker  # 导入BaseChunker基类，所有chunker类都继承自这个基类
from embedchain.config.add_config import ChunkerConfig  # 导入ChunkerConfig配置类，用于设置chunker的参数
from embedchain.helpers.json_serializable import register_deserializable  # 导入register_deserializable装饰器，用于注册类以便序列化

# 使用@register_deserializable装饰器来标记RSSFeedChunker类，这样这个类就可以被序列化了
@register_deserializable
class RSSFeedChunker(BaseChunker):  # 定义RSSFeedChunker类，它继承自BaseChunker
    """Chunker for RSS Feed."""  # 这是一个注释，说明这个类是用于处理RSS Feed的

    def __init__(self, config: Optional[ChunkerConfig] = None):  # 定义初始化方法，接受一个可选的配置参数config
        if config is None:  # 如果没有提供配置参数config
            config = ChunkerConfig(chunk_size=2000, chunk_overlap=0, length_function=len)  # 创建一个默认的配置，将文本分成最大2000个字符的小段，且各段之间没有重叠
        text_splitter = RecursiveCharacterTextSplitter(  # 创建一个RecursiveCharacterTextSplitter对象，用于实际的文本分隔
            chunk_size=config.chunk_size,  # 设置每个小段的最大长度
            chunk_overlap=config.chunk_overlap,  # 设置各段之间的重叠长度
            length_function=config.length_function,  # 设置计算长度的方式
        )
        super().__init__(text_splitter)  # 调用父类BaseChunker的初始化方法，并传入创建的RecursiveCharacterTextSplitter对象

