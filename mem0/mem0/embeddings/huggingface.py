# 导入一个叫做 EmbeddingBase 的基类
from embedding.base import EmbeddingBase
# 导入一个叫做 SentenceTransformer 的类，这个类可以帮助我们使用预训练好的模型进行文本处理
from sentence_transformers import SentenceTransformer


# 定义一个新的类，名字叫 HuggingFaceEmbedding，它继承了 EmbeddingBase 类
class HuggingFaceEmbedding(EmbeddingBase):
    # 初始化函数，当创建这个类的新对象时会自动调用
    def __init__(self, model_name="multi-qa-MiniLM-L6-cos-v1"):
        # 这里设置了一个默认的模型名称 "multi-qa-MiniLM-L6-cos-v1"，
        # 当创建对象时如果没有指定模型名称，就会使用这个默认值
        # 使用 SentenceTransformer 类加载指定的预训练模型
        self.model = SentenceTransformer(model_name)

    # 定义一个方法，名字叫 get_embedding，用来获取文本的嵌入向量
    def get_embedding(self, text):
        # 这个方法接收一个参数，就是需要转换的文本
        # 文档字符串，解释了这个方法的作用、参数和返回值
        """
        使用 Hugging Face 模型获取给定文本的嵌入向量。

        参数:
            text (str): 需要转换的文本。

        返回:
            list: 文本对应的嵌入向量。
        """
        # 使用之前加载好的模型对输入的文本进行编码，并返回编码结果
        return self.model.encode(text)

