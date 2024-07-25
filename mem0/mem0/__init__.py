# 这一行代码是导入了一个叫做 "importlib.metadata" 的工具。
import importlib.metadata

# 下面这一行代码做了一件事情：
# 它用我们刚刚导入的工具中的一个功能 "version" 来获取 "mem0ai" 这个程序的版本号，
# 然后把这个版本号保存到叫 "__version__" 的小盒子里。
__version__ = importlib.metadata.version("mem0ai")

# 这一行代码的意思是从 "mem0.memory.main" 这个地方找一个叫做 "Memory" 的东西，
# 并且把它引入到当前的文件中来用。但是这里有个特殊的标记 "# noqa"，意思是告诉一些检查工具不用管这一行代码。
from mem0.memory.main import Memory  # noqa

# 同样的，这一行也是从另一个地方 "mem0.client.main" 找一个叫做 "MemoryClient" 的东西，
# 把它也引入到当前的文件里。这里也有那个特别的标记 "# noqa"。
from mem0.client.main import MemoryClient  # noqa

