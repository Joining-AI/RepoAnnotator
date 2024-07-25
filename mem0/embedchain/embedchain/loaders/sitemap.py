# 引入了处理并发任务的库，可以同时做很多事情
import concurrent.futures
# 这个库用于生成文件的唯一标识符
import hashlib
# 日志记录工具，帮助我们跟踪发生了什么
import logging
# 操作系统相关功能，比如检查文件是否存在
import os
# 用于解析URL的工具
from urllib.parse import urlparse

# 请求网络资源的库
import requests
# 显示进度条的库，让等待看起来更友好
from tqdm import tqdm

# 尝试导入解析HTML的库，如果找不到，会告诉用户如何安装
try:
    from bs4 import BeautifulSoup
    from bs4.builder import ParserRejectedMarkup
except ImportError:
    raise ImportError(
        "Sitemap 需要额外的依赖库。可以通过 `pip install beautifulsoup4==4.12.3` 安装"
    ) from None

# 注册一个类，让它可以从JSON字符串中恢复成对象
from embedchain.helpers.json_serializable import register_deserializable
# 基础的数据加载器类
from embedchain.loaders.base_loader import BaseLoader
# 网页加载器，用于加载单个网页的内容
from embedchain.loaders.web_page import WebPageLoader

# 设置日志记录器，记录程序运行中的信息
logger = logging.getLogger(__name__)

