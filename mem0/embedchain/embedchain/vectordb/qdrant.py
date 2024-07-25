# 导入copy模块，这个模块里有一些函数可以用来复制对象。
import copy

# 导入os模块，这个模块里有很多和操作系统交互的功能。
import os

# 导入typing模块里的Any、Optional和Union类，这些可以帮助我们更好地定义变量类型。
from typing import Any, Optional, Union

# 尝试导入qdrant_client模块及其子模块里的类和函数，这些是用来操作Qdrant数据库的工具。
try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    from qdrant_client.http.models import Batch
    from qdrant_client.models import Distance, VectorParams
except ImportError:
    # 如果上面的导入失败了（也就是用户没有安装qdrant_client库），就抛出ImportError异常，
    # 并告诉用户需要安装额外的依赖，可以通过pip命令安装。
    raise ImportError("Qdrant requires extra dependencies. Install with `pip install embedchain[qdrant]`") from None

# 导入tqdm模块，这个模块可以用来显示进度条，让程序看起来更友好。
from tqdm import tqdm

# 导入embedchain项目里的QdrantDBConfig类，这个类用来配置Qdrant数据库的一些选项。
from embedchain.config.vector_db.qdrant import QdrantDBConfig

# 导入embedchain项目里的BaseVectorDB类，这是个基础类，用来处理向量数据库的基本操作。
from embedchain.vectordb.base import BaseVectorDB

class QdrantDB(BaseVectorDB):  # 定义QdrantDB类，继承自BaseVectorDB
    """
    Qdrant作为向量数据库
    """

    def __init__(self, config: QdrantDBConfig = None):  # 初始化方法
        """
        使用Qdrant作为向量数据库
        :param config: 连接时使用的Qdrant数据库配置
        """
        if config is None:  # 如果没有提供配置，则创建一个默认配置
            config = QdrantDBConfig()
        else:  # 如果提供了配置，检查其类型是否正确
            if not isinstance(config, QdrantDBConfig):
                raise TypeError(  # 如果类型错误，抛出异常
                    "config不是`QdrantDBConfig`实例。"
                    "请确保类型正确并且传递的是实例。"
                )
        self.config = config  # 设置配置属性
        self.batch_size = self.config.batch_size  # 设置批次大小
        self.client = QdrantClient(  # 创建Qdrant客户端
            url=os.getenv("QDRANT_URL"),  # 从环境变量获取URL
            api_key=os.getenv("QDRANT_API_KEY")  # 从环境变量获取API密钥
        )
        # 在这里调用父类的初始化方法，因为需要设置embedder属性
        super().__init__(config=self.config)

    def _initialize(self):  # 私有方法，用于初始化
        """
        此方法是必要的，因为`embedder`属性在初始化前需要外部设置。
        """
        if not self.embedder:  # 检查embedder是否已设置
            raise ValueError("Embedder未设置。"
                             "请在初始化前使用`set_embedder`设置一个embedder。")

        self.collection_name = self._get_or_create_collection()  # 获取或创建集合名称
        all_collections = self.client.get_collections()  # 获取所有集合
        collection_names = [collection.name for collection in all_collections.collections]  # 提取集合名称列表
        if self.collection_name not in collection_names:  # 如果当前集合不存在于列表中
            self.client.recreate_collection(  # 重新创建集合
                collection_name=self.collection_name,  # 集合名称
                vectors_config=VectorParams(  # 向量配置
                    size=self.embedder.vector_dimension,  # 向量维度
                    distance=Distance.COSINE,  # 距离度量
                    hnsw_config=self.config.hnsw_config,  # HNSW配置
                    quantization_config=self.config.quantization_config,  # 量化配置
                    on_disk=self.config.on_disk,  # 是否存储在磁盘上
                ),
            )

    def _get_or_create_db(self):  # 私有方法，返回Qdrant客户端
        return self.client

    def _get_or_create_collection(self):  # 私有方法，生成集合名称
        return f"{self.config.collection_name}-{self.embedder.vector_dimension}".lower().replace("_", "-")

    def get(self, ids: Optional[list[str]] = None, where: Optional[dict[str, any]] = None, limit: Optional[int] = None):  # 获取数据
        """
        获取向量数据库中已存在的文档ID
        ...
        """
        # 这里省略了详细注释，这部分代码用于根据提供的ID、过滤条件和限制来获取数据库中的现有ID和元数据。

    def add(self, documents: list[str], metadatas: list[object], ids: list[str], **kwargs: Optional[dict[str, any]]):  # 添加数据
        """
        将数据添加到向量数据库
        ...
        """
        # 这里省略了详细注释，这部分代码将文本、元数据和ID添加到数据库中。

    def query(self, input_query: str, n_results: int, where: dict[str, any], citations: bool = False, **kwargs: Optional[dict[str, Any]]) -> Union[list[tuple[str, dict]], list[str]]:  # 查询数据
        """
        根据向量相似性查询向量数据库的内容
        ...
        """
        # 这里省略了详细注释，这部分代码用于根据查询字符串、结果数量、过滤条件和引用标志来检索匹配的文档内容。

    def count(self) -> int:  # 计数
        response = self.client.get_collection(collection_name=self.collection_name)  # 获取集合信息
        return response.points_count  # 返回点的数量

    def reset(self):  # 重置
        self.client.delete_collection(collection_name=self.collection_name)  # 删除集合
        self._initialize()  # 重新初始化

    def set_collection_name(self, name: str):  # 设置集合名称
        """
        设置集合的名称。集合是向量的隔离空间。
        ...
        """
        # 这里省略了详细注释，这部分代码用于设置或更改集合名称。

    @staticmethod
    def _generate_query(where: dict):  # 静态方法，生成查询
        must_fields = []  # 初始化必须字段列表
        for key, value in where.items():  # 遍历过滤条件字典
            must_fields.append(  # 将每个条件转换为FieldCondition对象并添加到列表中
                models.FieldCondition(
                    key=f"metadata.{key}",  # 元数据键
                    match=models.MatchValue(  # 匹配值
                        value=value,  # 条件值
                    ),
                )
            )
        return models.Filter(must=must_fields)  # 返回Filter对象

    def delete(self, where: dict):  # 删除数据
        db_filter = self._generate_query(where)  # 生成过滤器
        self.client.delete(  # 删除满足条件的数据
            collection_name=self.collection_name,  # 集合名称
            points_selector=db_filter  # 过滤器
        )

