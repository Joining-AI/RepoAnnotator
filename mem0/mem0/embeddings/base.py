# 导入abc模块中的ABC类和abstractmethod装饰器
from abc import ABC, abstractmethod

# 定义了一个名为EmbeddingBase的类，并且它继承自ABC类（这会让这个类变成一个抽象基类）
class EmbeddingBase(ABC):
    # 使用abstractmethod装饰器标记了一个名为embed的方法，这意味着任何从EmbeddingBase继承的类都必须实现这个方法
    @abstractmethod
    def embed(self, text):
        # 这是一个文档字符串，用来说明这个方法的作用：获取给定文本的嵌入向量。
        """
        获取给定文本的嵌入向量。

        参数:
            text (str): 需要转换成向量的文本。

        返回值:
            list: 文本对应的嵌入向量。
        """
        # 这里写的是"pass"，表示这个方法目前什么也不做。但因为有abstractmethod装饰器，
        # 所以在实际使用时，任何继承此基类的新类都需要重写这个方法并提供具体的功能。
        pass

