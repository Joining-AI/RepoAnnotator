# 导入pytest库，这是一个用来写测试的库。
import pytest

# 从chromadb库中导入我们需要的Documents和Embeddings类型定义。
from chromadb.api.types import Documents, Embeddings

# 从我们自己的项目文件里导入BaseEmbedderConfig类，这是嵌入器的基础配置。
from embedchain.config.embedder.base import BaseEmbedderConfig

# 从我们自己的项目文件里导入BaseEmbedder类，这是所有嵌入器的基础类。
from embedchain.embedder.base import BaseEmbedder

# 使用pytest的一个特殊装饰器来定义一个测试用例中的共享资源（比如这个例子里的基础嵌入器）。
# 这个装饰器创建了一个叫做base_embedder的对象，它是一个BaseEmbedder的实例。
@pytest.fixture
def base_embedder():
    return BaseEmbedder()

# 定义一个测试函数，用于检查BaseEmbedder对象是否正确初始化了配置。
def test_initialization(base_embedder):
    # 检查base_embedder的config属性是否是BaseEmbedderConfig类型的实例。
    assert isinstance(base_embedder.config, BaseEmbedderConfig)

    # 检查base_embedder对象是否没有embedding_fn属性，因为此时还没有设置。
    assert not hasattr(base_embedder, "embedding_fn")

    # 同样，检查base_embedder对象是否没有vector_dimension属性，因为此时还没有设置。
    assert not hasattr(base_embedder, "vector_dimension")

# 定义一个测试函数，用于检查设置embedding_fn方法是否有效。
def test_set_embedding_fn(base_embedder):
    # 定义一个简单的函数，它接收一些文本并返回它们的“嵌入”表示。
    # 这里只是简单地在每个文本前面加上"Embedding for "。
    def embedding_function(texts: Documents) -> Embeddings:
        return [f"Embedding for {text}" for text in texts]

    # 使用set_embedding_fn方法来设置刚刚定义的embedding_function作为base_embedder的嵌入函数。
    base_embedder.set_embedding_fn(embedding_function)

    # 检查base_embedder现在是否有了embedding_fn属性。
    assert hasattr(base_embedder, "embedding_fn")

    # 检查base_embedder的embedding_fn属性是否是一个可以调用的函数。
    assert callable(base_embedder.embedding_fn)

    # 调用base_embedder的embedding_fn来获取"text1"和"text2"的嵌入表示。
    embeddings = base_embedder.embedding_fn(["text1", "text2"])

    # 检查返回的结果是否与预期一致，即["Embedding for text1", "Embedding for text2"]。
    assert embeddings == ["Embedding for text1", "Embedding for text2"]

# 定义一个测试函数，用于检查如果尝试设置一个不是函数的embedding_fn会发生什么。
def test_set_embedding_fn_when_not_a_function(base_embedder):
    # 使用pytest的raises上下文管理器来确认如果传递None给set_embedding_fn会抛出ValueError异常。
    with pytest.raises(ValueError):
        base_embedder.set_embedding_fn(None)

# 定义一个测试函数，用于检查设置向量维度的方法是否有效。
def test_set_vector_dimension(base_embedder):
    # 设置向量维度为256。
    base_embedder.set_vector_dimension(256)

    # 检查base_embedder现在是否有了vector_dimension属性。
    assert hasattr(base_embedder, "vector_dimension")

    # 检查vector_dimension属性是否等于256。
    assert base_embedder.vector_dimension == 256

# 定义一个测试函数，用于检查如果尝试设置一个不是数字的向量维度会发生什么。
def test_set_vector_dimension_type_error(base_embedder):
    # 使用pytest的raises上下文管理器来确认如果传递None给set_vector_dimension会抛出TypeError异常。
    with pytest.raises(TypeError):
        base_embedder.set_vector_dimension(None)

# 定义一个测试函数，用于检查使用BaseEmbedderConfig实例化BaseEmbedder是否有效。
def test_embedder_with_config():
    # 创建一个新的BaseEmbedder实例，并传入BaseEmbedderConfig实例作为参数。
    embedder = BaseEmbedder(BaseEmbedderConfig())

    # 检查embedder的config属性是否是BaseEmbedderConfig类型的实例。
    assert isinstance(embedder.config, BaseEmbedderConfig)

