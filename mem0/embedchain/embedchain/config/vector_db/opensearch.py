# 导入一些需要的模块
from typing import Optional  # 用于声明某些变量可以是特定类型或 None
from embedchain.config.vector_db.base import BaseVectorDbConfig  # 基础配置类
from embedchain.helpers.json_serializable import register_deserializable  # 装饰器，用于标记类以便后续序列化

# 使用装饰器标记这个类，表示它可以被序列化成 JSON 格式
@register_deserializable
class OpenSearchDBConfig(BaseVectorDbConfig):  # 定义一个继承自 BaseVectorDbConfig 的新类
    def __init__(self,  # 这个类的初始化方法
                 opensearch_url: str,  # OpenSearch 的地址，比如 "http://localhost:9200"
                 http_auth: tuple[str, str],  # 登录 OpenSearch 的用户名和密码组成的元组
                 vector_dimension: int = 1536,  # 向量的维度，默认是 1536
                 collection_name: Optional[str] = None,  # 集合（相当于数据库中的表）的名字，如果没有提供，则默认为 None
                 dir: Optional[str] = None,  # 数据库文件所在的目录路径，如果没有提供，则默认为 None
                 batch_size: Optional[int] = 100,  # 每次批量插入多少条数据，默认是 100 条
                 **extra_params: dict[str, any],  # 其他额外的参数，以字典形式传递
                 ):
        # 设置 OpenSearch 的地址
        self.opensearch_url = opensearch_url
        # 设置登录凭证
        self.http_auth = http_auth
        # 设置向量的维度
        self.vector_dimension = vector_dimension
        # 设置额外的参数
        self.extra_params = extra_params
        # 设置每次批量插入的数量
        self.batch_size = batch_size

        # 调用父类的初始化方法，传入集合名字和数据库目录
        super().__init__(collection_name=collection_name, dir=dir)

