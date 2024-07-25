# 首先，我们从typing模块导入Optional，这个工具帮助我们在定义变量时，可以指定它可能没有值。
from typing import Optional

# 然后，我们从langchain的text_splitter模块导入RecursiveCharacterTextSplitter，
# 这个类能帮我们将一大段文字分成小块，就像是把一个大蛋糕切成很多小块。
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 下面，我们从embedchain的base_chunker模块导入BaseChunker，
# 它是所有文本切割器的基础，就像画画时的画布，所有的画家都会用到。
from embedchain.chunkers.base_chunker import BaseChunker

# 再来，我们从embedchain的config.add_config模块导入ChunkerConfig，
# 这个配置类帮助我们设定如何切割文本的规则，比如切多大一块，重叠多少等。
from embedchain.config.add_config import ChunkerConfig

# 这里我们导入了一个叫做json_serializable的模块中的register_deserializable装饰器，
# 这个装饰器就像是魔法，能让我们的类变成可以被保存和读取的格式，就像书签一样方便。
from embedchain.helpers.json_serializable import register_deserializable


# 使用上面的魔法装饰器，我们定义了一个叫CommonChunker的类，它是所有加载器使用的通用文本切割器。
@register_deserializable
class CommonChunker(BaseChunker):
    # 这个类有一个构造函数，当我们创建CommonChunker对象时会被调用。
    def __init__(self, config: Optional[ChunkerConfig] = None):
        # 如果传入的config参数是None，我们就自己创建一个默认的配置。
        if config is None:
            # 我们创建一个ChunkerConfig实例，设置切割大小为2000，没有重叠，长度计算方式就是普通的len()函数。
            config = ChunkerConfig(chunk_size=2000, chunk_overlap=0, length_function=len)
        # 接着，我们使用config配置创建一个RecursiveCharacterTextSplitter实例，
        # 就像根据菜谱制作一个切蛋糕的刀具。
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            length_function=config.length_function,
        )
        # 最后，我们调用父类BaseChunker的构造函数，将我们刚才制作的刀具传进去，
        # 就像告诉厨师长我们准备好了切割蛋糕的工具，可以开始工作了。
        super().__init__(text_splitter)

