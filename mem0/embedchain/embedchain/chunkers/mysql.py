# 导入一些需要的模块和类，这些就像是我们画画前准备的颜料盒。
from typing import Optional  # 这个模块帮助我们说明变量可以是某种类型，也可以没有值。
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 这个类能帮我们将一大段文字切分成小块。
from embedchain.chunkers.base_chunker import BaseChunker  # 这是我们要继承的基类，它定义了一些基本的行为。
from embedchain.config.add_config import ChunkerConfig  # 这个类是用来配置如何切分文本的。
from embedchain.helpers.json_serializable import register_deserializable  # 这个装饰器让我们的类能够被序列化成JSON格式。

# 使用上面导入的装饰器，告诉程序这个类可以被转换成JSON格式。
@register_deserializable
class MySQLChunker(BaseChunker):
    """这个类是专门用来处理json数据的切分器。"""

    # 定义类的初始化方法，就像给机器人设定初始状态。
    def __init__(self, config: Optional[ChunkerConfig] = None):
        # 检查传入的配置是否存在，如果不存在，就创建一个新的配置，设置默认的切分大小和重叠量。
        if config is None:
            config = ChunkerConfig(chunk_size=1000, chunk_overlap=0, length_function=len)
        
        # 根据配置创建一个RecursiveCharacterTextSplitter对象，它会根据配置来决定如何切分文本。
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,  # 切分后的每一块有多大。
            chunk_overlap=config.chunk_overlap,  # 块与块之间重叠的部分有多少。
            length_function=config.length_function,  # 计算长度的方式。
        )
        
        # 调用父类的初始化方法，将创建好的text_splitter对象传递过去，这样我们就有了切分文本的能力。
        super().__init__(text_splitter)

