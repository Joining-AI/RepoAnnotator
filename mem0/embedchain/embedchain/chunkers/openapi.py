# 导入一些必要的工具。
from typing import Optional
# 导入一个叫做 RecursiveCharacterTextSplitter 的工具，它能帮我们把大段文字拆分成小块。
from langchain.text_splitter import RecursiveCharacterTextSplitter
# 导入自定义的 BaseChunker 类，`OpenAPIChunker` 类会继承这个类的功能。
from embedchain.chunkers.base_chunker import BaseChunker
# 导入 ChunkerConfig 配置类，这个类用来设置如何拆分文本的一些参数。
from embedchain.config.add_config import ChunkerConfig

# 定义一个名为 OpenAPIChunker 的新类，它继承了 BaseChunker 类。
class OpenAPIChunker(BaseChunker):
    # 这是 OpenAPIChunker 类的构造函数（初始化函数），当我们创建这个类的一个实例时就会自动运行这段代码。
    def __init__(self, config: Optional[ChunkerConfig] = None):
        # 如果没有传入配置信息（config 参数），那么就创建一个新的 ChunkerConfig 实例作为默认配置。
        if config is None:
            config = ChunkerConfig(chunk_size=1000, chunk_overlap=0, length_function=len)
        # 创建一个 RecursiveCharacterTextSplitter 实例，用上面得到的配置来告诉它如何拆分文本。
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,  # 每个文本块的大小。
            chunk_overlap=config.chunk_overlap,  # 文本块之间的重叠部分。
            length_function=config.length_function,  # 计算文本长度的方式。
        )
        # 调用父类（BaseChunker）的构造函数，传递给它 RecursiveCharacterTextSplitter 实例。
        super().__init__(text_splitter)

