# 导入必要的库和类
from typing import Optional  # 用来导入可选类型
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 从langchain中导入递归字符分割器
from embedchain.chunkers.base_chunker import BaseChunker  # 从embedchain中导入基础的分割器
from embedchain.config.add_config import ChunkerConfig  # 从embedchain中导入配置类
from embedchain.helpers.json_serializable import register_deserializable  # 从embedchain中导入用于序列化的装饰器

# 使用@register_deserializable装饰器，这个类可以被序列化和反序列化
@register_deserializable
class YoutubeVideoChunker(BaseChunker):  # 定义了一个名为YoutubeVideoChunker的类，继承自BaseChunker
    """Chunker for Youtube video."""  # 这个类是用来处理YouTube视频的

    def __init__(self, config: Optional[ChunkerConfig] = None):  # 初始化方法，传入一个可选的配置参数config
        if config is None:  # 如果没有传递配置参数
            config = ChunkerConfig(chunk_size=2000, chunk_overlap=0, length_function=len)  # 创建默认配置，每个块大小为2000字符，块之间没有重叠，长度计算方式是使用内置函数len
        text_splitter = RecursiveCharacterTextSplitter(  # 创建一个文本分割器
            chunk_size=config.chunk_size,  # 分割后的每个块的大小
            chunk_overlap=config.chunk_overlap,  # 块之间的重叠数量
            length_function=config.length_function,  # 计算长度的方式
        )
        super().__init__(text_splitter)  # 调用父类BaseChunker的初始化方法，并传入上面创建的文本分割器

