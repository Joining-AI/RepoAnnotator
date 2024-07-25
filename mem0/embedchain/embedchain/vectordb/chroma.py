# 导入日志模块，用于记录程序运行过程中的信息。
import logging
# 导入类型提示相关的模块，用于给变量添加类型注释，让代码更易理解。
from typing import Any, Optional, Union

# 从 chromadb 这个库中导入 Collection 和 QueryResult 类，它们是用来操作数据集合和查询结果的。
from chromadb import Collection, QueryResult
# 导入 Document 类，这个类是用来表示文档的。
from langchain.docstore.document import Document
# 导入 tqdm 模块，它可以帮助我们在循环中显示进度条。
from tqdm import tqdm

# 导入 ChromaDbConfig 类，这个类包含了 ChromaDB 数据库的一些配置选项。
from embedchain.config import ChromaDbConfig
# 导入一个装饰器，用来标记一个类可以被序列化成 JSON 格式。
from embedchain.helpers.json_serializable import register_deserializable
# 导入一个基类 BaseVectorDB，它是所有向量数据库实现的基础类。
from embedchain.vectordb.base import BaseVectorDB

# 尝试直接导入 chromadb 库及其相关组件。
try:
    import chromadb
    from chromadb.config import Settings
    # 导入一个异常类，当向量维度不正确时会被抛出。
    from chromadb.errors import InvalidDimensionException
# 如果尝试直接导入失败（可能是因为缺少依赖），则使用一个备用方法来解决依赖问题。
except RuntimeError:
    # 导入一个辅助函数，用来确保可以使用 pysqlite3 作为 sqlite3 的替代品。
    from embedchain.utils.misc import use_pysqlite3
    # 使用备用方法确保可以导入 chromadb 及其相关组件。
    use_pysqlite3()
    import chromadb
    from chromadb.config import Settings
    # 再次导入异常类，这次是在使用了备用方法后。
    from chromadb.errors import InvalidDimensionException

# 创建一个日志记录器，用于记录与 ChromaDB 相关的信息。
logger = logging.getLogger(__name__)

# 使用装饰器标记一个类，表示它可以被序列化成 JSON 格式。
@register_deserializable

