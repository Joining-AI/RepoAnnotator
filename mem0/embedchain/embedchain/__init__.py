# 这行代码是导入Python的一个模块，这个模块可以帮助我们获取一些关于程序的信息，比如版本号。
import importlib.metadata

# 下面这行代码是在设置一个叫做`__version__`的变量。它会从我们当前运行的程序包里找到版本信息，
# 如果找不到，它就会从程序的名字那里找。这样，我们就可以知道这个程序是哪个版本了。
__version__ = importlib.metadata.version(__package__ or __name__)

# 从这里开始，我们要从其他文件里导入一些东西到我们的程序里。
# 第一个导入的是`App`，这是个很厉害的东西，可以帮我们创建应用。
from embedchain.app import App  # noqa: F401

# 接下来，我们导入`Client`，这是一个帮助我们和程序交流的小助手。
from embedchain.client import Client  # noqa: F401

# 最后，我们还要导入`Pipeline`，它像是一个流水线，帮助我们处理数据。
from embedchain.pipeline import Pipeline  # noqa: F401

# 现在，我们要确保用户有一个专门的目录来保存他们的数据。
# 如果这个目录还没有，我们的小助手`Client`会帮我们创建一个。
Client.setup()

