# 这行代码是告诉Python我们要用到一些特别的工具箱里的工具。
from typing import Optional

# 这里我们从一个叫做langchain的超级大工具箱里拿出了一个叫RecursiveCharacterTextSplitter的小工具。
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 接下来是从embedchain这个工具箱里拿出两个小工具：BaseChunker和ChunkerConfig。
from embedchain.chunkers.base_chunker import BaseChunker
from embedchain.config.add_config import ChunkerConfig

# 还有一个小工具叫register_deserializable，它可以帮助我们把东西整理得更整齐。
from embedchain.helpers.json_serializable import register_deserializable

# 下面这行是在做一个标记，就像在书上做个记号，说：“嘿，这个MdxChunker类很特别哦！”
@register_deserializable

# 这里定义了一个新的类，名字叫MdxChunker，它是专门用来处理mdx文件的。
class MdxChunker(BaseChunker):
    """Chunker for mdx files."""
    
    # 这个__init__函数就像是新玩具的说明书，告诉我们怎么开始使用这个MdxChunker。
    def __init__(self, config: Optional[ChunkerConfig] = None):
        
        # 这里检查一下，如果config（就是配置信息）没有给的话，就给它一个默认的设置。
        if config is None:
            # 默认的配置是：每次切分文本的大小是1000个字符，而且切分的时候不会有重叠的部分。
            config = ChunkerConfig(chunk_size=1000, chunk_overlap=0, length_function=len)
        
        # 现在我们用上面提到的RecursiveCharacterTextSplitter工具，根据我们的配置来设置它。
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,       # 每次切分的大小
            chunk_overlap=config.chunk_overlap, # 切分时的重叠部分
            length_function=config.length_function, # 计算长度的方式
        )
        
        # 最后，我们调用父类的初始化方法，就像告诉爸爸：“我已经准备好，可以开始玩这个新玩具了！”
        super().__init__(text_splitter)

