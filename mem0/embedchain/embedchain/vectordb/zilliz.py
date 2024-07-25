import logging

class ZillizVectorDB(BaseVectorDB):  # 定义一个叫做 ZillizVectorDB 的类，它继承自 BaseVectorDB。
    """Base class for vector database."""  # 这是类的说明文档，说明这是一个向量数据库的基础类。

    def __init__(self, config: ZillizDBConfig = None):  # 定义构造函数，接受一个可选参数 config，类型为 ZillizDBConfig。
        """Initialize the database. Save the config and client as an attribute.  # 构造函数的说明文档，初始化数据库并保存配置和客户端信息。
        
        :param config: Database configuration class instance.  # 参数 config 是数据库配置类的一个实例。
        :type config: ZillizDBConfig  # 参数 config 的类型是 ZillizDBConfig。
        """

        if config is None:  # 如果没有传入配置信息，则创建一个新的 ZillizDBConfig 实例。
            self.config = ZillizDBConfig()  # 将新的配置实例赋值给 self.config。
        else:
            self.config = config  # 否则直接将传入的配置实例赋值给 self.config。

        self.client = MilvusClient(  # 创建一个 MilvusClient 客户端实例，并将其赋值给 self.client。
            uri=self.config.uri,  # 客户端的 URI 地址是从配置中获取的。
            token=self.config.token,  # 客户端的 token 也是从配置中获取的。
        )

        self.connection = connections.connect(  # 建立连接，并将其赋值给 self.connection。
            uri=self.config.uri,  # 连接的 URI 地址是从配置中获取的。
            token=self.config.token,  # 连接的 token 也是从配置中获取的。
        )

        super().__init__(config=self.config)  # 调用父类的构造函数，传入当前实例的配置信息。

    def _initialize(self):  # 定义一个私有方法（以下划线开头）叫做 _initialize。
        """
        This method is needed because `embedder` attribute needs to be set externally before it can be initialized.  # 方法说明文档，解释为什么需要这个方法。
        
        So it's can't be done in __init__ in one step.  # 不能在构造函数中一次性完成。
        """
        self._get_or_create_collection(self.config.collection_name)  # 调用另一个私有方法来获取或创建集合。

    def _get_or_create_db(self):  # 定义一个私有方法叫做 _get_or_create_db。
        """Get or create the database.  # 方法说明文档，说明这个方法用来获取或创建数据库。
        
        返回 self.client，即数据库客户端。
        """
        return self.client  # 返回数据库客户端。

    def _get_or_create_collection(self, name):  # 定义一个私有方法叫做 _get_or_create_collection，接受一个参数 name。
        """
        Get or create a named collection.  # 方法说明文档，说明这个方法用来获取或创建一个命名的集合。
        
        :param name: Name of the collection  # 参数 name 表示集合的名字。
        :type name: str  # 参数 name 的类型是字符串。
        """
        if utility.has_collection(name):  # 如果集合已经存在。
            logger.info(f"[ZillizDB]: found an existing collection {name}, make sure the auto-id is disabled.")  # 输出日志信息。
            self.collection = Collection(name)  # 获取已存在的集合。
        else:
            fields = [  # 如果集合不存在，则定义字段列表。
                FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=512),  # 定义主键字段。
                FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2048),  # 定义文本字段。
                FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=self.embedder.vector_dimension),  # 定义向量字段。
                FieldSchema(name="metadata", dtype=DataType.JSON),  # 定义元数据字段。
            ]

            schema = CollectionSchema(fields, enable_dynamic_field=True)  # 创建集合模式。
            self.collection = Collection(name=name, schema=schema)  # 创建集合。

            index = {  # 定义索引配置。
                "index_type": "AUTOINDEX",  # 索引类型。
                "metric_type": self.config.metric_type,  # 度量类型。
            }
            self.collection.create_index("embeddings", index)  # 在向量字段上创建索引。
        return self.collection  # 返回集合。

    def get(self, ids: Optional[list[str]] = None, where: Optional[dict[str, any]] = None, limit: Optional[int] = None):  # 定义 get 方法，接受三个可选参数 ids、where 和 limit。
        """
        Get existing doc ids present in vector database  # 方法说明文档，说明这个方法用来获取数据库中已有的文档 ID。
        
        :param ids: list of doc ids to check for existence  # 参数 ids 是要检查的文档 ID 列表。
        :type ids: list[str]  # 参数 ids 的类型是字符串列表。
        :param where: Optional. to filter data  # 参数 where 可选，用于过滤数据。
        :type where: dict[str, Any]  # 参数 where 的类型是字典。
        :param limit: Optional. maximum number of documents  # 参数 limit 可选，限制返回的最大文档数量。
        :type limit: Optional[int]  # 参数 limit 的类型是整数，可以为空。
        :return: Existing documents.  # 返回已存在的文档。
        :rtype: Set[str]  # 返回类型是字典。
        """
        data_ids = []  # 初始化文档 ID 列表。
        metadatas = []  # 初始化元数据列表。
        if self.collection.num_entities == 0 or self.collection.is_empty:  # 如果集合为空。
            return {"ids": data_ids, "metadatas": metadatas}  # 直接返回空的结果。

        filter_ = ""  # 初始化过滤条件字符串。
        if ids:  # 如果提供了文档 ID。
            filter_ = f'id in "{ids}"'  # 设置过滤条件。

        if where:  # 如果提供了过滤条件。
            if filter_:  # 如果已经有过滤条件了。
                filter_ += " and "  # 添加逻辑“与”。
            filter_ = f"{self._generate_zilliz_filter(where)}"  # 生成过滤条件。

        results = self.client.query(collection_name=self.config.collection_name, filter=filter_, output_fields=["*"])  # 查询数据。
        for res in results:  # 遍历查询结果。
            data_ids.append(res.get("id"))  # 提取文档 ID。
            metadatas.append(res.get("metadata", {}))  # 提取元数据。

        return {"ids": data_ids, "metadatas": metadatas}  # 返回文档 ID 和元数据。

    def add(  # 定义 add 方法，接受四个参数 documents、metadatas、ids 和 kwargs。
        self,
        documents: list[str],  # 文档列表。
        metadatas: list[object],  # 元数据列表。
        ids: list[str],  # 文档 ID 列表。
        **kwargs: Optional[dict[str, any]],  # 其他可选关键字参数。
    ):
        """Add to database  # 方法说明文档，说明这个方法用来添加数据到数据库。
        
        embeddings = self.embedder.embedding_fn(documents)  # 计算文档的向量表示。
        
        for id, doc, metadata, embedding in zip(ids, documents, metadatas, embeddings):  # 遍历每个文档及其相关数据。
            data = {"id": id, "text": doc, "embeddings": embedding, "metadata": metadata}  # 创建数据字典。
            self.client.insert(collection_name=self.config.collection_name, data=data, **kwargs)  # 插入数据。

        self.collection.load()  # 加载集合。
        self.collection.flush()  # 刷新集合。
        self.client.flush(self.config.collection_name)  # 刷新客户端。

    def query(  # 定义 query 方法，接受五个参数 input_query、n_results、where、citations 和 kwargs。
        self,
        input_query: str,  # 输入查询字符串。
        n_results: int,  # 查询结果的数量。
        where: dict[str, Any],  # 过滤条件。
        citations: bool = False,  # 是否返回引用，默认为 False。
        **kwargs: Optional[dict[str, Any]],  # 其他可选关键字参数。
    ) -> Union[list[tuple[str, dict]], list[str]]:  # 方法返回类型。
        """
        Query contents from vector database based on vector similarity  # 方法说明文档，说明这个方法用来根据向量相似度查询内容。
        
        :param input_query: query string  # 参数 input_query 是查询字符串。
        :type input_query: str  # 参数 input_query 的类型是字符串。
        :param n_results: no of similar documents to fetch from database  # 参数 n_results 是要从数据库获取的相似文档数量。
        :type n_results: int  # 参数 n_results 的类型是整数。
        :param where: to filter data  # 参数 where 用来过滤数据。
        :type where: dict[str, Any]  # 参数 where 的类型是字典。
        :raises InvalidDimensionException: Dimensions do not match.  # 如果维度不匹配会抛出异常。
        :param citations: we use citations boolean param to return context along with the answer.  # 参数 citations 用来控制是否返回上下文。
        :type citations: bool, default is False.  # 参数 citations 默认值为 False。
        :return: The content of the document that matched your query,  # 返回匹配查询的内容。
        along with url of the source and doc_id (if citations flag is true)  # 如果 citations 为真，则还返回来源 URL 和文档 ID。
        :rtype: list[str], if citations=False, otherwise list[tuple[str, str, str]]  # 返回类型。
        """

        if self.collection.is_empty:  # 如果集合为空。
            return []  # 直接返回空列表。

        output_fields = ["*"]  # 初始化输出字段列表。
        input_query_vector = self.embedder.embedding_fn([input_query])  # 计算查询字符串的向量表示。
        query_vector = input_query_vector[0]  # 获取查询向量。

        query_filter = self._generate_zilliz_filter(where)  # 生成过滤条件。
        query_result = self.client.search(  # 执行搜索。
            collection_name=self.config.collection_name,  # 指定集合名称。
            data=[query_vector],  # 搜索数据。
            filter=query_filter,  # 过滤条件。
            limit=n_results,  # 结果数量限制。
            output_fields=output_fields,  # 输出字段。
            **kwargs,  # 其他关键字参数。
        )
        query_result = query_result[0]  # 获取搜索结果的第一项。
        contexts = []  # 初始化上下文列表。
        for query in query_result:  # 遍历搜索结果。
            data = query["entity"]  # 获取实体数据。
            score = query["distance"]  # 获取距离分数。
            context = data["text"]  # 获取文本上下文。

            if citations:  # 如果需要引用。
                metadata = data.get("metadata", {})  # 获取元数据。
                metadata["score"] = score  # 添加分数到元数据。
                contexts.append(tuple((context, metadata)))  # 将上下文和元数据作为一个元组添加到列表。
            else:
                contexts.append(context)  # 否则只添加上下文到列表。
        return contexts  # 返回上下文列表。

    def count(self) -> int:  # 定义 count 方法，返回类型是整数。
        """
        Count number of documents/chunks embedded in the database.  # 方法说明文档，说明这个方法用来计算数据库中嵌入的文档数量。
        
        :return: number of documents  # 返回文档数量。
        :rtype: int  # 返回类型是整数。
        """
        return self.collection.num_entities  # 返回集合中的实体数量。

    def reset(self, collection_names: list[str] = None):  # 定义 reset 方法，接受一个可选参数 collection_names。
        """
        Resets the database. Deletes all embeddings irreversibly.  # 方法说明文档，说明这个方法用来重置数据库，不可逆地删除所有嵌入。
        
        if self.config.collection_name:  # 如果配置中有集合名称。
            if collection_names:  # 如果提供了集合名称列表。
                for collection_name in collection_names:  # 遍历提供的集合名称。
                    if collection_name in self.client.list_collections():  # 如果集合存在。
                        self.client.drop_collection(collection_name=collection_name)  # 删除集合。
            else:
                self.client.drop_collection(collection_name=self.config.collection_name)  # 删除配置中的集合。
                self._get_or_create_collection(self.config.collection_name)  # 获取或创建集合。

    def set_collection_name(self, name: str):  # 定义 set_collection_name 方法，接受一个参数 name。
        """
        Set the name of the collection. A collection is an isolated space for vectors.  # 方法说明文档，说明这个方法用来设置集合名称。
        
        :param name: Name of the collection.  # 参数 name 表示集合名称。
        :type name: str  # 参数 name 的类型是字符串。
        """
        if not isinstance(name, str):  # 如果 name 不是字符串。
            raise TypeError("Collection name must be a string")  # 抛出类型错误。
        self.config.collection_name = name  # 设置配置中的集合名称。

    def _generate_zilliz_filter(self, where: dict[str, str]):  # 定义私有方法 _generate_zilliz_filter，接受一个参数 where。
        operands = []  # 初始化操作数列表。
        for key, value in where.items():  # 遍历过滤条件字典。
            operands.append(f'(metadata["{key}"] == "{value}")')  # 构建过滤条件。
        return " and ".join(operands)  # 返回由逻辑“与”连接的操作数列表。

    def delete(self, where: dict[str, Any]):  # 定义 delete 方法，接受一个参数 where。
        """
        Delete the embeddings from DB. Zilliz only support deleting with keys.  # 方法说明文档，说明这个方法用来删除嵌入。
        
        :param keys: Primary keys of the table entries to delete.  # 参数 keys 表示要删除的表格条目的主键。
        :type keys: Union[list, str, int]  # 参数 keys 的类型可以是列表、字符串或整数。
        """
        data = self.get(where=where)  # 获取数据。
        keys = data.get("ids", [])  # 获取 ID 列表。
        if keys:  # 如果有 ID。
            self.client.delete(collection_name=self.config.collection_name, pks=keys)  # 删除数据。

