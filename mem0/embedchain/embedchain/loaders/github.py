# 引入了多个工具包，这些工具包可以帮助我们完成一些任务。
import concurrent.futures    # 这个包能帮助我们同时做多件事情，就像是你可以一边吃饭一边看电视。
import hashlib               # 这个包可以帮我们把信息变成一种特殊的代码，别人很难看懂，用来保护我们的信息。
import logging              # 这个包能帮我们记录发生了什么，就像是写日记，这样如果出问题了，我们可以查日记找到原因。
import re                   # 这个包能帮我们查找和替换文本中的模式，就像是找寻藏在文字里的宝藏。
import shlex                # 这个包能帮我们理解命令行输入的指令，就像是帮你理解妈妈说的“去超市买牛奶”。
from typing import Any, Optional   # 这个是从typing库中引入的，帮我们更好地理解和描述变量的类型。

# 下面是导入了一些特定的功能模块，这些模块是专门为了处理某些任务而设计的。
from tqdm import tqdm       # 这个模块可以在执行任务时显示进度条，就像是玩游戏时的血条，让我们知道还剩多少。

# 下面是从一个叫做embedchain的软件包里导入了BaseLoader类，这个类是用来加载数据的。
from embedchain.loaders.base_loader import BaseLoader

# 这个函数可以帮我们清理字符串，就像是打扫房间，把不需要的东西都清理掉。
from embedchain.utils.misc import clean_string

# 下面是一些常量，就像是地图上的标记点，告诉我们一些重要的位置。
GITHUB_URL = "https://github.com"      # 这是GitHub的网址，一个程序员们分享和合作写代码的地方。
GITHUB_API_URL = "https://api.github.com"  # 这是GitHub的API网址，就像是后门，可以让我们用特别的方法访问GitHub。

# 这个集合定义了搜索时可以用的类型，就像是选择菜单上的选项，有code（代码）、repo（仓库）等等。
VALID_SEARCH_TYPES = set(["code", "repo", "pr", "issue", "discussion", "branch", "file"])

class GithubLoader(BaseLoader):

