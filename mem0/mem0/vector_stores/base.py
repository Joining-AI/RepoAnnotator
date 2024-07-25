# 从 abc 模块导入 ABC 和 abstractmethod
from abc import ABC, abstractmethod


# 定义了一个叫 VectorStoreBase 的类，它是一个抽象基类（不能直接创建实例）
class VectorStoreBase(ABC):
    # 这是一个抽象方法，告诉所有继承这个类的新类必须要实现这个方法
    # 这个方法用来创建一个新的集合
    @abstractmethod
    def create_col(self, name, vector_size, distance):
        """Create a new collection."""
        pass

    # 这也是一个抽象方法，用来把向量插入到指定的集合里
    @abstractmethod
    def insert(self, name, vectors, payloads=None, ids=None):
        """Insert vectors into a collection."""
        pass

    # 这个抽象方法用于搜索与给定向量相似的其他向量
    @abstractmethod
    def search(self, name, query, limit=5, filters=None):
        """Search for similar vectors."""
        pass

    # 这个抽象方法用于根据 ID 删除一个向量
    @abstractmethod
    def delete(self, name, vector_id):
        """Delete a vector by ID."""
        pass

    # 这个抽象方法用于更新一个向量及其附带的信息
    @abstractmethod
    def update(self, name, vector_id, vector=None, payload=None):
        """Update a vector and its payload."""
        pass

    # 这个抽象方法用于通过 ID 获取一个向量
    @abstractmethod
    def get(self, name, vector_id):
        """Retrieve a vector by ID."""
        pass

    # 这个抽象方法列出所有的集合
    @abstractmethod
    def list_cols(self):
        """List all collections."""
        pass

    # 这个抽象方法用于删除一个集合
    @abstractmethod
    def delete_col(self, name):
        """Delete a collection."""
        pass

    # 这个抽象方法用于获取一个集合的信息
    @abstractmethod
    def col_info(self, name):
        """Get information about a collection."""
        pass

