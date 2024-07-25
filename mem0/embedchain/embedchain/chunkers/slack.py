# 这里我们从typing模块导入了Optional，这是一个帮助我们描述变量类型的东西。
from typing import Optional

# 导入了一个叫RecursiveCharacterTextSplitter的类，这个类是用来把大段文字切分成小块的。
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 导入一个叫做BaseChunker的类，我们的SlackChunker类会继承它，就像是做一个升级版。
from embedchain.chunkers.base_chunker import BaseChunker

# 导入ChunkerConfig类，这个类用来设置如何切分文本的一些规则。
from embedchain.config.add_config import ChunkerConfig

# 这个装饰器（就是有@符号的那行）让SlackChunker类可以被序列化和反序列化，简单来说就是可以把它变成字符串保存，也可以从字符串变回来。
from embedchain.helpers.json_serializable import register_deserializable

# 这是我们的主角，SlackChunker类，它继承自BaseChunker，就像是它的一个特别版本。
@register_deserializable
class SlackChunker(BaseChunker):
    # 这是我们创建SlackChunker对象时会调用的构造函数。
    def __init__(self, config: Optional[ChunkerConfig] = None):
        # 如果没有传入配置信息，我们就自己创建一个默认的配置信息。
        if config is None:
            config = ChunkerConfig(chunk_size=1000, chunk_overlap=0, length_function=len)
        # 现在我们创建一个RecursiveCharacterTextSplitter对象，它会根据我们设定的规则来切分文本。
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,  # 这是每一块文本的大小。
            chunk_overlap=config.chunk_overlap,  # 这是每一块文本之间重叠的部分，这里设为0，意味着没有重叠。
            length_function=config.length_function,  # 这是计算文本长度的方式，我们用的是Python内置的len()函数。
        )
        # 最后，我们调用父类BaseChunker的构造函数，并传入我们刚刚创建的text_splitter对象，这样我们的SlackChunker就有了切分文本的能力。
        super().__init__(text_splitter)

