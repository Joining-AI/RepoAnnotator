# 这一行导入了一些工具，让程序可以处理不同类型的值。
from typing import Any, Optional

# 这一行是从另一个文件里拿来了一个叫做 `BaseConfig` 的配置类。
from embedchain.config.base_config import BaseConfig
# 这行代码也是从其他地方拿来的一个装饰器（就像是给函数穿上的特殊外套），用来帮助我们处理一些数据。
from embedchain.helpers.json_serializable import register_deserializable

# 这个装饰器告诉 Python，`Mem0Config` 类可以被特殊地保存和读取，就像把东西打包好再拆包一样简单。
@register_deserializable
# 定义了一个新的类 `Mem0Config`，它继承自 `BaseConfig`。
class Mem0Config(BaseConfig):
    # 这是一个构造函数，当创建 `Mem0Config` 类的新对象时，会自动调用它。
    def __init__(self, api_key: str, top_k: Optional[int] = 10):
        # 这行代码将传入的 `api_key` 值保存在了当前对象中。
        self.api_key = api_key
        # 这行代码将传入的 `top_k` 值保存在了当前对象中。如果没有给出 `top_k`，那么默认值就是 10。
        self.top_k = top_k

    # 这是一个静态方法，意味着它不需要访问类中的任何特定实例就能工作。
    @staticmethod
    # 这个方法接收一个字典作为参数，用来创建一个新的 `Mem0Config` 对象。
    def from_config(config: Optional[dict[str, Any]]):
        # 如果没有提供配置信息（即 `config` 是 `None`），就直接返回一个默认的 `Mem0Config` 对象。
        if config is None:
            return Mem0Config()
        else:
            # 如果提供了配置信息，就根据这些信息创建一个新的 `Mem0Config` 对象。
            # `config.get("api_key", "")` 会尝试从配置中获取 `api_key` 的值，如果找不到，则使用空字符串。
            # `config.get("top_k", 10)` 会尝试从配置中获取 `top_k` 的值，如果找不到，则使用 10。
            return Mem0Config(
                api_key=config.get("api_key", ""),
                init_config=config.get("top_k", 10),
            )

