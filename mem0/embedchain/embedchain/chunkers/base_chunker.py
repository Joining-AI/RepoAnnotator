# 导入一些需要的库和工具。
import hashlib
import logging
from typing import Optional

# 导入其他相关模块。
from embedchain.config.add_config import ChunkerConfig
from embedchain.helpers.json_serializable import JSONSerializable
from embedchain.models.data_type import DataType

# 设置日志记录器。
logger = logging.getLogger(__name__)

# 定义了一个类 `BaseChunker`，它继承自 `JSONSerializable` 类。
class BaseChunker(JSONSerializable):
    # 初始化方法，创建一个新的 `BaseChunker` 实例时会被调用。
    def __init__(self, text_splitter):
        # 这里设置了一个属性 `text_splitter`，它用来分割文本。
        self.text_splitter = text_splitter
        # 还有一个属性 `data_type`，暂时还没设置值。
        self.data_type = None

    # 这个方法用来创建文档块（也就是把大的文档分成小块）。
    def create_chunks(self, loader, src, app_id=None, config: Optional[ChunkerConfig] = None):
        # 创建一个空列表，用来存放分割后的文档块。
        documents = []
        # 这个列表用来存放每个文档块的唯一标识符。
        chunk_ids = []
        # 这个字典用来确保每个文档块的标识符是唯一的。
        id_map = {}
        # 获取最小文档块大小，如果没有配置就默认为1。
        min_chunk_size = config.min_chunk_size if config is not None else 1
        # 记录日志，告诉我们忽略小于指定大小的文档块。
        logger.info(f"Skipping chunks smaller than {min_chunk_size} characters")
        # 使用 `loader` 加载数据。
        data_result = loader.load_data(src)
        # 从加载结果中获取实际的数据内容。
        data_records = data_result["data"]
        # 从加载结果中获取文档的 ID。
        doc_id = data_result["doc_id"]
        # 如果提供了 `app_id`，就在文档 ID 前面加上它，以区分不同的应用。
        doc_id = f"{app_id}--{doc_id}" if app_id is not None else doc_id
        # 创建一个空列表，用来存放每个文档块的元数据（比如作者、来源等信息）。
        metadatas = []
        # 遍历加载的数据内容。
        for data in data_records:
            # 获取当前数据的内容部分。
            content = data["content"]
            # 获取当前数据的元数据部分。
            metadata = data["meta_data"]
            # 在元数据中添加数据类型信息，方便后续查询。
            metadata["data_type"] = self.data_type.value
            # 在元数据中添加文档 ID。
            metadata["doc_id"] = doc_id
            # 获取元数据中的 URL，如果不存在则使用 `src` 作为 URL。
            url = metadata.get("url", src)
            # 把内容分割成多个文档块。
            chunks = self.get_chunks(content)
            # 遍历每个文档块。
            for chunk in chunks:
                # 根据文档块内容和 URL 生成一个唯一的标识符。
                chunk_id = hashlib.sha256((chunk + url).encode()).hexdigest()
                # 如果提供了 `app_id`，就在文档块 ID 前面加上它。
                chunk_id = f"{app_id}--{chunk_id}" if app_id is not None else chunk_id
                # 检查这个文档块是否已经被处理过，并且它的长度是否大于等于最小长度。
                if id_map.get(chunk_id) is None and len(chunk) >= min_chunk_size:
                    # 如果符合条件，就把它加入到字典中，表示已经处理过了。
                    id_map[chunk_id] = True
                    # 把文档块添加到列表中。
                    chunk_ids.append(chunk_id)
                    documents.append(chunk)
                    metadatas.append(metadata)
        # 最后返回一个字典，包含所有处理过的文档块信息。
        return {
            "documents": documents,
            "ids": chunk_ids,
            "metadatas": metadatas,
            "doc_id": doc_id,
        }

    # 这个方法用来获取文档块。
    def get_chunks(self, content):
        # 默认使用 `text_splitter` 分割内容。
        return self.text_splitter.split_text(content)

    # 这个方法用来设置文档类型。
    def set_data_type(self, data_type: DataType):
        # 设置 `data_type` 属性。
        self.data_type = data_type

        # 有一些待办事项，这里就不详细展开了。

    # 这是一个静态方法，用来计算文档总词数。
    @staticmethod
    def get_word_count(documents) -> int:
        # 计算并返回所有文档的单词总数。
        return sum(len(document.split(" ")) for document in documents)

