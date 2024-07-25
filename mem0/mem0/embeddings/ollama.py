# 首先，我们需要告诉我们的小机器人去哪里找到需要用到的一些特殊工具。
import ollama
from embedding.base import EmbeddingBase

# 现在我们要开始写我们自己的小机器人了！这个小机器人的名字叫做 OllamaEmbedding，它是从一个叫 EmbeddingBase 的大机器人那里学习来的。
class OllamaEmbedding(EmbeddingBase):
    # 当我们的小机器人第一次被创造出来的时候，它需要做一些准备工作。
    def __init__(self, model="nomic-embed-text"):
        # 小机器人会记住我们给它的模型的名字，默认是 "nomic-embed-text"。
        self.model = model
        # 接下来，小机器人要确保这个模型已经准备好了，如果没有准备好，它会去把它找来。
        self._ensure_model_exists()
        # 还有一个重要的事情，就是小机器人要知道这个模型产生的数字串有多长，这里是 512 个数字。
        self.dims = 512

    # 这个方法是小机器人用来确保模型已经准备好了的方法。
    def _ensure_model_exists(self):
        """
        确保指定的模型已经准备好了。如果没有，就让小机器人去把它找来。
        """
        # 首先，小机器人要列出所有它能找到的模型的名字。
        model_list = [m["name"] for m in ollama.list()["models"]]
        # 然后，小机器人检查一下列表里有没有以它需要的那个模型名开头的模型。
        if not any(m.startswith(self.model) for m in model_list):
            # 如果没有的话，小机器人就会去把它找来。
            ollama.pull(self.model)

    # 这个方法是小机器人用来把文字变成数字串的方法。
    def embed(self, text):
        """
        让小机器人把给定的文字变成一串特殊的数字。

        参数:
            text (str): 就是我们想要让它变的那句话。

        返回:
            list: 变出来的那一串数字。
        """
        # 小机器人会用它准备好的模型来处理我们给它的文字。
        response = ollama.embeddings(model=self.model, prompt=text)
        # 最后，小机器人会把变出来的数字串给我们。
        return response["embedding"]

