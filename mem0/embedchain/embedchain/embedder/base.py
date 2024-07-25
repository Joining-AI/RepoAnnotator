# 导入需要的库和模块。
from collections.abc import Callable  # 从集合库中导入Callable类，用于检查函数。
from typing import Any, Optional  # 从typing库导入Any和Optional类型提示。
from embedchain.config.embedder.base import BaseEmbedderConfig  # 从embedchain库中导入BaseEmbedderConfig配置类。

# 尝试导入chromadb库中的几个类型定义。
try:
    from chromadb.api.types import Embeddable, EmbeddingFunction, Embeddings  # 如果可以，就直接导入这些类型。
except RuntimeError:  # 如果运行时出现错误（比如缺少依赖），则执行以下代码。
    from embedchain.utils.misc import use_pysqlite3  # 从embedchain库中导入use_pysqlite3函数。
    use_pysqlite3()  # 调用use_pysqlite3函数，可能用于处理一些依赖问题。
    from chromadb.api.types import Embeddable, EmbeddingFunction, Embeddings  # 再次尝试导入这些类型。

# 定义一个类，名为EmbeddingFunc，继承自EmbeddingFunction。
class EmbeddingFunc(EmbeddingFunction):
    def __init__(self, embedding_fn: Callable[[list[str]], list[str]]):  # 初始化函数，传入一个函数作为参数。
        self.embedding_fn = embedding_fn  # 把传入的函数保存为类的一个属性。

    def __call__(self, input: Embeddable) -> Embeddings:  # 当这个类的对象被当作函数调用时，会执行这里的代码。
        return self.embedding_fn(input)  # 调用保存的函数，并返回结果。

# 定义一个基类，名为BaseEmbedder，用于处理嵌入（embedding）相关的操作。
class BaseEmbedder:
    """
    这个类管理所有关于嵌入的事情，包括嵌入函数、加载器和分块器。
    根据你选择的具体子类，嵌入函数和向量维度会被设置好。
    如果你需要手动更改，可以使用这个类里的`set_...`方法。
    """

    def __init__(self, config: Optional[BaseEmbedderConfig] = None):  # 初始化函数，可选地传入一个配置对象。
        """
        初始化这个嵌入器类。
        
        :param config: 可以传入一个配置对象，默认是None。
        :type config: Optional[BaseEmbedderConfig], 可选的
        """
        if config is None:  # 如果没有传入配置对象，则创建一个默认的配置对象。
            self.config = BaseEmbedderConfig()
        else:
            self.config = config  # 否则就使用传入的配置对象。
        self.vector_dimension: int  # 设置向量维度的属性。

    def set_embedding_fn(self, embedding_fn: Callable[[list[str]], list[str]]):  # 设置或替换嵌入函数的方法。
        """
        设置或替换数据库用来存储和检索文档时使用的嵌入函数。

        :param embedding_fn: 生成嵌入的函数。
        :type embedding_fn: Callable[[list[str]], list[str]]
        :raises ValueError: 如果嵌入函数不是真正的函数，会抛出错误。
        """
        if not hasattr(embedding_fn, "__call__"):  # 检查传入的是否是一个函数。
            raise ValueError("嵌入函数不是一个真正的函数")
        self.embedding_fn = embedding_fn  # 把传入的函数保存为类的一个属性。

    def set_vector_dimension(self, vector_dimension: int):  # 设置或替换向量维度大小的方法。
        """
        设置或替换向量维度的大小。

        :param vector_dimension: 向量的维度大小。
        :type vector_dimension: int
        """
        if not isinstance(vector_dimension, int):  # 检查传入的是否是整数。
            raise TypeError("向量维度必须是整数")
        self.vector_dimension = vector_dimension  # 把传入的值保存为类的一个属性。

    @staticmethod
    def _langchain_default_concept(embeddings: Any):  # 静态方法，用于生成Langchain默认的嵌入函数布局。
        """
        Langchain默认的嵌入函数布局。

        :param embeddings: Langchain的嵌入对象。
        :type embeddings: Any
        :return: 嵌入函数。
        :rtype: Callable
        """

        return EmbeddingFunc(embeddings.embed_documents)  # 返回一个EmbeddingFunc对象，它使用了传入对象的`embed_documents`方法。

    def to_embeddings(self, data: str, **_):  # 把数据转换成嵌入的方法。
        """
        把数据转换成嵌入。

        :param data: 需要转换的数据。
        :type data: str
        :return: 嵌入结果。
        :rtype: list[float]
        """
        embeddings = self.embedding_fn([data])  # 使用已设置的嵌入函数处理数据。
        return embeddings[0]  # 返回处理后的第一个结果。

