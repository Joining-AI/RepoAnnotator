# 导入需要的库和模块，让我们的代码能够使用这些库的功能。
from typing import Optional

# 这两行是引入了一些配置类和模型维度的定义，用来设置我们的文字转数字机器人的参数。
from embedchain.config import BaseEmbedderConfig
from embedchain.embedder.base import BaseEmbedder
from embedchain.models import VectorDimensions


# 定义了一个新的类叫做 GPT4AllEmbedder，继承自 BaseEmbedder，这个类就是我们要创建的文字转数字机器人。
class GPT4AllEmbedder(BaseEmbedder):
    # 这个是类的构造函数，当我们创建一个新的 GPT4AllEmbedder 实例时，就会自动运行这部分代码。
    def __init__(self, config: Optional[BaseEmbedderConfig] = None):
        # 调用父类 BaseEmbedder 的构造函数，设置一些基本配置。
        super().__init__(config=config)

        # 从另一个库中导入我们需要的模型，这个模型可以帮助我们把文字转换成数字。
        from langchain_community.embeddings import GPT4AllEmbeddings as LangchainGPT4AllEmbeddings

        # 设置模型的名字，默认是 "all-MiniLM-L6-v2-f16.gguf"，这就像选择一种特别的工具来帮助我们转换文字。
        model_name = self.config.model or "all-MiniLM-L6-v2-f16.gguf"
        # 设置模型的一些参数，这里允许下载模型文件。
        gpt4all_kwargs = {'allow_download': 'True'}
        # 使用上面设定的模型名和参数创建一个实际的模型实例。
        embeddings = LangchainGPT4AllEmbeddings(model_name=model_name, gpt4all_kwargs=gpt4all_kwargs)
        # 把模型实例包装成我们自己的格式，这样就可以在我们的系统里使用了。
        embedding_fn = BaseEmbedder._langchain_default_concept(embeddings)
        # 设置我们刚刚准备好的模型实例为我们机器人的一部分。
        self.set_embedding_fn(embedding_fn=embedding_fn)

        # 设置转换后数字的维度（长度），默认是根据 GPT4All 来的。
        vector_dimension = self.config.vector_dimension or VectorDimensions.GPT4ALL.value
        # 最后一步，设置好数字的维度，这样我们就完成了文字转数字机器人的配置。
        self.set_vector_dimension(vector_dimension=vector_dimension)

