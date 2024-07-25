# 导入一个叫做hashlib的模块，它能帮助我们创建一种特殊的安全码。
import hashlib

# 导入一个叫做logging的模块，这个模块能帮助我们在程序运行时记录信息，就像写日记一样。
import logging

# 导入一个叫做os的模块，它能帮助我们和电脑系统更好地交流。
import os

# 下面这行代码是从另一个文件里导入一个工具，这个工具能帮助我们把一些数据变成可以保存在文件里的格式。
from embedchain.helpers.json_serializable import register_deserializable

# 这行代码也是从另一个文件里导入一个基础的加载器，加载器就像是一个搬运工，帮助我们把数据从一个地方搬到另一个地方。
from embedchain.loaders.base_loader import BaseLoader

# 这行代码是设置一个日志记录器，我们可以用它来记录程序运行的情况。这里的logger就像是一个专门记录这些信息的小本子。
logger = logging.getLogger(__name__)

# 最后这行代码是在告诉我们的程序，接下来要使用一个特殊的标记，这个标记可以帮助我们注册一个类或者函数，让它具有可序列化的能力。
# 就像是给一个玩具贴上标签，这样别人就知道这个玩具是可以被拆开再重新组装的。
@register_deserializable

