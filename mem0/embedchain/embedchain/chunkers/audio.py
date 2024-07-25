# 首先，我们从typing库导入了一个叫做Optional的东西，它可以帮助我们告诉Python，某个变量可能不会总是有值。
from typing import Optional

# 然后，我们从一个叫langchain的包里拿出了RecursiveCharacterTextSplitter这个工具。这个工具能帮我们将一大段文字切分成小块。
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 接下来，我们从embedchain的chunkers模块中拿出了BaseChunker类，这是所有用来切分东西的类的妈妈。
from embedchain.chunkers.base_chunker import BaseChunker

# 再来，我们从embedchain的config模块里找来了ChunkerConfig这个类，它就像是一个配置文件，告诉我们怎么切分。
from embedchain.config.add_config import ChunkerConfig

# 最后，我们从helpers模块中的json_serializable文件里找到了register_deserializable这个装饰器。这个装饰器可以让我们的类变成可以被JSON读写的形式。
from embedchain.helpers.json_serializable import register_deserializable


# 使用register_deserializable装饰器，我们创建了一个新的类AudioChunker，它继承自BaseChunker，专门用来处理音频文件的切分。
@register_deserializable
class AudioChunker(BaseChunker):
    # 这个类有一个构造函数（就是__init__），当创建AudioChunker类的对象时，会自动调用它。
    def __init__(self, config: Optional[ChunkerConfig] = None):
        # 如果没有传入配置参数config，我们就创建一个新的ChunkerConfig实例，设置默认的切块大小是1000，重叠部分是0，长度计算方式是普通的len()函数。
        if config is None:
            config = ChunkerConfig(chunk_size=1000, chunk_overlap=0, length_function=len)
        
        # 然后，我们用上面得到的config参数，创建一个RecursiveCharacterTextSplitter对象，也就是我们的“切片机”。
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,   # 切块大小
            chunk_overlap=config.chunk_overlap,   # 重叠部分
            length_function=config.length_function,   # 长度计算方式
        )
        
        # 最后，我们通过super()函数调用了父类BaseChunker的构造函数，将刚刚创建的“切片机”text_splitter传进去，这样AudioChunker就有了切分音频的能力。
        super().__init__(text_splitter)

