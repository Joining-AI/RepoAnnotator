# 这里我们从其他文件中引入了一些我们需要的东西
from embedchain.config.vector_db.base import BaseVectorDbConfig  # 引入配置类，它帮助我们设置数据库的一些规则
from embedchain.embedder.base import BaseEmbedder  # 引入嵌入器基类，它负责处理数据的特殊转换
from embedchain.helpers.json_serializable import JSONSerializable  # 引入一个类，让我们的类可以被转化为JSON格式

# 下面定义了一个叫BaseVectorDB的类，它是所有向量数据库的共同基础
class BaseVectorDB(JSONSerializable):  # 我们说这个类继承自JSONSerializable，意味着它可以被转化成JSON
    """这是向量数据库的基础类，所有具体的数据库类都要基于这个类来构建"""

    def __init__(self, config: BaseVectorDbConfig):  # 定义类的初始化方法，每次创建这个类的对象时都会运行这个方法
        """初始化数据库，保存配置和客户端信息

        :param config: 数据库的配置实例，就是那些规则
        :type config: BaseVectorDbConfig
        """
        self.client = self._get_or_create_db()  # 初始化数据库的客户端
        self.config: BaseVectorDbConfig = config  # 保存传进来的配置

    def _initialize(self):  # 这个方法是留给子类实现的，用来做额外的初始化工作
        """
        这个方法很重要，因为它需要在外部设定好`embedder`属性后才能运行。
        所以不能在__init__方法里直接完成。
        """
        raise NotImplementedError  # 抛出异常，表示这个方法还没写好，提醒开发者去实现它

    def _get_or_create_db(self):  # 这个方法也是留给子类实现的，用来获取或创建数据库
        """获取或创建数据库"""
        raise NotImplementedError  # 同样，抛出异常提醒开发者去实现

    def _get_or_create_collection(self):  # 这个方法用来获取或创建数据库里的集合（就像一个文件夹）
        """获取或创建一个命名的集合"""
        raise NotImplementedError  # 提醒开发者去实现

    def _set_embedder(self, embedder: BaseEmbedder):  # 设置嵌入器，让它可以持久地关联到数据库
        """
        数据库有时候需要访问嵌入器，用这个方法可以设置它。

        :param embedder: 要设置为数据库嵌入器的实例
        :type embedder: BaseEmbedder
        """
        self.embedder = embedder  # 把传进来的嵌入器保存为类的一个属性

    def get(self):  # 获取数据库中的嵌入数据
        """根据ID获取数据库中的嵌入数据"""
        raise NotImplementedError  # 提醒开发者去实现

    def add(self):  # 添加数据到数据库
        """添加数据到数据库"""
        raise NotImplementedError  # 提醒开发者去实现

    def query(self):  # 根据向量相似性查询数据库内容
        """根据向量相似性查询数据库中的内容"""
        raise NotImplementedError  # 提醒开发者去实现

    def count(self) -> int:  # 计算数据库中有多少文档或片段
        """
        计算数据库中嵌入了多少文档或片段。

        :return: 文档的数量
        :rtype: int
        """
        raise NotImplementedError  # 提醒开发者去实现

    def reset(self):  # 重置数据库，删除所有数据
        """
        重置数据库，删除所有嵌入的数据，这个操作是不可逆的。
        """
        raise NotImplementedError  # 提醒开发者去实现

    def set_collection_name(self, name: str):  # 设置集合的名字
        """
        设置集合的名字。集合就像是向量的一个独立空间。

        :param name: 集合的名字
        :type name: str
        """
        raise NotImplementedError  # 提醒开发者去实现

    def delete(self):  # 从数据库中删除数据
        """从数据库中删除数据"""
        raise NotImplementedError  # 提醒开发者去实现

