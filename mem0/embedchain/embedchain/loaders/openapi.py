# 导入一个叫做 hashlib 的工具包，它可以帮助我们生成一种特别的代码（叫哈希码）。
import hashlib
# 导入一个叫做 StringIO 的工具，它可以让我们把字符串当作文件来读写。
from io import StringIO
# 导入一个叫做 urlparse 的工具，它可以帮助我们解析网址。
from urllib.parse import urlparse
# 导入一个叫做 requests 的工具包，它能帮助我们在网上获取信息。
import requests
# 导入一个叫做 yaml 的工具包，它能帮助我们处理一种叫 YAML 的文件格式。
import yaml

# 导入一些自定义的部分，它们是我们自己写的帮助程序。
from embedchain.loaders.base_loader import BaseLoader

