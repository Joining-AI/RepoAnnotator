# 导入所需的库和模块
from typing import Optional  # 导入Optional类型提示，用于表示变量可以是某种类型或None
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 导入递归字符文本分割器
from embedchain.chunkers.base_chunker import BaseChunker  # 导入基类BaseChunker
from embedchain.config.add_config import ChunkerConfig  # 导入配置类ChunkerConfig
from embedchain.helpers.json_serializable import register_deserializable  # 导入装饰器，使类支持JSON序列化

# 使用@register_deserializable装饰器，标记这个类可以被JSON序列化
@register_deserializable
class DiscourseChunker(BaseChunker):  # 定义一个名为DiscourseChunker的新类，它继承自BaseChunker
    """Chunker for discourse."""  # 这是一个文档字符串，说明这个类是用来做什么的：对话语进行切分的工具

    def __init__(self, config: Optional[ChunkerConfig] = None):  # 定义构造函数，初始化类的实例
        if config is None:  # 如果没有传入配置参数config
            config = ChunkerConfig(chunk_size=1000, chunk_overlap=0, length_function=len)  # 创建默认配置
        text_splitter = RecursiveCharacterTextSplitter(  # 创建一个递归字符文本分割器对象
            chunk_size=config.chunk_size,  # 设置每个文本块的最大长度
            chunk_overlap=config.chunk_overlap,  # 设置文本块之间的重叠长度
            length_function=config.length_function,  # 设置计算文本长度的方式
        )
        super().__init__(text_splitter)  # 调用父类BaseChunker的构造函数，传入创建好的文本分割器对象