class ChromaDB(BaseVectorDB):  # 定义ChromaDB类，继承自BaseVectorDB
    """Vector database using ChromaDB."""  # 这个类是使用ChromaDB的向量数据库

    def __init__(self, config: Optional[ChromaDbConfig] = None):  # 初始化方法，接收配置参数
        """Initialize a new ChromaDB instance  # 初始化一个新的ChromaDB实例
        :param config: Configuration options for Chroma, defaults to None  # 配置选项，如果没有提供默认为None
        :type config: Optional[ChromaDbConfig], optional  # 类型是可选的ChromaDbConfig
        """
        if config:  # 如果提供了配置
            self.config = config  # 使用提供的配置
        else:  # 否则
            self.config = ChromaDbConfig()  # 使用默认的ChromaDbConfig配置

        self.settings = Settings(anonymized_telemetry=False)  # 设置匿名遥测为False
        self.settings.allow_reset = self.config.allow_reset if hasattr(self.config, "allow_reset") else False  # 是否允许重置数据库
        self.batch_size = self.config.batch_size  # 批处理大小

        if self.config.chroma_settings:  # 如果有额外的Chroma设置
            for key, value in self.config.chroma_settings.items():  # 遍历这些设置
                if hasattr(self.settings, key):  # 如果设置中存在这个键
                    setattr(self.settings, key, value)  # 更新设置

        if self.config.host and self.config.port:  # 如果提供了主机和端口
            logger.info(f"Connecting to ChromaDB server: {self.config.host}:{self.config.port}")  # 日志记录连接信息
            self.settings.chroma_server_host = self.config.host  # 设置服务器主机
            self.settings.chroma_server_http_port = self.config.port  # 设置服务器HTTP端口
            self.settings.chroma_api_impl = "chromadb.api.fastapi.FastAPI"  # 设置API实现方式
        else:  # 否则（没有提供主机和端口）
            if self.config.dir is None:  # 如果没有提供目录
                self.config.dir = "db"  # 使用默认目录'db'
            self.settings.persist_directory = self.config.dir  # 设置持久化目录
            self.settings.is_persistent = True  # 设置为持久化模式

        self.client = chromadb.Client(self.settings)  # 创建ChromaDB客户端
        super().__init__(config=self.config)  # 调用父类初始化方法

    def _initialize(self):  # 初始化方法
        """
        This method is needed because `embedder` attribute needs to be set externally before it can be initialized.  # 这个方法需要在外部设置`embedder`属性后才能初始化
        """
        if not self.embedder:  # 如果没有嵌入器
            raise ValueError(  # 抛出错误
                "Embedder not set. Please set an embedder with `_set_embedder()` function before initialization."  # 错误信息：初始化前请设置嵌入器
            )
        self._get_or_create_collection(self.config.collection_name)  # 获取或创建集合

    def _get_or_create_db(self):  # 获取或创建数据库方法
        """Called during initialization"""  # 在初始化时调用
        return self.client  # 返回客户端

    @staticmethod
    def _generate_where_clause(where: dict[str, any]) -> dict[str, any]:  # 生成查询条件方法
        # 如果只有一个过滤器，直接返回
        if where is None:  # 如果where为空
            return {}  # 返回空字典
        if len(where.keys()) <= 1:  # 如果where字典长度小于等于1
            return where  # 直接返回where
        where_filters = []  # 创建过滤器列表
        for k, v in where.items():  # 遍历where字典
            if isinstance(v, str):  # 如果值是字符串
                where_filters.append({k: v})  # 添加到过滤器列表
        return {"$and": where_filters}  # 返回复合过滤器

    def _get_or_create_collection(self, name: str) -> Collection:  # 获取或创建集合方法
        """
        Get or create a named collection.  # 获取或创建命名集合
        :param name: Name of the collection  # 集合名称
        :type name: str  # 类型为字符串
        :raises ValueError: No embedder configured.  # 如果没有配置嵌入器抛出错误
        :return: Created collection  # 返回创建的集合
        :rtype: Collection  # 返回类型为Collection
        """
        if not hasattr(self, "embedder") or not self.embedder:  # 如果没有嵌入器
            raise ValueError("Cannot create a Chroma database collection without an embedder.")  # 抛出错误
        self.collection = self.client.get_or_create_collection(  # 获取或创建集合
            name=name,  # 名称
            embedding_function=self.embedder.embedding_fn,  # 嵌入函数
        )
        return self.collection  # 返回集合

    def get(self, ids: Optional[list[str]] = None, where: Optional[dict[str, any]] = None, limit: Optional[int] = None):  # 获取方法
        """
        Get existing doc ids present in vector database  # 获取向量数据库中存在的文档ID
        :param ids: list of doc ids to check for existence  # 文档ID列表
        :type ids: list[str]  # 类型为字符串列表
        :param where: Optional. to filter data  # 可选的过滤数据
        :type where: dict[str, Any]  # 类型为字典
        :param limit: Optional. maximum number of documents  # 最大文档数量
        :type limit: Optional[int]  # 类型为整数，可选
        :return: Existing documents.  # 返回存在的文档
        :rtype: list[str]  # 返回类型为字符串列表
        """
        args = {}  # 创建参数字典
        if ids:  # 如果有ids
            args["ids"] = ids  # 添加ids到参数字典
        if where:  # 如果有where
            args["where"] = self._generate_where_clause(where)  # 添加过滤条件
        if limit:  # 如果有限制
            args["limit"] = limit  # 添加限制
        return self.collection.get(**args)  # 根据参数获取数据

    def add(  # 添加数据方法
        self,
        documents: list[str],  # 文档列表
        metadatas: list[object],  # 元数据列表
        ids: list[str],  # ID列表
    ) -> Any:  # 返回任意类型
        """
        Add vectors to chroma database  # 向Chroma数据库添加向量
        :param documents: Documents  # 文档
        :type documents: list[str]  # 类型为字符串列表
        :param metadatas: Metadatas  # 元数据
        :type metadatas: list[object]  # 类型为对象列表
        :param ids: ids  # ID
        :type ids: list[str]  # 类型为字符串列表
        """
        size = len(documents)  # 获取文档列表长度
        if len(documents) != size or len(metadatas) != size or len(ids) != size:  # 检查长度是否一致
            raise ValueError(  # 如果不一致，抛出错误
                "Cannot add documents to chromadb with inconsistent sizes. Documents size: {}, Metadata size: {}, Ids size: {}".format(  # 错误信息
                    len(documents), len(metadatas), len(ids)  # 提供详细信息
                )
            )

        for i in tqdm(range(0, len(documents), self.batch_size), desc="Inserting batches in chromadb"):  # 批量插入
            self.collection.add(  # 添加数据
                documents=documents[i : i + self.batch_size],  # 文档切片
                metadatas=metadatas[i : i + self.batch_size],  # 元数据切片
                ids=ids[i : i + self.batch_size],  # ID切片
            )
        self.config  # 访问配置

    @staticmethod
    def _format_result(results: QueryResult) -> list[tuple[Document, float]]:  # 格式化结果方法
        """
        Format Chroma results  # 格式化Chroma结果
        :param results: ChromaDB query results to format.  # 待格式化的ChromaDB查询结果
        :type results: QueryResult  # 类型为QueryResult
        :return: Formatted results  # 格式化后的结果
        :rtype: list[tuple[Document, float]]  # 返回类型为文档和浮点数的元组列表
        """
        return [  # 返回列表
            (  # 元组
                Document(page_content=result[0], metadata=result[1] or {}),  # 文档内容和元数据
                result[2]  # 结果距离
            )
            for result in zip(  # 对结果进行组合
                results["documents"][0],  # 文档
                results["metadatas"][0],  # 元数据
                results["distances"][0],  # 距离
            )
        ]

    def query(  # 查询方法
        self,
        input_query: str,  # 输入查询
        n_results: int,  # 结果数量
        where: Optional[dict[str, any]] = None,  # 过滤条件
        raw_filter: Optional[dict[str, any]] = None,  # 原始过滤
        citations: bool = False,  # 引用标志
        **kwargs: Optional[dict[str, any]],  # 其他参数
    ) -> Union[list[tuple[str, dict]], list[str]]:  # 返回类型
        """
        Query contents from vector database based on vector similarity  # 根据向量相似性从向量数据库中查询内容
        :param input_query: query string  # 查询字符串
        :type input_query: str  # 类型为字符串
        :param n_results: no of similar documents to fetch from database  # 从数据库获取的类似文档数量
        :type n_results: int  # 类型为整数
        :param where: to filter data  # 过滤数据
        :type where: dict[str, Any]  # 类型为字典
        :param raw_filter: Raw filter to apply  # 应用原始过滤
        :type raw_filter: dict[str, Any]  # 类型为字典
        :param citations: we use citations boolean param to return context along with the answer.  # 引用布尔参数用于返回上下文和答案
        :type citations: bool, default is False.  # 类型为布尔，缺省为False
        :raises InvalidDimensionException: Dimensions do not match.  # 维度不匹配时抛出错误
        :return: The content of the document that matched your query,  # 匹配查询的文档内容
        along with url of the source and doc_id (if citations flag is true)  # 如果引用标志为真，则返回源URL和doc_id
        :rtype: list[str], if citations=False, otherwise list[tuple[str, str, str]]  # 返回类型
        """
        if where and raw_filter:  # 如果同时有where和raw_filter
            raise ValueError("Both `where` and `raw_filter` cannot be used together.")  # 抛出错误

        where_clause = {}  # 创建过滤条件字典
        if raw_filter:  # 如果有原始过滤
            where_clause = raw_filter  # 使用原始过滤
        if where:  # 如果有where
            where_clause = self._generate_where_clause(where)  # 生成过滤条件

        try:  # 尝试
            result = self.collection.query(  # 查询集合
                query_texts=[  # 查询文本
                    input_query,  # 输入查询
                ],
                n_results=n_results,  # 结果数量
                where=where_clause,  # 过滤条件
            )
        except InvalidDimensionException as e:  # 如果出现维度错误
            raise InvalidDimensionException(  # 抛出错误
                e.message()  # 错误消息
                + ". This is commonly a side-effect when an embedding function, different from the one used to add the embeddings, is used to retrieve an embedding from the database."  # 补充说明
            ) from None  # 不捕获异常

        results_formatted = self._format_result(result)  # 格式化结果
        contexts = []  # 创建上下文列表
        for result in results_formatted:  # 遍历格式化结果
            context = result[0].page_content  # 上下文内容
            if citations:  # 如果引用标志为真
                metadata = result[0].metadata  # 元数据
                metadata["score"] = result[1]  # 分数
                contexts.append((context, metadata))  # 添加到上下文列表
            else:  # 否则
                contexts.append(context)  # 添加上下文内容
        return contexts  # 返回上下文列表

    def set_collection_name(self, name: str):  # 设置集合名称方法
        """
        Set the name of the collection. A collection is an isolated space for vectors.  # 设置集合名称，集合是向量的隔离空间
        :param name: Name of the collection.  # 集合名称
        :type name: str  # 类型为字符串
        """
        if not isinstance(name, str):  # 如果名称不是字符串
            raise TypeError("Collection name must be a string")  # 抛出类型错误
        self.config.collection_name = name  # 设置集合名称
        self._get_or_create_collection(self.config.collection_name)  # 获取或创建集合

    def count(self) -> int:  # 计数方法
        """
        Count number of documents/chunks embedded in the database.  # 计算数据库中嵌入的文档/块数量
        :return: number of documents  # 文档数量
        :rtype: int  # 类型为整数
        """
        return self.collection.count()  # 返回集合中的计数

    def delete(self, where):  # 删除方法
        return self.collection.delete(where=self._generate_where_clause(where))  # 删除符合条件的数据

    def reset(self):  # 重置方法
        """
        Resets the database. Deletes all embeddings irreversibly.  # 重置数据库，不可逆地删除所有嵌入
        """
        # Delete all data from the collection  # 从集合中删除所有数据
        try:  # 尝试
            self.client.delete_collection(self.config.collection_name)  # 删除集合
        except ValueError:  # 如果出现值错误
            raise ValueError(  # 抛出错误
                "For safety reasons, resetting is disabled. Please enable it by setting `allow_reset=True` in your ChromaDbConfig"  # 错误信息：为了安全原因，重置被禁用，请在您的ChromaDbConfig中设置`allow_reset=True`
            ) from None  # 不捕获异常
        # Recreate  # 重新创建
        self._get_or_create_collection(self.config.collection_name)  # 获取或创建集合

