# 导入了两个工具：ABC 和 abstractmethod。
# ABC 是 Abstract Base Class 的缩写，意思是“抽象基类”。
# abstractmethod 是一个装饰器，用来标记一个方法是抽象的，也就是必须在子类中重写的方法。
from abc import ABC, abstractmethod

# 导入了一个叫做 EvalData 的类，这个类是用来表示需要被评估的数据的。
# 这个类定义在另一个文件里，这里只是告诉 Python 我们需要用到它。
from embedchain.utils.evaluation import EvalData


# 定义了一个新的类叫做 BaseMetric，它是所有评估标准的共同祖先。
# 就像所有动物都有一个共同的祖先一样，所有的评估标准都从这个类开始。
# ABC 这个词在这里意味着这是一个抽象基类，不能直接创建它的实例。
class BaseMetric(ABC):
    # 这是一个说明，告诉别人这个类是干什么用的。
    # 就像是玩具包装盒上的说明，告诉小朋友这个玩具怎么玩。
    """Base class for a metric.

    This class provides a common interface for all metrics.
    """

    # 这是一个特殊的方法，叫做构造函数或者初始化方法。
    # 当我们创建一个新的 BaseMetric 对象时，这个方法就会自动被调用。
    # 这里给这个对象起了个名字，默认叫 "base_metric"。
    def __init__(self, name: str = "base_metric"):
        """
        Initialize the BaseMetric.
        """
        # 把传进来的名字赋值给 self.name，self 就像是指向当前对象的一个指针。
        self.name = name

    # 这是一个抽象方法，意味着所有继承自 BaseMetric 的类都必须实现这个方法。
    # 这就像说，如果你要做一个玩具车，那么你必须给这个玩具车加上轮子。
    @abstractmethod
    # 这个方法是用来评估数据集的，数据集是由很多 EvalData 对象组成的列表。
    # EvalData 对象里面包含了要被评估的信息。
    def evaluate(self, dataset: list[EvalData]):
        """
        Abstract method to evaluate the dataset.

        This method should be implemented by subclasses to perform the actual
        evaluation on the dataset.

        :param dataset: dataset to evaluate
        :type dataset: list[EvalData]
        """
        # 因为这是一个抽象方法，所以这里不应该有具体实现。
        # 如果有人试图直接使用 BaseMetric 类而不是继承它并实现 evaluate 方法，
        # 那么这里会抛出一个错误，告诉他们这是不允许的。
        raise NotImplementedError()

