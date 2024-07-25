# 导入abc模块中的ABC和abstractmethod。ABC是抽象基类的意思，abstractmethod是一个装饰器，用来标记抽象方法。
from abc import ABC, abstractmethod

# 定义了一个名为MemoryBase的类，并继承自ABC类，这样MemoryBase就变成了一个抽象基类。
class MemoryBase(ABC):

    # 使用abstractmethod装饰器标记get方法为抽象方法，必须在子类中实现这个方法。
    @abstractmethod
    def get(self, memory_id):
        # 这个方法是用来通过ID获取一条记忆的。
        # 参数：memory_id（字符串类型）：需要获取的记忆的ID。
        # 返回值：字典类型：获取到的记忆内容。
        # 这里写pass表示不做任何操作，实际使用时需要被子类重写。
        pass

    # 同样使用abstractmethod装饰器标记get_all方法为抽象方法，必须在子类中实现这个方法。
    @abstractmethod
    def get_all(self):
        # 这个方法是用来列出所有记忆的。
        # 返回值：列表类型：包含所有记忆的列表。
        # 这里写pass表示不做任何操作，实际使用时需要被子类重写。
        pass

    # 再次使用abstractmethod装饰器标记update方法为抽象方法，必须在子类中实现这个方法。
    @abstractmethod
    def update(self, memory_id, data):
        # 这个方法是用来通过ID更新一条记忆的。
        # 参数：memory_id（字符串类型）：需要更新的记忆的ID。
        # 参数：data（字典类型）：用于更新记忆的数据。
        # 返回值：字典类型：更新后的记忆内容。
        # 这里写pass表示不做任何操作，实际使用时需要被子类重写。
        pass

    # 还是使用abstractmethod装饰器标记delete方法为抽象方法，必须在子类中实现这个方法。
    @abstractmethod
    def delete(self, memory_id):
        # 这个方法是用来通过ID删除一条记忆的。
        # 参数：memory_id（字符串类型）：需要删除的记忆的ID。
        # 这里写pass表示不做任何操作，实际使用时需要被子类重写。
        pass

    # 最后一次使用abstractmethod装饰器标记history方法为抽象方法，必须在子类中实现这个方法。
    @abstractmethod
    def history(self, memory_id):
        # 这个方法是用来通过ID获取一条记忆的历史变更记录的。
        # 参数：memory_id（字符串类型）：需要获取历史记录的记忆的ID。
        # 返回值：列表类型：包含这条记忆的所有变更记录。
        # 这里写pass表示不做任何操作，实际使用时需要被子类重写。
        pass

