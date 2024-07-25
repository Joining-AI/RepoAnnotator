# 导入json模块，用于处理json数据
import json
# 导入logging模块，用于记录日志信息
import logging
# 导入Template类，可能用于字符串模板化处理
from string import Template
# 导入Type、TypeVar和Union，这些是类型提示相关的工具
from typing import Any, Type, TypeVar, Union

# 定义一个类型变量T，它的约束条件是必须继承自"JSONSerializable"这个类
T = TypeVar("T", bound="JSONSerializable")

# 这里是一个备注：通过继承关系，我们所有的类都应该成为JSONSerializable的子类（最高级）
# 另一个备注：@register_deserializable装饰器应该被添加到所有面向用户的子类上（最低级）

# 创建一个名为__name__的日志记录器，用来记录这个文件中的日志信息
logger = logging.getLogger(__name__)

# 定义一个装饰器函数，作用是注册一个可以被反序列化的类
def register_deserializable(cls: Type[T]) -> Type[T]:
    """
    一个类装饰器，用来注册一个类使其可以被反序列化。

    当一个类用@register_deserializable装饰时，它就变成了
    JSONSerializable类可以反序列化的类集合中的一员。

    反序列化基本上就是从json文件中加载属性的过程。
    这个装饰器是一个安全措施，确保你不会加载原本属于其他类的属性。

    示例：
        @register_deserializable
        class ChildClass(JSONSerializable):
            def __init__(self, ...):
                # 初始化逻辑

    参数:
        cls (Type): 需要注册的类。

    返回:
        Type: 注册后的相同类。
    """
    # 调用JSONSerializable类中的_register_class_as_deserializable方法来注册这个类
    JSONSerializable._register_class_as_deserializable(cls)
    # 最后返回传入的类本身
    return cls

# 定义一个类叫做JSONSerializable，这个类能帮助我们把对象变成JSON格式，或者从JSON格式读取对象。
class JSONSerializable:
    # 这个集合用来存放那些被允许从JSON转换回来的类，就像一个白名单一样。
    _deserializable_classes = set()

    # 这个方法把对象变成JSON字符串。
    def serialize(self) -> str:
        try:
            # 使用json.dumps把self（也就是当前对象）变成JSON字符串，如果对象有特殊类型，会用到_auto_encoder方法来处理。
            return json.dumps(self, default=self._auto_encoder, ensure_ascii=False)
        except Exception as e:
            # 如果转换出错，记录错误信息并返回一个空的JSON字符串。
            logger.error(f"序列化错误：{e}")
            return "{}"

    # 这个类方法从JSON字符串读取对象。
    @classmethod
    def deserialize(cls, json_str: str) -> Any:
        try:
            # 使用json.loads从JSON字符串读取对象，如果需要，会调用_auto_decoder方法来处理特殊类型。
            return json.loads(json_str, object_hook=cls._auto_decoder)
        except Exception as e:
            # 如果读取失败，记录错误信息，并返回一个这个类的新实例作为默认值。
            logger.error(f"反序列化错误：{e}")
            return cls()

    # 静态方法，用于自动编码对象以便进行JSON序列化。
    @staticmethod
    def _auto_encoder(obj: Any) -> Union[dict[str, Any], None]:
        # 如果对象有__dict__属性，意味着它可以被转换成字典。
        if hasattr(obj, "__dict__"):
            dct = {}
            # 遍历对象的所有属性和值。
            for key, value in obj.__dict__.items():
                try:
                    # 如果值也是一个JSONSerializable的实例，先把它序列化再加到字典里。
                    if isinstance(value, JSONSerializable):
                        serialized_value = value.serialize()
                        dct[key] = json.loads(serialized_value)
                    # 特殊处理Template类型，把它的数据保存下来。
                    elif isinstance(value, Template):
                        dct[key] = {"__type__": "Template", "data": value.template}
                    # 其他类型的值，尝试直接序列化。
                    else:
                        json.dumps(value)
                        dct[key] = value
                except TypeError:
                    # 如果序列化失败，跳过这个键值对。
                    pass
            # 把对象的类名也保存在字典里。
            dct["__class__"] = obj.__class__.__name__
            return dct
        # 如果对象不能被序列化，抛出错误。
        raise TypeError(f"类型为{type(obj)}的对象无法进行JSON序列化")

    # 类方法，用于在JSON反序列化时自动解码字典。
    @classmethod
    def _auto_decoder(cls, dct: dict[str, Any]) -> Any:
        # 从字典中取出类名。
        class_name = dct.pop("__class__", None)
        if class_name:
            # 检查是否注册了可反序列化的类。
            if not hasattr(cls, "_deserializable_classes"):
                raise AttributeError(f"`{class_name}`没有可反序列化类的注册。")
            if class_name not in {cl.__name__ for cl in cls._deserializable_classes}:
                raise KeyError(f"不允许反序列化`{class_name}`类。")
            # 找到目标类。
            target_class = next((cl for cl in cls._deserializable_classes if cl.__name__ == class_name), None)
            if target_class:
                # 创建目标类的新实例。
                obj = target_class.__new__(target_class)
                # 遍历字典中的键值对，处理特殊类型。
                for key, value in dct.items():
                    if isinstance(value, dict) and "__type__" in value:
                        if value["__type__"] == "Template":
                            value = Template(value["data"])
                        # 未来可以添加更多自定义类型的处理。
                    # 设置对象的属性。
                    default_value = getattr(target_class, key, None)
                    setattr(obj, key, value or default_value)
                return obj
        # 如果无法解码，直接返回原字典。
        return dct

    # 方法，将序列化后的对象保存到文件。
    def save_to_file(self, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            # 写入序列化后的字符串到文件。
            f.write(self.serialize())

    # 类方法，从文件加载并反序列化对象。
    @classmethod
    def load_from_file(cls, filename: str) -> Any:
        with open(filename, "r", encoding="utf-8") as f:
            # 读取文件内容，然后反序列化。
            json_str = f.read()
            return cls.deserialize(json_str)

    # 类方法，注册一个类为可反序列化。
    @classmethod
    def _register_class_as_deserializable(cls, target_class: Type[T]) -> None:
        # 把目标类加入到可反序列化的集合中。
        cls._deserializable_classes.add(target_class)

