# 这里我们从typing库导入了Optional，这个东西是用来帮助我们告诉Python，“嘿，这里可能有东西，也可能没有。”
from typing import Optional

# 我们从langchain库中导入了一个叫做RecursiveCharacterTextSplitter的东西。它就像一把剪刀，可以帮我们把大段的文字剪成小块。
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 现在，我们从embedchain的chunkers文件夹里找到base_chunker.py，然后导入BaseChunker类。这就像我们有一个基础的工具箱，而BaseChunker就是里面的一种工具。
from embedchain.chunkers.base_chunker import BaseChunker

# 接下来，我们从add_config.py文件中导入ChunkerConfig类。这个就像是我们做手工前的准备，决定要用多大的纸片和多少重叠的部分。
from embedchain.config.add_config import ChunkerConfig

# 这里我们从helpers文件夹里的json_serializable.py导入register_deserializable装饰器。这个装饰器就像是一个魔术师，能让我们的类变成可以被保存和读取的格式。
from embedchain.helpers.json_serializable import register_deserializable

# 下面这一行很特别，我们使用了上面提到的魔术师（装饰器），告诉Python，“嘿，GmailChunker这个类可以变成可以保存和读取的格式哦！”
@register_deserializable
class GmailChunker(BaseChunker):
    # 这里是GmailChunker类的开始，它继承自BaseChunker，就像它是BaseChunker家族的一员，但是它有自己的特殊技能。
    """Chunker for gmail."""
    
    # 这个是GmailChunker类的构造函数，也就是当我们要创建一个新的GmailChunker实例时，会做的事情。
    def __init__(self, config: Optional[ChunkerConfig] = None):
        # 这里我们检查config参数是不是None，如果是，就创建一个新的ChunkerConfig实例，设置它的属性。
        if config is None:
            config = ChunkerConfig(chunk_size=1000, chunk_overlap=0, length_function=len)
        
        # 然后我们创建一个RecursiveCharacterTextSplitter实例，传入我们刚刚准备好的config，这样我们就有了剪切文字的小剪刀。
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            length_function=config.length_function,
        )
        
        # 最后，我们调用super().__init__()，这是在告诉Python，“我要用我继承自BaseChunker的所有功能，并且我已经准备好我的小剪刀了！”
        super().__init__(text_splitter)

