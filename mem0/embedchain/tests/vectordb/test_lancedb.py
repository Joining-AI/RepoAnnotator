# 引入操作系统相关功能，用于环境变量设置和文件操作
import os
# 引入文件拷贝和删除功能，用于清理测试产生的文件
import shutil
# 引入pytest库，用于编写和运行单元测试
import pytest
# 引入App类，可能是应用程序的主要类
from embedchain import App
# 引入AppConfig类，用于配置应用程序的行为
from embedchain.config import AppConfig
# 引入LanceDBConfig类，用于配置LanceDB数据库的行为
from embedchain.config.vector_db.lancedb import LanceDBConfig
# 引入LanceDB类，这是基于LanceDB的向量数据库实现
from embedchain.vectordb.lancedb import LanceDB

# 设置环境变量，用于测试的OpenAI API密钥，这里只是一个示例值
os.environ["OPENAI_API_KEY"] = "test-api-key"

# 这个函数测试了LanceDB数据库里的集合（collection）是否能持久化存储数据。
def test_lancedb_collection_collections_are_persistent():
    db = LanceDB(config=LanceDBConfig(allow_reset=True, dir="test-db"))  # 创建一个LanceDB数据库实例，允许重置，并指定存储路径。
    app = App(config=AppConfig(collect_metrics=False), db=db)  # 创建一个应用实例，关联上面创建的数据库，设置不收集度量信息。
    app.set_collection_name("test_collection_1")  # 设置这个应用使用的集合名字。
    app.db.add(ids=["0"], documents=["doc1"], metadatas=["test"])  # 往集合里添加一条记录，包括ID、文档内容和元数据。
    del app  # 删除应用实例。

    db = LanceDB(config=LanceDBConfig(allow_reset=True, dir="test-db"))  # 再次创建一个LanceDB数据库实例。
    app = App(config=AppConfig(collect_metrics=False), db=db)  # 再次创建应用实例。
    app.set_collection_name("test_collection_1")  # 设置应用使用的集合名。
    assert app.db.count() == 1  # 检查集合里的记录数量是不是1条，如果不是就会报错。

    app.db.reset()  # 清空这个集合。

