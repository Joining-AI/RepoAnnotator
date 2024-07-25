# 导入需要用到的模块和库
import os
import unittest
from unittest.mock import patch

# 导入自己项目中的相关模块
from embedchain import App
from embedchain.config import AppConfig, ElasticsearchDBConfig
from embedchain.embedder.gpt4all import GPT4AllEmbedder
from embedchain.vectordb.elasticsearch import ElasticsearchDB

# 定义一个继承自unittest.TestCase的类，用来编写具体的测试案例
class TestEsDB(unittest.TestCase):

    # 使用装饰器@patch来模拟Elasticsearch客户端的行为
    @patch("embedchain.vectordb.elasticsearch.Elasticsearch")
    # 定义第一个测试方法，名字叫test_setUp
    def test_setUp(self, mock_client):
        # 创建一个ElasticsearchDB实例，传入配置信息（服务器地址）
        self.db = ElasticsearchDB(config=ElasticsearchDBConfig(es_url="https://localhost:9200"))
        # 设定向量维度为384
        self.vector_dim = 384
        # 创建AppConfig实例，设置不收集度量数据
        app_config = AppConfig(collect_metrics=False)
        # 创建App实例，传入配置和数据库实例
        self.app = App(config=app_config, db=self.db)

        # 检查Elasticsearch客户端是否正确存储在ElasticsearchDB类中
        self.assertEqual(self.db.client, mock_client.return_value)

    # 再次使用装饰器@patch来模拟Elasticsearch客户端的行为
    @patch("embedchain.vectordb.elasticsearch.Elasticsearch")
    # 定义第二个测试方法，名字叫test_query
    def test_query(self, mock_client):
        # 创建一个ElasticsearchDB实例，传入配置信息（服务器地址）
        self.db = ElasticsearchDB(config=ElasticsearchDBConfig(es_url="https://localhost:9200"))
        # 创建AppConfig实例，设置不收集度量数据
        app_config = AppConfig(collect_metrics=False)
        # 创建App实例，传入配置、数据库实例以及指定的嵌入模型
        self.app = App(config=app_config, db=self.db, embedding_model=GPT4AllEmbedder())

        # 检查Elasticsearch客户端是否正确存储在ElasticsearchDB类中
        self.assertEqual(self.db.client, mock_client.return_value)

        # 准备一些示例文档数据
        documents = ["This is a document.", "This is another document."]
        # 准备这些文档的元数据
        metadatas = [{"url": "url_1", "doc_id": "doc_id_1"}, {"url": "url_2", "doc_id": "doc_id_2"}]
        # 准备文档的唯一标识符
        ids = ["doc_1", "doc_2"]

        # 将数据添加到数据库中
        self.db.add(documents, metadatas, ids)

        # 构造一个搜索响应结果的示例
        search_response = {
            "hits": {
                "hits": [
                    {
                        "_source": {"text": "This is a document.", "metadata": {"url": "url_1", "doc_id": "doc_id_1"}},
                        "_score": 0.9,
                    },
                    {
                        "_source": {
                            "text": "This is another document.",
                            "metadata": {"url": "url_2", "doc_id": "doc_id_2"},
                        },
                        "_score": 0.8,
                    },
                ]
            }
        }

        # 配置模拟的客户端返回预设的搜索响应结果
        mock_client.return_value.search.return_value = search_response

        # 查询数据库中与查询字符串"This is a document"最相似的两个文档
        query = "This is a document"
        # 获取不带引用信息的结果
        results_without_citations = self.db.query(query, n_results=2, where={})
        # 预期的结果列表
        expected_results_without_citations = ["This is a document.", "This is another document."]
        # 检查结果是否与预期一致
        self.assertEqual(results_without_citations, expected_results_without_citations)

        # 获取带有引用信息的结果
        results_with_citations = self.db.query(query, n_results=2, where={}, citations=True)
        # 预期的结果列表（包含文本和附加信息）
        expected_results_with_citations = [
            ("This is a document.", {"url": "url_1", "doc_id": "doc_id_1", "score": 0.9}),
            ("This is another document.", {"url": "url_2", "doc_id": "doc_id_2", "score": 0.8}),
        ]
        # 检查结果是否与预期一致
        self.assertEqual(results_with_citations, expected_results_with_citations)

    # 定义第三个测试方法，名字叫test_init_without_url
    def test_init_without_url(self):
        # 尝试从环境变量中删除ELASTICSEARCH_URL，如果没有就直接跳过
        try:
            del os.environ["ELASTICSEARCH_URL"]
        except KeyError:
            pass
        # 测试当提供的es_config无效时是否会抛出异常
        with self.assertRaises(AttributeError):
            ElasticsearchDB()

    # 定义第四个测试方法，名字叫test_init_with_invalid_es_config
    def test_init_with_invalid_es_config(self):
        # 测试当提供的es_config无效时是否会抛出异常
        with self.assertRaises(TypeError):
            ElasticsearchDB(es_config={"ES_URL": "some_url", "valid es_config": False})

