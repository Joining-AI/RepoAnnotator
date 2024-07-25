# 导入 Enum 这个类，这个类是用来定义一些固定的选项的。
from enum import Enum

# 下面我们定义了一个叫做 VectorDimensions 的类，它继承了 Enum 类。
# 这个类用来表示不同的人工智能模型生成的向量长度。
# 每个人工智能模型都有一个固定长度的向量，这些向量是由模型内部的一些数学计算产生的。
# 现在我们就把每个模型的名字和对应的向量长度写在这里。
class VectorDimensions(Enum):
    # GPT4ALL 模型产生的向量长度是 384。
    GPT4ALL = 384
    # OPENAI 模型产生的向量长度是 1536。
    OPENAI = 1536
    # VERTEX_AI 模型产生的向量长度是 768。
    VERTEX_AI = 768
    # HUGGING_FACE 模型产生的向量长度是 384。
    HUGGING_FACE = 384
    # GOOGLE_AI 模型产生的向量长度是 768。
    GOOGLE_AI = 768
    # MISTRAL_AI 模型产生的向量长度是 1024。
    MISTRAL_AI = 1024
    # NVIDIA_AI 模型产生的向量长度也是 1024。
    NVIDIA_AI = 1024
    # COHERE 模型产生的向量长度是 384。
    COHERE = 384
    # OLLAMA 模型产生的向量长度是 384。
    OLLAMA = 384

