# 导入需要的模块
from typing import Optional  # 这行代码是导入了可选类型的功能，这样可以让其他程序员更容易理解代码里的参数可以是空值。
from langchain_community.embeddings import AzureOpenAIEmbeddings  # 导入了Azure OpenAI服务中用于生成向量的类。
from embedchain.config import BaseEmbedderConfig  # 导入了一个配置基类，用于设置一些默认配置。
from embedchain.embedder.base import BaseEmbedder  # 导入了一个基础的嵌入器类，我们的新类会继承这个类。
from embedchain.models import VectorDimensions  # 导入了一个枚举类，里面包含了不同模型的向量维度。

# 定义了一个新的类 `AzureOpenAIEmbedder`，它继承自 `BaseEmbedder`
class AzureOpenAIEmbedder(BaseEmbedder):
    # 初始化方法，每个类都会有一个初始化方法，用于创建类的新实例时设置一些初始状态。
    def __init__(self, config: Optional[BaseEmbedderConfig] = None):
        # 调用父类 `BaseEmbedder` 的初始化方法，设置一些基本配置。
        super().__init__(config=config)

        # 如果没有指定模型名称，默认使用 "text-embedding-ada-002" 这个模型。
        if self.config.model is None:
            self.config.model = "text-embedding-ada-002"

        # 创建一个 `AzureOpenAIEmbeddings` 对象，这个对象可以帮助我们把文本转换成向量。
        embeddings = AzureOpenAIEmbeddings(deployment=self.config.deployment_name)
        
        # 使用 `_langchain_default_concept` 方法来获取一个函数，这个函数可以接受文本并返回它的向量表示。
        embedding_fn = BaseEmbedder._langchain_default_concept(embeddings)

        # 设置 `embedding_fn` 为当前对象的嵌入函数。
        self.set_embedding_fn(embedding_fn=embedding_fn)
        
        # 设置向量的维度。如果在配置里没有指定，就使用 `VectorDimensions.OPENAI.value` 的值。
        vector_dimension = self.config.vector_dimension or VectorDimensions.OPENAI.value
        self.set_vector_dimension(vector_dimension=vector_dimension)

