# 引入OpenAI库中的一个类叫做OpenAI
from openai import OpenAI

# 从mem0库的embeddings模块下的base文件中引入一个叫做EmbeddingBase的类
from mem0.embeddings.base import EmbeddingBase

# 定义一个新的类叫做OpenAIEmbedding，它继承自EmbeddingBase类
class OpenAIEmbedding(EmbeddingBase):
    # 这个类的初始化函数
    def __init__(self, model="text-embedding-3-small"):
        # 初始化函数里面创建了一个OpenAI客户端对象
        self.client = OpenAI()
        # 设置模型的名字，默认是"text-embedding-3-small"
        self.model = model
        # 设置向量的维度为1536
        self.dims = 1536

    # 定义一个叫做embed的方法，用来处理文本并生成向量
    def embed(self, text):
        """
        使用OpenAI的工具来获取给定文本的向量表示。

        参数:
            text (str): 需要转换的文本。

        返回:
            list: 文本对应的向量。
        """
        # 先把文本里的换行符替换成空格
        text = text.replace("\n", " ")
        # 使用OpenAI客户端对象的embeddings方法创建向量
        # 把处理后的文本传进去，指定使用的模型
        # 然后取出返回数据中的向量部分
        return (
            self.client.embeddings.create(input=[text], model=self.model)
            .data[0]
            .embedding
        )

