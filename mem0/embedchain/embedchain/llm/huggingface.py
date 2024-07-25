# 引入了Python的一个标准库模块，它允许我们在运行时动态地导入其他模块。
import importlib

# 引入Python的日志记录模块，用于记录程序运行过程中的信息。
import logging

# 引入操作系统模块，可以用来与操作系统进行交互，比如读取环境变量等。
import os

# 这行代码是从Python的类型提示库中引入了一个叫做Optional的类型，这个类型在定义函数参数或返回值时使用，表示这个值可以是None或者指定的类型。
from typing import Optional

# 从langchain_community库的llms子目录下的huggingface_endpoint模块中引入HuggingFaceEndpoint类。
# 这个类是用来和HuggingFace的模型端点通信的，可以调用部署在远程服务器上的模型。
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint

# 同样的方式，这里引入了HuggingFaceHub类，它提供了和HuggingFace Hub上的模型进行交互的功能。
from langchain_community.llms.huggingface_hub import HuggingFaceHub

# 再次以相同的方式引入HuggingFacePipeline类，这个类是用来执行HuggingFace的pipeline操作的，比如文本生成、问答等。
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline

# 从embedchain库的config子目录中引入BaseLlmConfig类，这个类可能是用来配置语言模型的基本设置的。
from embedchain.config import BaseLlmConfig

# 引入了一个叫做register_deserializable的装饰器，它可以将一个类注册为可序列化/反序列化的，这意味着这个类的对象可以被转换成字符串保存，也可以从字符串中恢复出来。
from embedchain.helpers.json_serializable import register_deserializable

# 引入了embedchain库的llm子目录下的base模块中的BaseLlm类，这个类可能是所有语言模型类的基类，包含了一些通用的方法和属性。
from embedchain.llm.base import BaseLlm

# 创建一个日志记录器，名字是__name__，这通常意味着这个日志记录器只在这个模块内部使用。
logger = logging.getLogger(__name__)

# 使用register_deserializable装饰器来修饰接下来要定义的类，这样这个类就可以被序列化和反序列化了。
@register_deserializable

class HuggingFaceLlm(BaseLlm):  # 这里创建了一个新的类叫做 HuggingFaceLlm，它继承自 BaseLlm 类。