# Todo: Automatically recreating a collection with the same name cannot be the best way to handle a reset.
# 这里说，当需要重置（比如清空并重新创建）一个数据库里的集合时，
# 直接用同一个名字自动重建这个集合可能不是最好的办法。
# 就像是你把乐高城堡拆了再用同样方式重建，但可能有更好的方法去清理和开始新游戏。

# A downside of this implementation is, if you have two instances,
# 如果你有两份这样的“乐高城堡”实例（就像是两个游戏存档），
# the other instance will not get the updated `self.collection` attribute.
# 当你在一个实例中重置了集合后，另一个实例中的集合不会被更新。
# 就好像你在第一个存档里重置了城堡，但第二个存档里的城堡还是老样子。

# A better way would be to create the collection if it is called again after being reset.
# 更好的方法是，在重置后如果再次调用这个集合，
# 应该检查集合是否还在，不在的话就创建它。
# 就像是如果你发现城堡被拆了，应该先检查一下，没有了就再建一个。

# That means, checking if collection exists in the db-consuming methods, and creating it if it doesn't.
# 这意味着在所有使用数据库的方法里，都应该先检查集合是否存在，不存在就创建。
# 就像每次玩游戏前都检查一下城堡是不是还在，不在就造一个。

# That's an extra steps for all uses, just to satisfy a niche use case in a niche method.
# 这样做对所有使用情况来说都是额外的步骤，仅仅是为了满足一个特殊方法里的特殊需求。
# 就像是为了一个偶尔才玩的游戏模式，让所有玩家每次都要多做一步检查。

# For now, this will do.
# 不过，目前这样先凑合着用吧。

