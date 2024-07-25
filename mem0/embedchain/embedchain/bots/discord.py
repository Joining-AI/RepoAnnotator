# 导入需要的库
import argparse
import logging
import os

# 导入自定义的模块，这些模块帮助我们处理一些特定的功能
from embedchain.helpers.json_serializable import register_deserializable

# 导入自定义的基类，这个类提供了一些基本功能给我们的Discord机器人使用
from .base import BaseBot

# 尝试导入Discord相关的库，如果找不到这些库就会提示用户安装
try:
    import discord
    from discord import app_commands
    from discord.ext import commands
except ModuleNotFoundError:
    # 如果没有找到所需的库，就告诉用户如何安装
    raise ModuleNotFoundError(
        "缺少Discord所需的库，请使用`pip install discord==2.3.2`来安装"
    ) from None

# 设置日志记录器，用来记录程序运行时的信息
logger = logging.getLogger(__name__)

# 这里配置了Discord客户端能够接收的消息类型
intents = discord.Intents.default()
intents.message_content = True

# 创建一个Discord客户端实例
client = discord.Client(intents=intents)

# 创建一个命令树，用来管理机器人的命令
tree = app_commands.CommandTree(client)

# 下面是创建一个Discord机器人类
@register_deserializable
class DiscordBot(BaseBot):
    # 初始化方法，当创建一个新的DiscordBot对象时会调用
    def __init__(self, *args, **kwargs):
        # 调用父类BaseBot的初始化方法
        BaseBot.__init__(self, *args, **kwargs)

    # 添加数据的方法
    def add_data(self, message):
        # 获取消息中的数据
        data = message.split(" ")[-1]
        try:
            # 尝试添加数据到数据库
            self.add(data)
            # 返回成功信息
            response = f"已添加数据：{data}"
        except Exception:
            # 如果添加失败，则记录错误并返回错误信息
            logger.exception(f"无法添加数据：{data}。")
            response = "在添加数据时出现了一些问题。"
        return response

    # 向机器人提问的方法
    def ask_bot(self, message):
        try:
            # 尝试查询答案
            response = self.query(message)
        except Exception:
            # 如果查询失败，则记录错误并返回错误信息
            logger.exception(f"无法查询：{message}。")
            response = "发生了一个错误，请再试一次！"
        return response

    # 启动机器人的方法
    def start(self):
        # 使用环境变量中的令牌来启动Discord客户端
        client.run(os.environ["DISCORD_BOT_TOKEN"])

# 定义一个命令，用于向机器人提问
@tree.command(name="question", description="向embedchain提问")
async def query_command(interaction: discord.Interaction, question: str):
    # 延迟响应以准备回答
    await interaction.response.defer()
    # 获取当前机器人的信息
    member = client.guilds[0].get_member(client.user.id)
    # 记录提问者和问题
    logger.info(f"用户: {member}, 提问: {question}")
    try:
        # 获取回答
        answer = discord_bot.ask_bot(question)
        # 根据参数决定是否显示提问内容
        if args.include_question:
            response = f"> {question}\n\n{answer}"
        else:
            response = answer
        # 发送回答
        await interaction.followup.send(response)
    except Exception as e:
        # 如果出现问题，则发送错误提示
        await interaction.followup.send("发生了一个错误，请再试一次！")
        # 记录错误详情
        logger.error("在'提问'命令中出现错误:", e)

# 定义一个命令，用于向数据库添加新内容
@tree.command(name="add", description="向embedchain数据库添加新内容")
async def add_command(interaction: discord.Interaction, url_or_text: str):
    # 延迟响应以准备处理
    await interaction.response.defer()
    # 获取当前机器人的信息
    member = client.guilds[0].get_member(client.user.id)
    # 记录添加请求
    logger.info(f"用户: {member}, 添加: {url_or_text}")
    try:
        # 尝试添加内容
        response = discord_bot.add_data(url_or_text)
        # 发送确认信息
        await interaction.followup.send(response)
    except Exception as e:
        # 如果出现问题，则发送错误提示
        await interaction.followup.send("发生了一个错误，请再试一次！")
        # 记录错误详情
        logger.error("在'添加'命令中出现错误:", e)

# 定义一个简单的命令，用于测试机器人的响应
@tree.command(name="ping", description="简单的Ping-Pong命令")
async def ping(interaction: discord.Interaction):
    # 直接回复Pong
    await interaction.response.send_message("Pong", ephemeral=True)

# 处理命令执行时可能出现的错误
@tree.error

# 这是一个异步函数，当机器人接收到一个应用命令(app command)错误时会被调用。
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:

