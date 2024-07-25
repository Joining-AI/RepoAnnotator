import importlib

# 定义了一个叫做 EmbedderFactory 的类
class EmbedderFactory:
    # 这是一个字典，它把不同的服务名字（比如 "azure_openai"）映射到对应的类名
    provider_to_class = {
        "azure_openai": "embedchain.embedder.azure_openai.AzureOpenAIEmbedder",  # Azure OpenAI 的嵌入器
        "gpt4all": "embedchain.embedder.gpt4all.GPT4AllEmbedder",  # GPT4All 的嵌入器
        "huggingface": "embedchain.embedder.huggingface.HuggingFaceEmbedder",  # Hugging Face 的嵌入器
        "openai": "embedchain.embedder.openai.OpenAIEmbedder",  # OpenAI 的嵌入器
        "vertexai": "embedchain.embedder.vertexai.VertexAIEmbedder",  # Vertex AI 的嵌入器
        "google": "embedchain.embedder.google.GoogleAIEmbedder",  # Google 的嵌入器
        "mistralai": "embedchain.embedder.mistralai.MistralAIEmbedder",  # Mistral AI 的嵌入器
        "clarifai": "embedchain.embedder.clarifai.ClarifaiEmbedder",  # Clarifai 的嵌入器
        "nvidia": "embedchain.embedder.nvidia.NvidiaEmbedder",  # NVIDIA 的嵌入器
        "cohere": "embedchain.embedder.cohere.CohereEmbedder",  # Cohere 的嵌入器
        "ollama": "embedchain.embedder.ollama.OllamaEmbedder",  # Ollama 的嵌入器
    }
    # 这个字典用来把服务名字映射到配置类的名字
    provider_to_config_class = {
        "azure_openai": "embedchain.config.embedder.base.BaseEmbedderConfig",  # Azure OpenAI 配置类
        "google": "embedchain.config.embedder.google.GoogleAIEmbedderConfig",  # Google 配置类
        "gpt4all": "embedchain.config.embedder.base.BaseEmbedderConfig",  # GPT4All 配置类
        "huggingface": "embedchain.config.embedder.base.BaseEmbedderConfig",  # Hugging Face 配置类
        "clarifai": "embedchain.config.embedder.base.BaseEmbedderConfig",  # Clarifai 配置类
        "openai": "embedchain.config.embedder.base.BaseEmbedderConfig",  # OpenAI 配置类
        "ollama": "embedchain.config.embedder.ollama.OllamaEmbedderConfig",  # Ollama 配置类
    }

    # 这是一个特殊的方法，它用 `@classmethod` 装饰器标记，表示这个方法是类方法。
    # 类方法的第一个参数总是类本身，这里用 `cls` 表示。这个方法用于创建一个嵌入器实例。
    @classmethod
    def create(cls, provider_name, config_data):
        # 根据提供的服务名字 `provider_name`，从 `provider_to_class` 字典中找到对应的类名
        class_type = cls.provider_to_class.get(provider_name)
        # 如果没有找到对应的服务名字在 `provider_to_config_class` 中，就默认使用 OpenAI 的配置类
        config_name = "openai" if provider_name not in cls.provider_to_config_class else provider_name
        # 同样地，根据 `config_name` 找到对应的配置类名
        config_class_type = cls.provider_to_config_class.get(config_name)
        # 如果找到了对应的类名
        if class_type:
            # 使用一个叫做 `load_class` 的函数加载这个类名对应的类
            embedder_class = load_class(class_type)
            # 加载配置类
            embedder_config_class = load_class(config_class_type)
            # 创建并返回一个嵌入器实例，传入配置数据
            return embedder_class(config=embedder_config_class(**config_data))
        else:
            # 如果没有找到对应的类名，抛出一个错误，告诉用户这个服务名字不支持
            raise ValueError(f"Unsupported Embedder provider: {provider_name}")
            

# 定义了一个叫做 VectorDBFactory 的类
class VectorDBFactory:
    # 这个字典把不同的数据库服务名字映射到对应的类名
    provider_to_class = {
        "chroma": "embedchain.vectordb.chroma.ChromaDB",  # Chroma 数据库
        "elasticsearch": "embedchain.vectordb.elasticsearch.ElasticsearchDB",  # Elasticsearch 数据库
        "opensearch": "embedchain.vectordb.opensearch.OpenSearchDB",  # OpenSearch 数据库
        "lancedb": "embedchain.vectordb.lancedb.LanceDB",  # LanceDB 数据库
        "pinecone": "embedchain.vectordb.pinecone.PineconeDB",  # Pinecone 数据库
        "qdrant": "embedchain.vectordb.qdrant.QdrantDB",  # Qdrant 数据库
        "weaviate": "embedchain.vectordb.weaviate.WeaviateDB",  # Weaviate 数据库
        "zilliz": "embedchain.vectordb.zilliz.ZillizVectorDB",  # Zilliz 数据库
    }
    # 这个字典把数据库服务名字映射到对应的配置类名
    provider_to_config_class = {
        "chroma": "embedchain.config.vector_db.chroma.ChromaDbConfig",  # Chroma 配置类
        "elasticsearch": "embedchain.config.vector_db.elasticsearch.ElasticsearchDBConfig",  # Elasticsearch 配置类
        "opensearch": "embedchain.config.vector_db.opensearch.OpenSearchDBConfig",  # OpenSearch 配置类
        "lancedb": "embedchain.config.vector_db.lancedb.LanceDBConfig",  # LanceDB 配置类
        "pinecone": "embedchain.config.vector_db.pinecone.PineconeDBConfig",  # Pinecone 配置类
        "qdrant": "embedchain.config.vector_db.qdrant.QdrantDBConfig",  # Qdrant 配置类
        "weaviate": "embedchain.config.vector_db.weaviate.WeaviateDBConfig",  # Weaviate 配置类
        "zilliz": "embedchain.config.vector_db.zilliz.ZillizDBConfig",  # Zilliz 配置类
    }

    # 这也是一个类方法，用于创建一个向量数据库实例
    @classmethod
    def create(cls, provider_name, config_data):
        # 根据提供的服务名字 `provider_name`，从 `provider_to_class` 字典中找到对应的类名
        class_type = cls.provider_to_class.get(provider_name)
        # 根据 `provider_name` 找到对应的配置类名
        config_class_type = cls.provider_to_config_class.get(provider_name)
        # 如果找到了对应的类名
        if class_type:
            # 使用 `load_class` 函数加载这个类名对应的类
            embedder_class = load_class(class_type)
            # 加载配置类
            embedder_config_class = load_class(config_class_type)
            # 创建并返回一个向量数据库实例，传入配置数据
            return embedder_class(config=embedder_config_class(**config_data))
        else:
            # 如果没有找到对应的类名，抛出一个错误，告诉用户这个服务名字不支持
            raise ValueError(f"Unsupported Embedder provider: {provider_name}")

