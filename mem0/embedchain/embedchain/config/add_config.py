# 导入Python内置的一些功能模块。
import builtins
# 导入日志记录的功能。
import logging
# 导入用来处理可调用对象（函数等）的工具。
from collections.abc import Callable
# 导入动态导入模块的功能。
from importlib import import_module
# 导入类型提示中的“可选”类型，表示某个参数可以是某种类型或None。
from typing import Optional

# 导入自定义的基配置类。
from embedchain.config.base_config import BaseConfig
# 导入一个装饰器，用于注册类以便进行序列化和反序列化操作。
from embedchain.helpers.json_serializable import register_deserializable

# 使用上面的装饰器来注册这个类。
@register_deserializable
# 定义了一个名为`ChunkerConfig`的类，继承自`BaseConfig`。
class ChunkerConfig(BaseConfig):
    # 这个类是用来配置如何把大段文本分成小块的。
    """
    Config for the chunker used in `add` method
    """

    # 定义构造函数，初始化这个类的实例。
    def __init__(
        self,
        # 每个小块的大小，默认是2000个字符。
        chunk_size: Optional[int] = 2000,
        # 小块之间重叠的字符数量，默认是0。
        chunk_overlap: Optional[int] = 0,
        # 计算文本长度的方法，默认是使用Python内置的`len`函数。
        length_function: Optional[Callable[[str], int]] = None,
        # 最小允许的小块大小，默认是0。
        min_chunk_size: Optional[int] = 0,
    ):
        # 设置每块的大小。
        self.chunk_size = chunk_size
        # 设置块间的重叠大小。
        self.chunk_overlap = chunk_overlap
        # 设置最小块大小。
        self.min_chunk_size = min_chunk_size
        # 如果最小块大小大于等于每块的大小，那么就报错。
        if self.min_chunk_size >= self.chunk_size:
            raise ValueError(f"min_chunk_size {min_chunk_size} should be less than chunk_size {chunk_size}")
        # 如果最小块大小小于块间重叠的大小，会给出警告。
        if self.min_chunk_size < self.chunk_overlap:
            logging.warning(
                f"min_chunk_size {min_chunk_size} should be greater than chunk_overlap {chunk_overlap}, otherwise it is redundant."  # noqa:E501
            )
        
        # 如果用户传入的是字符串形式的长度计算方法，那么就解析并加载它。
        if isinstance(length_function, str):
            self.length_function = self.load_func(length_function)
        # 否则直接使用用户提供的计算长度的函数，如果没有提供，则使用默认的`len`函数。
        else:
            self.length_function = length_function if length_function else len

    # 静态方法，用于从字符串形式加载函数。
    @staticmethod
    def load_func(dotpath: str):
        # 如果字符串中没有`.`分隔符，那么尝试直接从Python内置函数中获取。
        if "." not in dotpath:
            return getattr(builtins, dotpath)
        # 如果有`.`分隔符，说明是一个模块路径+函数名的形式，需要先导入模块再获取函数。
        else:
            module_, func = dotpath.rsplit(".", maxsplit=1)  # 分割模块名和函数名。
            m = import_module(module_)  # 动态导入模块。
            return getattr(m, func)  # 获取并返回函数。

# 使用上面的装饰器来注册这个类。
@register_deserializable
# 定义了一个名为`LoaderConfig`的类，同样继承自`BaseConfig`。
class LoaderConfig(BaseConfig):
    """
    Config for the loader used in `add` method
    """
    # 这个类的构造函数目前什么也不做，将来可能会扩展更多配置选项。
    def __init__(self):
        pass

# 使用上面的装饰器来注册这个类。
@register_deserializable
# 定义了一个名为`AddConfig`的类，也继承自`BaseConfig`。
class AddConfig(BaseConfig):
    """
    Config for the `add` method.
    """
    # 构造函数，初始化这个类的实例。
    def __init__(
        self,
        # 分块器配置，默认是None。
        chunker: Optional[ChunkerConfig] = None,
        # 加载器配置，默认是None。
        loader: Optional[LoaderConfig] = None,
    ):
        # 设置分块器配置。
        self.loader = loader
        # 设置加载器配置。
        self.chunker = chunker

