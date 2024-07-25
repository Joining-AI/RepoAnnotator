# 引入需要的库和模块
import argparse  # 这个库用于处理命令行参数
import logging   # 日志记录库，用于记录程序运行中的信息
import os        # 操作系统接口，用于访问环境变量等
from typing import Optional  # 类型注解，表示某项可以为None

# 引入自定义的模块，用于处理JSON序列化
from embedchain.helpers.json_serializable import register_deserializable 

# 引入基类Bot
from .base import BaseBot

# 尝试引入FastAPI Poe相关的库和函数
try:
    from fastapi_poe import PoeBot, run  # FastAPI PoeBot是聊天机器人的实现，run用于启动服务
except ModuleNotFoundError:  # 如果找不到所需的库
    # 抛出错误并告诉用户如何安装
    raise ModuleNotFoundError(
        "The required dependencies for Poe are not installed." 
        "Please install with `pip install fastapi-poe==0.0.16`"
    ) from None

# 定义一个函数，用于启动命令行界面
def start_command():
    parser = argparse.ArgumentParser(description="EmbedChain PoeBot command line interface")  # 创建解析器
    # 设置命令行参数：端口号，默认是8080
    parser.add_argument("--port", default=8080, type=int, help="Port to bind")
    # 设置命令行参数：Poe API的密钥
    parser.add_argument("--api-key", type=str, help="Poe API key")
    # 解析命令行参数
    args = parser.parse_args()

    # 使用解析到的参数或环境变量启动PoeBot
    run(PoeBot(), api_key=args.api_key or os.environ.get("POE_API_KEY"))

# 注册一个可反序列化的类
@register_deserializable
class PoeBot(BaseBot, PoeBot):  # 继承BaseBot和PoeBot类
    def __init__(self):  # 构造函数
        self.history_length = 5  # 聊天历史长度
        super().__init__()  # 调用父类构造函数

    # 获取响应的方法
    async def get_response(self, query):
        last_message = query.query[-1].content  # 最后一条消息的内容
        try:
            # 根据历史长度获取聊天历史
            history = [
                f"{m.role}: {m.content}" 
                for m in query.query[-(self.history_length + 1) : -1]
            ] if len(query.query) > 0 else None
        except Exception as e:
            # 如果处理历史时出错，记录错误并忽略历史
            logging.error(f"Error when processing the chat history. Message is being sent without history. Error: {e}")
        # 处理消息并生成响应
        answer = self.handle_message(last_message, history)
        yield self.text_event(answer)  # 生成响应事件

    # 处理消息的方法
    def handle_message(self, message, history=None):
        if message.startswith("/add "):  # 如果消息以"/add "开始，执行添加数据的操作
            response = self.add_data(message)
        else:  # 否则，询问机器人
            response = self.ask_bot(message, history)
        return response

    # 添加数据的方法（注释掉了，未实现）
    # def add_data(self, message):
    #     ...

    # 询问机器人的方法
    def ask_bot(self, message, history):
        try:
            # 设置历史记录并询问机器人
            self.app.llm.set_history(history=history)
            response = self.query(message)
        except Exception:
            # 如果出错，记录错误并返回错误信息
            logging.exception(f"Failed to query {message}.")
            response = "An error occurred. Please try again!"
        return response

    # 启动方法（调用start_command）
    def start(self):
        start_command()

# 如果文件被直接运行，而不是被导入，就启动命令行界面
if __name__ == "__main__":
    start_command()

