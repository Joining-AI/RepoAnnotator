# 导入需要的库
import os  # 用于与操作系统交互
import shutil  # 提供了高级文件操作的功能
from unittest.mock import patch  # 用于模拟对象行为进行单元测试
import pytest  # 测试框架
from chromadb.config import Settings  # 从chromadb库中导入配置类
from embedchain import App  # 导入嵌入式应用
from embedchain.config import AppConfig, ChromaDbConfig  # 导入应用配置和Chroma数据库配置
from embedchain.vectordb.chroma import ChromaDB  # 导入Chroma数据库接口

# 设置环境变量，这里是设置一个测试用的API密钥
os.environ["OPENAI_API_KEY"] = "test-api-key"

# 定义一个测试夹具(fixture)，创建一个ChromaDB实例
@pytest.fixture
def chroma_db():
    # 返回一个ChromaDB实例，其中配置了主机名为'test-host'，端口号为'1234'
    return ChromaDB(config=ChromaDbConfig(host="test-host", port="1234"))

# 另一个测试夹具，创建一个带有特定设置的应用实例
@pytest.fixture
def app_with_settings():
    # 配置ChromaDB，允许重置并指定目录为'test-db'
    chroma_config = ChromaDbConfig(allow_reset=True, dir="test-db")
    # 创建ChromaDB实例
    chroma_db = ChromaDB(config=chroma_config)
    # 应用配置，这里设置不收集度量信息
    app_config = AppConfig(collect_metrics=False)
    # 返回一个带有上述配置的应用实例
    return App(config=app_config, db=chroma_db)

# 这个测试夹具会在整个测试会话结束后自动清理'test-db'目录
@pytest.fixture(scope="session", autouse=True)
def cleanup_db():
    # 使用yield关键字表示在测试执行完毕后执行后面的代码
    yield
    # 尝试删除'test-db'目录
    try:
        shutil.rmtree("test-db")
    except OSError as e:  # 如果删除过程中出现错误
        # 打印出错误信息
        print("Error: %s - %s." % (e.filename, e.strerror))

# 使用mock模拟chromadb.Client的初始化方法
@patch("embedchain.vectordb.chroma.chromadb.Client")
# 测试ChromaDB是否正确地使用主机名和端口进行初始化
def test_chroma_db_init_with_host_and_port(mock_client):
    # 创建一个ChromaDB实例，传入主机名和端口号
    chroma_db = ChromaDB(config=ChromaDbConfig(host="test-host", port="1234"))
    # 获取调用时传递的参数
    called_settings: Settings = mock_client.call_args[0][0]
    # 检查主机名和端口号是否与预期相符
    assert called_settings.chroma_server_host == "test-host"
    assert called_settings.chroma_server_http_port == "1234"

# 类似上一个测试函数，但这次测试基本认证配置
@patch("embedchain.vectordb.chroma.chromadb.Client")
def test_chroma_db_init_with_basic_auth(mock_client):
    # 定义配置字典
    chroma_config = {
        "host": "test-host",
        "port": "1234",
        "chroma_settings": {
            "chroma_client_auth_provider": "chromadb.auth.basic.BasicAuthClientProvider",
            "chroma_client_auth_credentials": "admin:admin",
        },
    }
    # 创建ChromaDB实例，并传入配置
    ChromaDB(config=ChromaDbConfig(**chroma_config))
    # 获取调用时传递的参数
    called_settings: Settings = mock_client.call_args[0][0]
    # 检查主机名、端口号、认证提供者和凭证是否与预期相符
    assert called_settings.chroma_server_host == "test-host"
    assert called_settings.chroma_server_http_port == "1234"
    assert (
        called_settings.chroma_client_auth_provider == chroma_config["chroma_settings"]["chroma_client_auth_provider"]
    )
    assert (
        called_settings.chroma_client_auth_credentials
        == chroma_config["chroma_settings"]["chroma_client_auth_credentials"]
    )

# 测试带有主机名和端口的应用初始化
@patch("embedchain.vectordb.chroma.chromadb.Client")
def test_app_init_with_host_and_port(mock_client):
    # 定义主机名和端口号
    host = "test-host"
    port = "1234"
    # 创建应用配置实例
    config = AppConfig(collect_metrics=False)
    # 创建ChromaDB配置实例
    db_config = ChromaDbConfig(host=host, port=port)
    # 创建ChromaDB实例
    db = ChromaDB(config=db_config)
    # 创建应用实例
    _app = App(config=config, db=db)
    # 获取调用时传递的参数
    called_settings: Settings = mock_client.call_args[0][0]
    # 检查主机名和端口号是否与预期相符
    assert called_settings.chroma_server_host == host
    assert called_settings.chroma_server_http_port == port

# 测试当主机名和端口未设置时的应用初始化
@patch("embedchain.vectordb.chroma.chromadb.Client")
def test_app_init_with_host_and_port_none(mock_client):
    # 创建允许重置的ChromaDB实例
    db = ChromaDB(config=ChromaDbConfig(allow_reset=True, dir="test-db"))
    # 创建应用实例
    _app = App(config=AppConfig(collect_metrics=False), db=db)
    # 获取调用时传递的参数
    called_settings: Settings = mock_client.call_args[0][0]
    # 检查主机名和端口号是否为None
    assert called_settings.chroma_server_host is None
    assert called_settings.chroma_server_http_port is None

# 测试重复插入数据时的警告信息
def test_chroma_db_duplicates_throw_warning(caplog):
    # 创建允许重置的ChromaDB实例
    db = ChromaDB(config=ChromaDbConfig(allow_reset=True, dir="test-db"))
    # 创建应用实例
    app = App(config=AppConfig(collect_metrics=False), db=db)
    # 向集合中添加相同的ID和嵌入向量
    app.db.collection.add(embeddings=[[0, 0, 0]], ids=["0"])
    app.db.collection.add(embeddings=[[0, 0, 0]], ids=["0"])
    # 检查日志中是否包含了预期的警告信息
    assert "Insert of existing embedding ID: 0" in caplog.text
    assert "Add of existing embedding ID: 0" in caplog.text
    # 重置数据库
    app.db.reset()

# 这个函数测试当向同一个数据库中两个不同的集合插入相同ID的数据时，不会出现警告信息。
def test_chroma_db_duplicates_collections_no_warning(caplog):
    # 创建一个允许重置的 ChromaDB 实例，并指定存储目录。
    db = ChromaDB(config=ChromaDbConfig(allow_reset=True, dir="test-db"))
    # 创建一个不收集度量信息的应用实例，并关联上面创建的数据库。
    app = App(config=AppConfig(collect_metrics=False), db=db)
    # 设置当前使用的集合名称为 "test_collection_1"。
    app.set_collection_name("test_collection_1")
    # 向集合添加一个嵌入向量和对应的ID。
    app.db.collection.add(embeddings=[[0, 0, 0]], ids=["0"])
    # 设置当前使用的集合名称为 "test_collection_2"。
    app.set_collection_name("test_collection_2")
    # 再次向另一个集合添加相同的嵌入向量和ID。
    app.db.collection.add(embeddings=[[0, 0, 0]], ids=["0"])
    # 检查日志，确保没有出现关于重复ID的警告信息。
    assert "Insert of existing embedding ID: 0" not in caplog.text
    assert "Add of existing embedding ID: 0" not in caplog.text
    # 重置数据库。
    app.db.reset()
    # 再次设置当前使用的集合名称为 "test_collection_1"。
    app.set_collection_name("test_collection_1")
    # 重置数据库。
    app.db.reset()

def test_chroma_db_collection_ids_share_collections():

