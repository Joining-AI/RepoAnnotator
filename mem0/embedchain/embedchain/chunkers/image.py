# 导入需要的模块
from typing import Optional  # 用于指定变量类型，这里表示某个参数可以是None
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 用来把文本分成小块的工具
from embedchain.chunkers.base_chunker import BaseChunker  # 基础的分块器类
from embedchain.config.add_config import ChunkerConfig  # 分块配置类
from embedchain.helpers.json_serializable import register_deserializable  # 注册可序列化的类

# 使用 `register_deserializable` 装饰器来标记 `ImageChunker` 类，这样这个类就可以被序列化和反序列化。
@register_deserializable
class ImageChunker(BaseChunker):  # 定义了一个名为 `ImageChunker` 的类，继承自 `BaseChunker`
    """Chunker for Images."""  # 这个类是用来处理图片的

    def __init__(self, config: Optional[ChunkerConfig] = None):  # 初始化方法，当创建类的新实例时会被调用
        if config is None:  # 如果没有提供配置信息
            config = ChunkerConfig(chunk_size=2000, chunk_overlap=0, length_function=len)  # 使用默认配置
        text_splitter = RecursiveCharacterTextSplitter(  # 创建一个文本分割器对象
            chunk_size=config.chunk_size,  # 设置每个块的大小
            chunk_overlap=config.chunk_overlap,  # 设置块之间的重叠部分
            length_function=config.length_function,  # 设置计算长度的方式
        )
        super().__init__(text_splitter)  # 调用父类的初始化方法，并传入刚才创建的文本分割器对象

