# 这里是从一些特别的地方拿一些我们需要的东西。
from typing import Optional   # 这个是帮助我们告诉别人，某个东西可以没有。
from langchain.text_splitter import RecursiveCharacterTextSplitter   # 这个工具帮我们把大段文字切成小块。

# 下面这些是我们自己做的东西，它们在别的地方帮助我们做事情。
from embedchain.chunkers.base_chunker import BaseChunker   # 这个是我们之前做好的切片机的基础版。
from embedchain.config.add_config import ChunkerConfig   # 这个是切片机的设置，告诉我们怎么切。
from embedchain.helpers.json_serializable import register_deserializable   # 这个是让我们的东西可以变成字符串，方便保存和分享。

# 这里是我们的超级切片机，专门用来处理网站地图（sitemap）的。
@register_deserializable   # 这个装饰器让我们这个切片机能变成字符串。
class SitemapChunker(BaseChunker):   # 我们说这个切片机是BaseChunker的升级版，专门对付网站地图。
    """Chunker for sitemap."""   # 这是在告诉别人，这个类是用来切网站地图的。

    def __init__(self, config: Optional[ChunkerConfig] = None):   # 这是切片机开始工作前的准备步骤。
        if config is None:   # 如果没有给切片机设置，我们就用默认的设置。
            config = ChunkerConfig(chunk_size=500, chunk_overlap=0, length_function=len)   # 这是默认的设置，告诉切片机每块500字，不重叠，按字数算。
        text_splitter = RecursiveCharacterTextSplitter(   # 这里我们用了一个工具，按照刚刚的设置来切文字。
            chunk_size=config.chunk_size,   # 切片大小，就是每块文字多少字。
            chunk_overlap=config.chunk_overlap,   # 切片重叠，这里是不重叠。
            length_function=config.length_function,   # 怎么计算长度，这里按字数。
        )
        super().__init__(text_splitter)   # 这里是告诉超级切片机，我们要用上面那个工具来切片，然后开始工作。

