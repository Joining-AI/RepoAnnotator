# 这里我们从Python的一个特殊模块叫做"enum"中，导入了一个叫Enum的东西。
# Enum就像是一个工具箱，能帮助我们创建一些有名字的常量，这样代码看起来更清楚。
from enum import Enum

# 下面我们开始创建一个属于我们自己的工具箱，我们给它起个名字叫做"EmbeddingFunctions"。
# 这个工具箱是用来放不同类型的文字转编码方式的名字的，这些编码方式可以帮我们把文字变成电脑能理解的语言。
class EmbeddingFunctions(Enum):
    # 这是我们工具箱里的第一个工具，我们叫它"OPENAI"，它是OpenAI公司提供的一种编码方式。
    OPENAI = "OPENAI"
    
    # 接下来是第二个工具，叫"HUGGING_FACE"，这是由Hugging Face公司提供的另一种编码方式。
    HUGGING_FACE = "HUGGING_FACE"
    
    # 第三个工具叫做"VERTEX_AI"，这是Google Vertex AI提供的一种编码方式。
    VERTEX_AI = "VERTEX_AI"
    
    # 第四个工具是"GPT4ALL"，这是一种通用的编码方式，可以在很多地方用到。
    GPT4ALL = "GPT4ALL"
    
    # 最后一个工具是"OLLAMA"，这也是一个编码方式的名字，可能来源于一个叫Ollama的项目。
    OLLAMA = "OLLAMA"

