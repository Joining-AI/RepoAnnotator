# 导入我们需要的一些工具包，这些就像是工具箱里的不同工具。
from typing import Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from embedchain.chunkers.base_chunker import BaseChunker
from embedchain.config.add_config import ChunkerConfig
from embedchain.helpers.json_serializable import register_deserializable

# 这个装饰器（就像贴在工具上的标签）告诉我们的系统，这个类可以被保存和读取，就像把工具放回工具箱或从工具箱里拿出来一样。
@register_deserializable
class DocxFileChunker(BaseChunker):
    # 这是我们特殊工具的说明书，它告诉我们这个工具是专门用来处理.docx文件的。
    """Chunker for .docx file."""
    
    # 这是工具的制作过程，我们在这里设定它的初始状态。
    def __init__(self, config: Optional[ChunkerConfig] = None):
        # 如果没有给出特别的配置，我们就用默认的配置来制作这个工具。
        if config is None:
            # 默认配置是这样的：每个小块的大小是1000个字符，小块之间没有重叠，我们用数字符的方式来计算长度。
            config = ChunkerConfig(chunk_size=1000, chunk_overlap=0, length_function=len)
        
        # 这里我们创建了一个切割器，它会按照我们设定的规则来切分文本。
        text_splitter = RecursiveCharacterTextSplitter(
            # 切割器的规则也是根据我们的配置来的，包括每个小块的大小、小块之间的重叠以及如何计算长度。
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            length_function=config.length_function,
        )
        
        # 最后，我们通过调用父类的初始化方法，来完成我们的工具制作，这样我们的工具就具备了切割文本的功能。
        super().__init__(text_splitter)

