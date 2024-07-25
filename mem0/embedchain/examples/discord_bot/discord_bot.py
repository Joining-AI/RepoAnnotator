# 导入需要的库
import os
# 这里导入了Python中用来操作环境变量的库，可以让我们从系统环境中读取一些配置信息。

import discord
# 导入discord库，这是用来和Discord服务器通信的库。

from discord.ext import commands
# 导入commands模块，这让我们能够更方便地给机器人添加命令。

from dotenv import load_dotenv
# 导入dotenv库中的load_dotenv函数，这个库可以帮助我们加载.env文件中的环境变量。

from embedchain import App
# 导入embedchain库中的App类，这个库提供了一些处理文本和链接的功能，用于我们的聊天机器人。

load_dotenv()
# 调用load_dotenv()函数，它会加载当前目录下的.env文件里的环境变量。

intents = discord.Intents.default()
intents.message_content = True
# 初始化intents对象，告诉Discord我们需要读取消息内容的权限。

bot = commands.Bot(command_prefix="/ec ", intents=intents)
# 创建一个Bot实例，设置命令前缀为"/ec "，并赋予它上面定义的权限。

root_folder = os.getcwd()
# 获取当前工作目录，并存储在root_folder变量中。

def initialize_chat_bot():
    global chat_bot
    chat_bot = App()
# 定义一个函数initialize_chat_bot，这个函数创建了一个embedchain的App实例，并将其赋值给chat_bot变量。

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    initialize_chat_bot()
# 当机器人准备好时，打印登录成功的消息，并初始化聊天机器人。

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await send_response(ctx, "Invalid command. Please refer to the documentation for correct syntax.")
    else:
        print("Error occurred during command execution:", error)
# 如果机器人遇到错误，这个函数会被调用。如果是找不到命令的错误，就发送一条消息告诉用户；其他类型的错误则打印出来。

@bot.command()
async def add(ctx, data_type: str, *, url_or_text: str):
    print(f"User: {ctx.author.name}, Data Type: {data_type}, URL/Text: {url_or_text}")
    try:
        chat_bot.add(data_type, url_or_text)
        await send_response(ctx, f"Added {data_type} : {url_or_text}")
    except Exception as e:
        await send_response(ctx, f"Failed to add {data_type} : {url_or_text}")
        print("Error occurred during 'add' command:", e)
# 定义一个名为add的命令，接收数据类型（比如网站链接或文本）和要处理的数据。尝试将数据添加到chat_bot中，并告诉用户结果。

@bot.command()
async def query(ctx, *, question: str):
    print(f"User: {ctx.author.name}, Query: {question}")
    try:
        response = chat_bot.query(question)
        await send_response(ctx, response)
    except Exception as e:
        await send_response(ctx, "An error occurred. Please try again!")
        print("Error occurred during 'query' command:", e)
# 定义一个名为query的命令，接收一个问题，然后尝试从chat_bot中获取答案并返回给用户。

@bot.command()
async def chat(ctx, *, question: str):
    print(f"User: {ctx.author.name}, Query: {question}")
    try:
        response = chat_bot.chat(question)
        await send_response(ctx, response)
    except Exception as e:
        await send_response(ctx, "An error occurred. Please try again!")
        print("Error occurred during 'chat' command:", e)
# 和上面的query命令类似，但是这里使用chat_bot的chat方法。

async def send_response(ctx, message):
    if ctx.guild is None:
        await ctx.send(message)
    else:
        await ctx.reply(message)
# 这个函数用来发送消息。如果消息是在私聊中，则直接发送；如果是在服务器频道，则回复原消息。

bot.run(os.environ["DISCORD_BOT_TOKEN"])
# 使用环境变量中的DISCORD_BOT_TOKEN启动机器人。

