# 导入操作系统相关的功能，这里可能用来设置环境变量。
import os

# 导入pytest库，这是一个用于编写测试用例的强大工具。
import pytest

# 导入embedchain项目中的各个模块，这些模块负责处理不同的任务，比如语言模型、向量数据库等。
import embedchain
import embedchain.embedder.gpt4all
import embedchain.embedder.huggingface
import embedchain.embedder.openai
import embedchain.embedder.vertexai
import embedchain.llm.anthropic
import embedchain.llm.openai
import embedchain.vectordb.chroma
import embedchain.vectordb.elasticsearch
import embedchain.vectordb.opensearch

# 导入工厂类，这些类用于创建上面导入的各种组件实例。
from embedchain.factory import EmbedderFactory, LlmFactory, VectorDBFactory

# 定义一个名为TestFactories的测试类。
class TestFactories:
    # 使用pytest的参数化装饰器来定义一组测试数据，用于测试语言模型的创建。
    @pytest.mark.parametrize(
        "provider_name, config_data, expected_class",
        [
            # 测试OpenAI的语言模型创建。
            ("openai", {}, embedchain.llm.openai.OpenAILlm),
            # 测试Anthropic的语言模型创建。
            ("anthropic", {}, embedchain.llm.anthropic.AnthropicLlm),
        ],
    )
    # 这个方法用于测试语言模型（LLM）的创建是否正确。
    def test_llm_factory_create(self, provider_name, config_data, expected_class):
        # 设置一些环境变量，这些变量通常包含API密钥等敏感信息。
        os.environ["ANTHROPIC_API_KEY"] = "test_api_key"
        os.environ["OPENAI_API_KEY"] = "test_api_key"
        os.environ["OPENAI_API_BASE"] = "test_api_base"

        # 使用工厂类创建一个语言模型实例。
        llm_instance = LlmFactory.create(provider_name, config_data)

        # 检查创建的实例是否属于预期的类。
        assert isinstance(llm_instance, expected_class)

    # 使用pytest的参数化装饰器来定义一组测试数据，用于测试嵌入器的创建。
    @pytest.mark.parametrize(
        "provider_name, config_data, expected_class",
        [
            # 测试GPT4All嵌入器的创建。
            ("gpt4all", {}, embedchain.embedder.gpt4all.GPT4AllEmbedder),
            # 测试HuggingFace嵌入器的创建，这里指定了特定的模型和向量维度。
            (
                "huggingface",
                {"model": "sentence-transformers/all-mpnet-base-v2", "vector_dimension": 768},
                embedchain.embedder.huggingface.HuggingFaceEmbedder,
            ),
            # 测试VertexAI嵌入器的创建，指定了模型名称。
            ("vertexai", {"model": "textembedding-gecko"}, embedchain.embedder.vertexai.VertexAIEmbedder),
            # 测试OpenAI嵌入器的创建。
            ("openai", {}, embedchain.embedder.openai.OpenAIEmbedder),
        ],
    )
    # 这个方法用于测试嵌入器（Embedder）的创建是否正确。
    def test_embedder_factory_create(self, mocker, provider_name, config_data, expected_class):
        # 使用mocker（模拟工具）来模拟VertexAIEmbedder类的行为，以避免实际调用其构造函数。
        mocker.patch("embedchain.embedder.vertexai.VertexAIEmbedder", autospec=True)

        # 使用工厂类创建一个嵌入器实例。
        embedder_instance = EmbedderFactory.create(provider_name, config_data)

        # 检查创建的实例是否属于预期的类。
        assert isinstance(embedder_instance, expected_class)

    # 使用pytest的参数化装饰器来定义一组测试数据，用于测试向量数据库的创建。
    @pytest.mark.parametrize(
        "provider_name, config_data, expected_class",
        [
            # 测试ChromaDB向量数据库的创建。
            ("chroma", {}, embedchain.vectordb.chroma.ChromaDB),
            # 测试OpenSearchDB向量数据库的创建，这里指定了URL和认证信息。
            (
                "opensearch",
                {"opensearch_url": "http://localhost:9200", "http_auth": ("admin", "admin")},
                embedchain.vectordb.opensearch.OpenSearchDB,
            ),
            # 测试ElasticsearchDB向量数据库的创建，指定了URL。
            ("elasticsearch", {"es_url": "http://localhost:9200"}, embedchain.vectordb.elasticsearch.ElasticsearchDB),
        ],
    )
    # 这个方法用于测试向量数据库（VectorDB）的创建是否正确。
    def test_vectordb_factory_create(self, mocker, provider_name, config_data, expected_class):
        # 使用mocker（模拟工具）来模拟OpenSearchDB类的行为，以避免实际调用其构造函数。
        mocker.patch("embedchain.vectordb.opensearch.OpenSearchDB", autospec=True)

        # 使用工厂类创建一个向量数据库实例。
        vectordb_instance = VectorDBFactory.create(provider_name, config_data)

        # 检查创建的实例是否属于预期的类。
        assert isinstance(vectordb_instance, expected_class)

