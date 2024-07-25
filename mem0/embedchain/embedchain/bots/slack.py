# 导入一些我们需要的工具库，这些库可以帮助我们做不同的事情。
import argparse          # 这个库让我们可以从命令行输入参数。
import logging           # 这个库帮助我们记录程序运行时的信息。
import os                # 这个库让我们可以和操作系统交互，比如获取环境变量。
import signal            # 这个库用来处理程序中断信号，比如用户按Ctrl+C。
import sys               # 这个库提供了很多系统相关的函数，比如退出程序。

# 导入一些专门的库和模块，它们是程序的核心部分。
from embedchain import App     # 这个是从embedchain库导入的App类，用于创建应用程序。
from embedchain.helpers.json_serializable import register_deserializable   # 这个是从embedchain库导入的装饰器，用于注册可序列化的类。

# 下面是从一个叫做base的模块中导入BaseBot类，这个类是所有机器人的基础。
from .base import BaseBot

# 尝试导入Flask和Slack相关的库，如果找不到会抛出错误并告诉用户怎么安装。
try:
    from flask import Flask, request     # Flask是一个用于创建web应用的微框架。
    from slack_sdk import WebClient      # Slack SDK，用于和Slack平台通信。
except ModuleNotFoundError:
    # 如果没有找到所需的库，这里会告诉用户需要安装哪些库。
    raise ModuleNotFoundError(
        "The required dependencies for Slack are not installed."
        "请用`pip install slack-sdk==3.21.3 flask==2.3.3`来安装必要的库。"
    ) from None

# 设置日志记录器，这样我们就可以在程序运行时看到重要的信息。
logger = logging.getLogger(__name__)

# 从环境变量中获取Slack机器人的令牌，这是和Slack平台通信的身份验证。
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

# 使用装饰器注册一个可序列化的类，这在数据持久化或传输时很有用。
@register_deserializable

# 定义一个叫做SlackBot的类，继承自BaseBot
class SlackBot(BaseBot):

