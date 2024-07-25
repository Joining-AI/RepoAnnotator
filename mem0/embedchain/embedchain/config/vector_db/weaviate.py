# 这行是从一个叫做 "typing" 的工具包里拿出 "Optional" 这个工具。
from typing import Optional

# 这行是从 "embedchain.config.vector_db.base" 这个地方拿出 "BaseVectorDbConfig" 类。
from embedchain.config.vector_db.base import BaseVectorDbConfig

# 这行是从 "embedchain.helpers.json_serializable" 拿出 "register_deserializable" 这个装饰器。
from embedchain.helpers.json_serializable import register_deserializable

# 这行是在说：用 "@register_deserializable" 这个装饰器，把接下来定义的 "WeaviateDBConfig" 类做一些特别的标记，
# 这样其他部分的代码就知道这个类有一些特殊的功能。
@register_deserializable

# 这行是开始定义一个新的类 "WeaviateDBConfig"，它继承自 "BaseVectorDbConfig"。
class WeaviateDBConfig(BaseVectorDbConfig):

    # 这行是定义 "WeaviateDBConfig" 类的构造函数（就是创建这个类的新对象时会自动运行的函数）。
    def __init__(
        self,

        # 这行是说这个构造函数需要一个叫做 "collection_name" 的参数，默认值是 "None"。
        collection_name: Optional[str] = None,

        # 这行是说还需要一个叫做 "dir" 的参数，默认值也是 "None"。
        dir: Optional[str] = None,

        # 这行是说需要一个叫做 "batch_size" 的参数，默认值是 100。
        batch_size: Optional[int] = 100,

        # 这行是说还需要一个叫 "**extra_params" 的参数，它可以接收任意数量的键值对（字典形式）。
        **extra_params: dict[str, any],
    ):

        # 这行是设置 "self.batch_size" 属性等于传入的 "batch_size" 参数。
        self.batch_size = batch_size

        # 这行是设置 "self.extra_params" 属性等于传入的 "**extra_params" 参数。
        self.extra_params = extra_params

        # 这行是调用父类 "BaseVectorDbConfig" 的构造函数，并传递 "collection_name" 和 "dir" 参数。
        # 这样可以确保父类的一些初始化工作也能完成。
        super().__init__(collection_name=collection_name, dir=dir)

