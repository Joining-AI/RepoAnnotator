# 这里我们从typing模块导入了Optional这个东西，
# 它可以帮助我们在写代码时，告诉别人某个变量可以是None（也就是什么都没有）。
from typing import Optional

# 接下来，我们从langchain库中导入了一个叫RecursiveCharacterTextSplitter的类，
# 这个类能帮我们将一大段文字拆分成更小的部分。
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 然后，我们从embedchain库中的chunkers模块导入了BaseChunker这个类，
# 这个类是我们要创建的NotionChunker类的基础，它提供了一些基本的功能。
from embedchain.chunkers.base_chunker import BaseChunker

# 再从embedchain库的config模块导入了ChunkerConfig这个类，
# 这个类用来设置如何拆分文本的规则。
from embedchain.config.add_config import ChunkerConfig

# 最后，我们从embedchain库的helpers模块导入了json_serializable中的register_deserializable装饰器，
# 这个装饰器可以让我们的类更容易被保存和读取。
from embedchain.helpers.json_serializable import register_deserializable

# 现在，我们开始定义我们自己的类，叫做NotionChunker，
# 它继承自BaseChunker，也就是说它具有BaseChunker的所有功能，但还可以添加一些新的功能。
@register_deserializable
class NotionChunker(BaseChunker):
    # 下面是NotionChunker类的说明，告诉别人这个类是做什么的。
    """Chunker for notion."""
    
    # 这是NotionChunker类的构造函数，当我们创建NotionChunker的对象时，这个函数会被调用。
    def __init__(self, config: Optional[ChunkerConfig] = None):
        # 如果在创建对象时没有传入config参数，那么我们就创建一个新的ChunkerConfig对象，
        # 并设置它的chunk_size为300（表示每个小段文本的长度），chunk_overlap为0（表示小段文本之间的重叠部分为0），
        # length_function为len（表示计算文本长度的方法）。
        if config is None:
            config = ChunkerConfig(chunk_size=300, chunk_overlap=0, length_function=len)
        
        # 然后，我们创建一个RecursiveCharacterTextSplitter对象，
        # 并将之前设置的config对象的属性作为参数传进去，这样就告诉了这个对象如何拆分文本。
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            length_function=config.length_function,
        )
        
        # 最后，我们调用父类BaseChunker的构造函数，并传入我们刚刚创建的text_splitter对象，
        # 这样我们的NotionChunker对象就可以使用text_splitter来拆分文本了。
        super().__init__(text_splitter)

