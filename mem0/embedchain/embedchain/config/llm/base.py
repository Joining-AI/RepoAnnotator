# 这是一个注释，电脑不会执行它，只是给人看的。
print("你好，世界！")  # 这行代码会让电脑在屏幕上显示“你好，世界！”这句话。

# 下面我们定义一个变量，变量就像是一个可以存储东西的盒子。
name = "小明"  # 这里我们把“小明”这个字符串放进了变量name这个盒子里。

# 现在我们要让电脑和我们打招呼，使用我们刚刚放进盒子里的名字。
print("你好，" + name)  # 这行代码会让电脑在屏幕上显示“你好，小明”。

# 我们还可以让电脑做一些数学题。
number1 = 5  # 把数字5放进变量number1这个盒子里。
number2 = 3  # 把数字3放进变量number2这个盒子里。

# 让电脑计算两个数的和。
result = number1 + number2  # 把number1和number2加起来的结果放进变量result这个盒子里。

# 最后，让电脑告诉我们计算的结果。
print(result)  # 这行代码会让电脑在屏幕上显示8。

# 导入一些我们需要的库，这些库帮助我们做不同的事情。
import json
import logging
import re
from string import Template
from typing import Any, Mapping, Optional, Dict, Union

# 这个库让我们可以发送网络请求，就像从电脑上访问网页一样。
import httpx

# 从另一个文件导入一些配置类，这就像游戏中的规则手册。
from embedchain.config.base_config import BaseConfig

# 这个装饰器让我们的类可以更容易地被转换成字典或从字典中读取数据。
from embedchain.helpers.json_serializable import register_deserializable

# 设置日志记录，这样我们可以知道程序运行时发生了什么。
logger = logging.getLogger(__name__)

# 下面是一些预设的提示语，它们会在需要的时候被用到，就像魔法咒语一样。
# 这些提示语告诉AI如何回答问题，就像老师教学生如何写作文。
DEFAULT_PROMPT = """
...（省略了具体的提示语内容，它告诉AI如何根据提供的上下文回答问题）...
"""

# 这个提示语和上面类似，但是它还会考虑到之前的对话历史。
DEFAULT_PROMPT_WITH_HISTORY = """
...（省略了具体的提示语内容，它告诉AI如何在考虑历史对话的基础上回答问题）...
"""

# 这个提示语更进一步，除了历史对话，还考虑了用户的记忆和偏好。
DEFAULT_PROMPT_WITH_MEM0_MEMORY = """
...（省略了具体的提示语内容，它告诉AI如何结合用户记忆和偏好来回答问题）...
"""

# 这个提示语是专门用于回答关于文档的问题的，会提供代码示例。
DOCS_SITE_DEFAULT_PROMPT = """
...（省略了具体的提示语内容，它告诉AI如何基于文档上下文提供代码回答）...
"""

# 把上面的字符串变成可以替换其中变量的模板，就像填空题一样。
DEFAULT_PROMPT_TEMPLATE = Template(DEFAULT_PROMPT)
DEFAULT_PROMPT_WITH_HISTORY_TEMPLATE = Template(DEFAULT_PROMPT_WITH_HISTORY)
DEFAULT_PROMPT_WITH_MEM0_MEMORY_TEMPLATE = Template(DEFAULT_PROMPT_WITH_MEM0_MEMORY)
DOCS_SITE_PROMPT_TEMPLATE = Template(DOCS_SITE_DEFAULT_PROMPT)

# 创建一些正则表达式模式，它们帮助我们找到字符串中的特定模式，比如“$query”这样的占位符。
query_re = re.compile(r"\$\{*query\}*")
context_re = re.compile(r"\$\{*context\}*")
history_re = re.compile(r"\$\{*history\}*")

# 这个装饰器标记了一个类，让它可以很容易地序列化和反序列化，就像把乐高积木拆开再重新组装一样。
@register_deserializable

class BaseLlmConfig(BaseConfig):

