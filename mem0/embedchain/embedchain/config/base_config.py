# 导入一个叫做 "Any" 的类型提示工具，它可以帮助我们更好地理解和编写代码。
from typing import Any

# 导入一个名为 "JSONSerializable" 的类，这个类帮助我们将数据转换成 JSON 格式。
from embedchain.helpers.json_serializable import JSONSerializable


# 定义了一个名为 BaseConfig 的类，并让它继承自 JSONSerializable 类。
# 这意味着 BaseConfig 会拥有 JSONSerializable 类的所有功能。
class BaseConfig(JSONSerializable):
    """
    Base config.
    """

    # 初始化方法，当我们创建一个新的 BaseConfig 对象时，这个方法会被自动调用。
    def __init__(self):
        """Initializes a configuration class for a class."""
        # 这里没有做任何事情，只是简单地通过 "pass" 声明了初始化方法。
        pass

    # 这个方法用于把 BaseConfig 对象转换成字典格式。
    def as_dict(self) -> dict[str, Any]:
        """Return config object as a dict

        :return: config object as dict
        :rtype: dict[str, Any]
        """
        # 使用 "vars" 函数将对象的属性转换成字典形式并返回。
        return vars(self)

