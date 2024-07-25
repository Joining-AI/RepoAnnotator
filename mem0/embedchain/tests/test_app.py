# 这里我们导入了操作系统相关的工具，可以用来设置环境变量。
import os

# pytest 是一个用于编写测试代码的库，它可以帮助我们检查代码是否正确工作。
import pytest

# yaml 是一种数据序列化格式，常用于配置文件中，这里可能用于读取或写入配置信息。
import yaml

# 接下来我们导入了一些与“embedchain”项目有关的类和配置，这个项目是用来处理文本嵌入和数据库操作的。
from embedchain import App
from embedchain.config import ChromaDbConfig
from embedchain.embedder.base import BaseEmbedder
from embedchain.llm.base import BaseLlm
from embedchain.vectordb.base import BaseVectorDB
from embedchain.vectordb.chroma import ChromaDB

# 这里定义了一个特殊的函数叫做“fixture”，它会在运行测试前被调用，用来准备一些初始状态。
@pytest.fixture
def app():
    # 我们设置两个环境变量，它们通常用于与OpenAI API交互时提供认证信息。
    os.environ["OPENAI_API_KEY"] = "test-api-key"
    os.environ["OPENAI_API_BASE"] = "test-api-base"
    # 创建一个“App”实例，这是embedchain框架的核心部分。
    return App()

# 定义了一个测试函数，它的作用是检查“app”实例的各个组件是否正确初始化。
def test_app(app):
    # 检查“app”的LLM（语言模型）组件是否是BaseLlm类的实例。
    assert isinstance(app.llm, BaseLlm)
    # 检查“app”的数据库组件是否是BaseVectorDB类的实例。
    assert isinstance(app.db, BaseVectorDB)
    # 检查“app”的嵌入模型组件是否是BaseEmbedder类的实例。
    assert isinstance(app.embedding_model, BaseEmbedder)

# 这是一个类，包含了几个测试方法，专门用于检查“App”组件的配置。
class TestConfigForAppComponents:
    # 第一个测试方法，检查在构造App时传入的配置是否被正确应用。
    def test_constructor_config(self):
        # 定义一个集合名称，这将用于Chroma数据库的特定集合。
        collection_name = "my-test-collection"
        # 创建一个ChromaDB实例，并传入配置信息。
        db = ChromaDB(config=ChromaDbConfig(collection_name=collection_name))
        # 使用上面创建的数据库实例来创建一个App实例。
        app = App(db=db)
        # 检查App实例中的数据库配置是否与我们之前设置的一致。
        assert app.db.config.collection_name == collection_name

    # 第二个测试方法，检查通过组件方式传入的配置是否被正确应用。
    def test_component_config(self):
        # 同样地，我们定义一个集合名称。
        collection_name = "my-test-collection"
        # 创建一个ChromaDB实例，并传入配置信息。
        database = ChromaDB(config=ChromaDbConfig(collection_name=collection_name))
        # 使用上面创建的数据库实例来创建一个App实例。
        app = App(db=database)
        # 检查App实例中的数据库配置是否与我们之前设置的一致。
        assert app.db.config.collection_name == collection_name

class TestAppFromConfig:   # 定义一个名为TestAppFromConfig的类，用来做测试。

