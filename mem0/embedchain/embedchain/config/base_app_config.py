# 导入日志模块
import logging
# 导入类型提示中的可选类型
from typing import Optional

# 从 embedchain 的配置文件夹中导入一个基础配置类
from embedchain.config.base_config import BaseConfig
# 从 embedchain 的帮助工具中导入一个可以让对象序列化为 JSON 的类
from embedchain.helpers.json_serializable import JSONSerializable
# 从 embedchain 的向量数据库文件夹中导入一个向量数据库的基础类
from embedchain.vectordb.base import BaseVectorDB

# 创建一个日志记录器，这里给它起个名字叫做 __name__ 对应的日志记录器
logger = logging.getLogger(__name__)

# 定义一个类 BaseAppConfig，它是 BaseConfig 和 JSONSerializable 这两个类的子类
class BaseAppConfig(BaseConfig, JSONSerializable):
    # 这个类是用来初始化一个 App 实例的基础配置的
    """
    父配置类，用来初始化一个 `App` 实例。
    """

    # 初始化方法，创建这个类的一个实例
    def __init__(
        self,
        log_level: str = "WARNING",  # 日志级别，默认是 "WARNING"
        db: Optional[BaseVectorDB] = None,  # 数据库对象，默认是 None
        id: Optional[str] = None,  # 应用的 ID，默认是 None
        collect_metrics: bool = True,  # 是否收集匿名数据，默认是 True
        collection_name: Optional[str] = None,  # 集合名称，默认是 None
    ):
        """
        初始化一个 App 的配置类实例。
        大部分配置工作在 `App` 类里面完成。

        参数：
        - log_level: 日志调试级别，默认是 "WARNING"。
        - db: 数据库类，默认是 None。建议直接在 `App` 类里设置。
        - id: 应用的 ID，默认是 None。文档元数据会包含这个 ID。
        - collect_metrics: 是否发送匿名遥测数据以改进 embedchain，默认是 True。
        - collection_name: 默认集合名称，默认是 None。建议使用 app.db.set_collection_name() 来设置。
        """

        # 设置应用的 ID
        self.id = id
        # 设置是否收集匿名数据，如果是 None 或者 True 就设为 True，否则设为 False
        self.collect_metrics = True if (collect_metrics is True or collect_metrics is None) else False
        # 设置默认集合名称
        self.collection_name = collection_name

        # 如果数据库对象 db 不为空
        if db:
            # 把 db 赋值给私有属性 _db
            self._db = db
            # 输出一条警告信息，告诉用户最好使用新的方式传递数据库对象
            logger.warning(
                "过时警告：请在创建 App 实例时将数据库作为第二个参数传入。例如 `app(config=config, db=db)`。"
            )

        # 如果集合名称 collection_name 不为空
        if collection_name:
            # 输出一条警告信息，告诉用户最好使用新的方式设置集合名称
            logger.warning("过时警告：请将集合名称设置到数据库配置中。")
        
        # 这里没有实际作用，只是为了让代码完整，通常我们不需要写这行
        return

    # 一个私有方法，用来设置日志
    def _setup_logging(self, log_level):
        # 配置日志格式和级别
        logger.basicConfig(format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s", level=log_level)
        # 获取日志记录器
        self.logger = logger.getLogger(__name__)

