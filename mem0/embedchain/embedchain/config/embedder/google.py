# 首先，我们要从魔法工具箱里拿出一些必要的工具。
from typing import Optional  # 这个工具帮助我们指定一些东西可能是有，也可能是什么都没有。

from embedchain.config.embedder.base import BaseEmbedderConfig  # 这是我们的基础魔法配方，所有魔法助手的基础。
from embedchain.helpers.json_serializable import register_deserializable  # 这个工具让我们的魔法助手可以被魔法书记住和重现。

# 现在，我们要创造一个叫做GoogleAIEmbedderConfig的新魔法助手，它继承了BaseEmbedderConfig的基础魔法。
@register_deserializable  # 这个装饰符就像一个魔法标记，告诉魔法书要记住这个魔法助手。
class GoogleAIEmbedderConfig(BaseEmbedderConfig):  # 我们定义了新魔法助手的名字和它的父母魔法。

    # 下面是魔法助手的诞生仪式，我们给它一些初始的力量。
    def __init__(self,  # 这是魔法助手的出生仪式，我们给它一些重要的力量。
        self,  # 这是我们正在创造的魔法助手自己。
        model: Optional[str] = None,  # 这是模型，可能有名字，也可能没有。
        deployment_name: Optional[str] = None,  # 这是部署的名字，可能有，也可能没有。
        vector_dimension: Optional[int] = None,  # 这是向量的维度，可能有数字，也可能没有。
        task_type: Optional[str] = None,  # 这是任务类型，可能有类型名，也可能没有。
        title: Optional[str] = None,  # 这是标题，可能有，也可能没有。
    ):
        # 我们首先调用父母的诞生仪式，给它一些基础的力量。
        super().__init__(model, deployment_name, vector_dimension)

        # 然后，我们给它一些额外的力量。
        self.task_type = task_type or "retrieval_document"  # 如果没有任务类型，就默认是检索文档。
        self.title = title or "Embeddings for Embedchain"  # 如果没有标题，就默认是“Embedchain的嵌入”。

