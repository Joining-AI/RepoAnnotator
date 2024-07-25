# 导入必要的模块，这些模块就像是工具箱里的工具，帮助我们完成任务。
from typing import Optional
# 导入RecursiveCharacterTextSplitter类，这个类可以帮助我们将一大段文字分成许多小段。
from langchain.text_splitter import RecursiveCharacterTextSplitter
# 导入BaseChunker类，这是所有用于分块的类的基础。
from embedchain.chunkers.base_chunker import BaseChunker
# 导入ChunkerConfig类，这个类用来配置分块时的一些参数，比如每一块的大小。
from embedchain.config.add_config import ChunkerConfig
# 导入注册功能，让我们可以将类的信息保存起来，以便之后使用。
from embedchain.helpers.json_serializable import register_deserializable

# 使用装饰器（一种特殊的语法糖）来标记WebPageChunker类，这样我们就可以轻松地保存和读取这个类的信息了。
@register_deserializable
class WebPageChunker(BaseChunker):
    # 这是我们定义的一个新类，它继承自BaseChunker，专门用来处理网页内容。
    """Chunker for web page."""
    
    # 定义类的构造函数，当我们创建这个类的对象时，会自动运行这部分代码。
    def __init__(self, config: Optional[ChunkerConfig] = None):
        # 检查传入的配置参数config是否为空，如果为空，则使用默认配置。
        if config is None:
            # 创建一个默认的配置对象，设置每一块的最大长度为2000个字符，相邻块之间的重叠为0个字符。
            config = ChunkerConfig(chunk_size=2000, chunk_overlap=0, length_function=len)
        # 根据配置创建一个RecursiveCharacterTextSplitter对象，这个对象将帮助我们分块。
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            length_function=config.length_function,
        )
        # 调用父类的构造函数，传入我们刚刚创建的RecursiveCharacterTextSplitter对象。
        super().__init__(text_splitter)

