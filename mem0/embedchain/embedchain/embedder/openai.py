# 导入操作系统相关的功能，这里可能会用到环境变量。
import os
# 导入类型提示中的Optional，用于表示某个参数可以是某种类型，也可以是None。
from typing import Optional
# 导入OpenAIEmbeddingFunction类，这个类是用来生成文本嵌入向量的。
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
# 导入BaseEmbedderConfig类，这是配置类的基础。
from embedchain.config import BaseEmbedderConfig
# 导入BaseEmbedder类，这是嵌入器类的基础。
from embedchain.embedder.base import BaseEmbedder
# 导入VectorDimensions枚举类，它定义了不同模型对应的向量维度。
from embedchain.models import VectorDimensions

# 定义一个名为OpenAIEmbedder的新类，它继承自BaseEmbedder。
class OpenAIEmbedder(BaseEmbedder):
    # 这个类的构造函数，也就是创建对象时会自动调用的方法。
    def __init__(self, config: Optional[BaseEmbedderConfig] = None):
        # 调用父类BaseEmbedder的构造函数。
        super().__init__(config=config)

        # 如果没有指定模型名称，默认设置为"text-embedding-ada-002"。
        if self.config.model is None:
            self.config.model = "text-embedding-ada-002"

        # 获取API密钥，优先从配置中获取，如果没有则从环境变量中获取。
        api_key = self.config.api_key or os.environ["OPENAI_API_KEY"]
        # 获取API的基本地址，优先从配置中获取，如果没有则尝试从环境变量中获取。
        api_base = self.config.api_base or os.environ.get("OPENAI_API_BASE")

        # 检查是否提供了API密钥或组织ID，如果都没有提供，则抛出错误。
        if api_key is None and os.getenv("OPENAI_ORGANIZATION") is None:
            raise ValueError("OPENAI_API_KEY or OPENAI_ORGANIZATION 环境变量未提供")
        
        # 创建OpenAIEmbeddingFunction对象，传入所需的API密钥、基本地址、组织ID和模型名称。
        embedding_fn = OpenAIEmbeddingFunction(
            api_key=api_key,
            api_base=api_base,
            organization_id=os.getenv("OPENAI_ORGANIZATION"),
            model_name=self.config.model,
        )
        # 设置嵌入函数。
        self.set_embedding_fn(embedding_fn=embedding_fn)
        # 设置向量维度，优先从配置中获取，如果没有则使用默认值。
        vector_dimension = self.config.vector_dimension or VectorDimensions.OPENAI.value
        self.set_vector_dimension(vector_dimension=vector_dimension)

