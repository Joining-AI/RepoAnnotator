# 这行代码是引入了一个叫做"Optional"的工具，它可以帮助我们在写代码时，告诉别人某个东西可以存在，也可以不存在。
from typing import Optional

# 这里引入了两个类：BaseEmbedderConfig 和 register_deserializable，就像是拿出了两本不同的故事书。
from embedchain.config.embedder.base import BaseEmbedderConfig
from embedchain.helpers.json_serializable import register_deserializable

