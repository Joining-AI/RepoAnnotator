# 这一行是在导入一些我们需要的工具包，这些工具包可以帮助我们处理不同类型的数据。
from typing import Optional

# 下面这一行是从一个叫做langchain的库中，导入了一个叫RecursiveCharacterTextSplitter的类，
# 它可以帮我们将一大段文字分割成许多小段。
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 这里从我们自己的程序中导入了两个类，BaseChunker和ChunkerConfig，
# 它们是用来配置和处理文本块的大小和重叠的。
from embedchain.chunkers.base_chunker import BaseChunker
from embedchain.config.add_config import ChunkerConfig

# 这个导入的函数是帮助我们的类能够被序列化，也就是说，可以把这个类的对象转换成字符串保存，
# 或者从字符串中读取出来，这样就可以在不同地方共享数据了。
from embedchain.helpers.json_serializable import register_deserializable

# 这个装饰器（@register_deserializable）的作用就是告诉我们的程序，
# 我们即将定义的BeehiivChunker类是可以被序列化的。
@register_deserializable

# 这里我们定义了一个新的类，叫做BeehiivChunker，它是用来处理一种叫做Beehiiv的内容的。
# 这个类继承自BaseChunker，意味着它有BaseChunker的所有功能，但可以做一些特别的定制。
class BeehiivChunker(BaseChunker):

    # 这是BeehiivChunker类的构造函数，当我们创建这个类的一个实例时，它会被自动调用。
    def __init__(self, config: Optional[ChunkerConfig] = None):
        
        # 这里检查传入的config参数是否为空，如果为空，我们就创建一个新的ChunkerConfig对象，
        # 并设置它的默认值：chunk_size=1000（每个块的大小），chunk_overlap=0（块之间的重叠量），
        # length_function=len（计算长度的方法）。
        if config is None:
            config = ChunkerConfig(chunk_size=1000, chunk_overlap=0, length_function=len)

        # 接下来，我们使用上面设置的config参数，创建一个RecursiveCharacterTextSplitter对象，
        # 这个对象将根据config的设置来分割文本。
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            length_function=config.length_function,
        )

        # 最后，我们调用了父类BaseChunker的构造函数，并传递了我们刚刚创建的text_splitter对象，
        # 这样我们的BeehiivChunker类就有了处理文本块的能力。
        super().__init__(text_splitter)

