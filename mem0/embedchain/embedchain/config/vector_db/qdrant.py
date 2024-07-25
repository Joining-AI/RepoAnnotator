# 这里我们从typing模块导入了Optional，这是一个特殊的类型提示，意味着某些参数可以是None。
from typing import Optional

# 我们从embedchain.config.vector_db.base模块导入BaseVectorDbConfig类，
# 这个类是用来配置向量数据库的基础设置的。
from embedchain.config.vector_db.base import BaseVectorDbConfig

# 我们还从embedchain.helpers.json_serializable模块导入register_deserializable装饰器，
# 这个装饰器可以让我们的类支持序列化和反序列化，简单来说就是可以更容易地保存和读取类的实例。
from embedchain.helpers.json_serializable import register_deserializable


# 使用上面提到的装饰器，我们定义了一个新的类QdrantDBConfig，
# 这个类继承自BaseVectorDbConfig，专门用来配置qdrant数据库的客户端。
@register_deserializable
class QdrantDBConfig(BaseVectorDbConfig):
    # 这是类的文档字符串，用来说明这个类是干什么的。
    """
    这个类是用来初始化一个qdrant数据库客户端的配置。
    它需要一个参数url，这个url可以是单个qdrant服务器的地址，也可以是一系列服务器地址的列表。
    """

    # 这是类的构造函数，当我们创建这个类的一个实例时，它就会被调用。
    def __init__(
        self,
        collection_name: Optional[str] = None,  # 这是可选的参数，用来指定默认的集合名称。
        dir: Optional[str] = None,             # 这也是可选的，用来指定数据库存储的目录路径。
        hnsw_config: Optional[dict[str, any]] = None,  # 可选参数，用于HNSW索引的配置。
        quantization_config: Optional[dict[str, any]] = None,  # 可选参数，用于量化配置，如果为None，则禁用量化。
        on_disk: Optional[bool] = None,       # 可选参数，如果为True，则数据不会存放在内存中，而是每次请求时从磁盘读取。
        batch_size: Optional[int] = 10,       # 可选参数，指定一次批量插入的数据项数量，默认是10。
        **extra_params: dict[str, any],       # 这是一个可变参数字典，可以接收任意多的额外参数。
    ):
        # 下面的这些行代码，是在设置类的实例变量。
        self.hnsw_config = hnsw_config
        self.quantization_config = quantization_config
        self.on_disk = on_disk
        self.batch_size = batch_size
        self.extra_params = extra_params

        # 最后，我们调用了父类BaseVectorDbConfig的构造函数，并传递了一些必要的参数。
        # 这样，我们可以复用父类的一些通用功能。
        super().__init__(collection_name=collection_name, dir=dir)

