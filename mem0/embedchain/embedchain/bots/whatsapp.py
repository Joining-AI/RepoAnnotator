# 导入一些我们需要的库
import argparse
import importlib
import logging
import signal
import sys

# 导入一些自定义的模块
from embedchain.helpers.json_serializable import register_deserializable
from .base import BaseBot

# 设置日志记录器
logger = logging.getLogger(__name__)

