# 导入需要的库
import hashlib           # 用于生成唯一标识符
import logging          # 记录程序运行过程中的信息
import time             # 控制程序的运行时间
from xml.etree import ElementTree # 解析XML文件
import requests         # 发送网络请求

# 自定义的导入，用于序列化和加载数据
from embedchain.helpers.json_serializable import register_deserializable
from embedchain.loaders.base_loader import BaseLoader
from embedchain.utils.misc import is_readable

# 设置日志记录器
logger = logging.getLogger(__name__)

