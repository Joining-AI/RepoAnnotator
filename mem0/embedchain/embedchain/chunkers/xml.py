# 引入需要的模块，这些就像是工具箱里的工具，帮助我们完成任务。
from typing import Optional

# 导入一个叫做RecursiveCharacterTextSplitter的类，它能帮助我们把一大段文字分成小块。
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 这是从embedchain项目里导入的BaseChunker类，它是处理文件的基础框架。
from embedchain.chunkers.base_chunker import BaseChunker

# 再从embedchain的config模块中导入ChunkerConfig类，这个类用来设置分块的大小和重叠的部分。
from embedchain.config.add_config import ChunkerConfig

# 导入一个帮助类，可以让我们的类在程序中更容易被识别和使用。
from embedchain.helpers.json_serializable import register_deserializable

# 使用装饰器@register_deserializable标记XmlChunker类，这样它就能被系统更好地管理和使用了。
@register_deserializable

# 定义一个名为XmlChunker的类，它是BaseChunker的子类，专门用来处理XML文件。
class XmlChunker(BaseChunker):

    # 这是XmlChunker类的构造函数，当我们创建这个类的一个实例时，就会自动运行这里。
    def __init__(self, config: Optional[ChunkerConfig] = None):
        
        # 如果没有传入配置信息（config），我们就自己创建一个默认的配置。
        if config is None:
            config = ChunkerConfig(chunk_size=500, chunk_overlap=50, length_function=len)
        
        # 创建一个RecursiveCharacterTextSplitter对象，用上面的配置来告诉它如何分割文本。
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,  # 每个块的大小是多少字符
            chunk_overlap=config.chunk_overlap,  # 块与块之间重叠多少字符
            length_function=config.length_function,  # 计算长度的方法
        )
        
        # 最后，调用父类BaseChunker的构造函数，把刚才创建的text_splitter对象传进去。
        super().__init__(text_splitter)

