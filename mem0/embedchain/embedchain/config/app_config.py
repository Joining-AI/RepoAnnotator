# 引入typing模块中的Optional类，这个类用来表示某个变量可能没有值。
from typing import Optional

# 引入一个名为json_serializable的模块里的register_deserializable类，
# 这个类让我们的类可以被序列化和反序列化，简单说就是可以变成字符串保存，也可以从字符串变回来。
from embedchain.helpers.json_serializable import register_deserializable

# 引入base_app_config模块里的BaseAppConfig类，这个类是AppConfig类的父类，包含一些基础配置。
from .base_app_config import BaseAppConfig

# 使用register_deserializable装饰器，告诉Python这个AppConfig类支持序列化和反序列化。
@register_deserializable
# 定义一个名为AppConfig的类，它继承自BaseAppConfig类。
class AppConfig(BaseAppConfig):
    # 这个类是用来初始化embedchain自定义App实例的配置，有一些额外的配置选项。
    """
    Config to initialize an embedchain custom `App` instance, with extra config options.
    """

    # 定义AppConfig类的构造函数（__init__方法），用于创建这个类的实例。
    def __init__(
        # 定义构造函数接收的参数：
        # log_level：日志级别，默认是"WARNING"，可以设置为['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']之一。
        self,
        log_level: str = "WARNING",
        # id：应用的ID，文档元数据会有这个ID，如果没有指定，则默认为None。
        id: Optional[str] = None,
        # name：应用的名字，如果没有指定，则默认为None。
        name: Optional[str] = None,
        # collect_metrics：是否收集匿名数据以改进embedchain，默认为True。
        collect_metrics: Optional[bool] = True,
        # **kwargs：允许传入任意数量的关键字参数，这些参数会被传递给父类。
        **kwargs,
    ):
        # 设置当前实例的name属性。
        self.name = name
        # 调用父类的构造函数，传入log_level、id、collect_metrics和**kwargs作为参数。
        # 这里是在做父类的基础配置。
        super().__init__(log_level=log_level, id=id, collect_metrics=collect_metrics, **kwargs)

