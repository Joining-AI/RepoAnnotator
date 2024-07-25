# 从typing模块中导入Optional类型提示，用于表示某些参数可能是None。
from typing import Optional

# 从embedchain.config.base_config模块中导入BaseConfig类，这个类是所有配置类的基础。
from embedchain.config.base_config import BaseConfig


# 定义一个新的类BaseVectorDbConfig，它继承自BaseConfig。
class BaseVectorDbConfig(BaseConfig):
    # 定义初始化方法__init__，当创建BaseVectorDbConfig类的新实例时，这个方法会被自动调用。
    def __init__(
        self,
        # 定义collection_name参数，默认值为None。如果没有提供这个参数，那么就使用默认的"embedchain_store"作为数据库集合的名字。
        collection_name: Optional[str] = None,
        # 定义dir参数，默认值为"db"。这个参数指定了数据库文件存储的位置。
        dir: str = "db",
        # 定义host参数，默认值为None。如果Embedchain程序是作为一个客户端运行的话，需要指定远程主机地址。
        host: Optional[str] = None,
        # 定义port参数，默认值为None。如果Embedchain程序是作为一个客户端运行的话，需要指定远程主机的端口号。
        port: Optional[str] = None,
        # 定义kwargs参数，这是一个字典类型，用来接收其他额外的关键字参数。
        **kwargs,
    ):
        # 如果没有传入collection_name参数或者它的值是None，则使用"embedchain_store"作为默认值。
        self.collection_name = collection_name or "embedchain_store"
        # 将dir参数的值赋给self.dir，这样在类的其他地方可以通过self.dir访问到这个值。
        self.dir = dir
        # 将host参数的值赋给self.host，这样在类的其他地方可以通过self.host访问到这个值。
        self.host = host
        # 将port参数的值赋给self.port，这样在类的其他地方可以通过self.port访问到这个值。
        self.port = port
        # 如果kwargs字典不为空（即有其他的参数传递进来），则遍历字典中的每一个键值对。
        if kwargs:
            # 使用for循环遍历kwargs字典中的每一个键(key)和值(value)。
            for key, value in kwargs.items():
                # 使用setattr函数将键名作为属性名，值作为属性值，添加到当前对象(self)上。
                setattr(self, key, value)

