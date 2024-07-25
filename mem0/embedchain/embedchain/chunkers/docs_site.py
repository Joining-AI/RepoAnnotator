# 引入一些必要的工具箱，就像准备画画前要先准备好颜料和画笔。
from typing import Optional  # 这个工具帮助我们说明某个东西可以有值，也可以没有值（就像你可以选择戴帽子，也可以不戴）。
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 这个工具箱里有一把特别的剪刀，能帮我们按字符来剪切文本。
from embedchain.chunkers.base_chunker import BaseChunker  # 这是我们的基础模板，所有分割文本的工作都基于它。
from embedchain.config.add_config import ChunkerConfig  # 这是我们用来设定剪切规则的配置文件，比如剪多大一块，重叠多少。
from embedchain.helpers.json_serializable import register_deserializable  # 这个工具帮助我们把类变成可以保存和读取的格式，就像把乐高模型拆开再组装。

# 使用特殊标记告诉Python，这个类可以被保存和读取，就像说这个乐高模型可以拆开后装进盒子里。
@register_deserializable
class DocsSiteChunker(BaseChunker):
    """这是一个专门用来处理代码文档网站内容的文本分割器。"""

    # 定义一个新朋友，叫DocsSiteChunker，他有一个特别的构造方法。
    def __init__(self, config: Optional[ChunkerConfig] = None):
        # 如果没有给这个新朋友指定剪切规则，我们就给他一套默认的规则。
        if config is None:
            config = ChunkerConfig(chunk_size=500, chunk_overlap=50, length_function=len)
            # 这里就像是说，“如果你没带午餐，那我就给你一个三明治，里面有500克的食物，但为了不浪费，我们允许相邻的两顿饭有50克的食物是重复的。”

        # 现在我们要用到之前提到的特别剪刀了，根据我们的规则来设置它。
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,  # 剪切的大小
            chunk_overlap=config.chunk_overlap,  # 重叠的部分
            length_function=config.length_function,  # 计算长度的方式
        )

        # 最后，我们调用超能力，让我们的新朋友继承BaseChunker的所有本领，并且带上我们刚刚设置好的剪刀。
        super().__init__(text_splitter)

