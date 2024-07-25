# 这里导入了一个叫做Optional的东西，它来自typing这个包。Optional可以让我们在定义变量时说：“这个变量可以是某种类型，也可以什么都不放（也就是None）”。
from typing import Optional

# 导入RecursiveCharacterTextSplitter，这是一个帮助我们把大段文字切成小块的工具，来自langchain.text_splitter这个包。
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 导入BaseChunker，这是个基础的切分器类，我们后面会继承它来创建自己的切分器。
from embedchain.chunkers.base_chunker import BaseChunker

# 导入ChunkerConfig，这是配置切分器的一些选项，比如每块文本的大小等。
from embedchain.config.add_config import ChunkerConfig

# 导入register_deserializable，这像是一个标签，让我们能更容易地保存和读取类的信息。
from embedchain.helpers.json_serializable import register_deserializable

# 使用上面的标签装饰GoogleDriveChunker这个类，这样它就可以被更方便地保存和读取了。
@register_deserializable
class GoogleDriveChunker(BaseChunker):
    # 这个类是用来处理谷歌云端硬盘文件夹里的内容的，把它切成小块。
    """Chunker for google drive folder."""

    # 定义类的构造函数，当我们创建GoogleDriveChunker的实例时，会自动运行这个函数。
    def __init__(self, config: Optional[ChunkerConfig] = None):
        # 如果没有传入配置，就自己创建一个默认的配置，每块文本有1000个字符，块之间没有重叠，计算长度的方式就是直接数字符数量。
        if config is None:
            config = ChunkerConfig(chunk_size=1000, chunk_overlap=0, length_function=len)

        # 创建一个RecursiveCharacterTextSplitter实例，用上面的配置来设置它如何切分文本。
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            length_function=config.length_function,
        )

        # 调用父类BaseChunker的构造函数，传入我们刚刚创建的text_splitter，这样我们的GoogleDriveChunker就能开始工作了。
        super().__init__(text_splitter)

