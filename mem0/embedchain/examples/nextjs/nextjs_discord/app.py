# 导入日志模块，用于记录程序运行信息
import logging
# 导入操作系统模块，用于与环境变量交互
import os
# 导入Discord模块，用于和Discord服务器通信
import discord
# 导入dotenv模块，用于加载环境变量
import dotenv
# 导入requests模块，用于发送网络请求
import requests

# 加载存储在.env文件中的环境变量
dotenv.load_dotenv(".env")

# 设置Discord机器人的权限
intents = discord.Intents.default()
# 确保机器人可以读取消息内容
intents.message_content = True
# 创建一个Discord客户端实例
client = discord.Client(intents=intents)
# 从环境变量中获取机器人的名字
discord_bot_name = os.environ["DISCORD_BOT_NAME"]

# 配置日志记录器
logger = logging.getLogger(__name__)

