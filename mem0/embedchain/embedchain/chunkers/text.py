# 引入一些需要的工具包，让我们的代码可以使用这些工具。
from typing import Optional  # 这个工具帮助我们告诉别人某个变量可能是什么类型，或者可能没有值。
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 这个工具帮我们把一大段文字切成小块。
from embedchain.chunkers.base_chunker import BaseChunker  # 这是我们要继承的基础切片器类。
from embedchain.config.add_config import ChunkerConfig  # 这个配置帮助我们设置切片的大小和重叠部分。
from embedchain.helpers.json_serializable import register_deserializable  # 这个装饰器让我们的类可以被序列化成JSON。

# 使用上面提到的装饰器，这样我们的类就可以被保存成JSON格式了。
@register_deserializable
class TextChunker(BaseChunker):
    """这是一个专门用来处理文本切片的类。"""

    # 这是类的构造函数，当我们创建这个类的一个实例时，它会被调用。
    def __init__(self, config: Optional[ChunkerConfig] = None):
        # 如果用户没有提供配置信息，我们就自己创建一个默认的配置。
        if config is None:
            config = ChunkerConfig(chunk_size=300, chunk_overlap=0, length_function=len)
        # 使用用户的或默认的配置来创建一个文字切片工具。
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,  # 每一块文字的大小。
            chunk_overlap=config.chunk_overlap,  # 文字块之间的重叠部分。
            length_function=config.length_function,  # 计算文字长度的方法。
        )
        # 调用父类的构造函数，传入我们刚刚创建的文字切片工具。
        super().__init__(text_splitter)

