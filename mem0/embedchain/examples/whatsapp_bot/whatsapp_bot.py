# 引入Flask库，用于创建Web应用
from flask import Flask, request
# 引入Twilio的库，用于处理短信消息
from twilio.twiml.messaging_response import MessagingResponse

# 引入embedchain库，用于创建聊天机器人
from embedchain import App

# 创建一个Flask应用实例
app = Flask(__name__)
# 创建一个聊天机器人实例
chat_bot = App()

# 定义一个路由，当收到POST请求到"/chat"时，会运行下面的函数
@app.route("/chat", methods=["POST"])
def chat():
    # 获取用户发送的短信内容，并转换成小写
    incoming_message = request.values.get("Body", "").lower()
    # 处理接收到的消息，得到回复
    response = handle_message(incoming_message)
    # 创建一个Twilio的回复对象
    twilio_response = MessagingResponse()
    # 向用户发送回复消息
    twilio_response.message(response)
    # 将回复消息转换成字符串返回
    return str(twilio_response)

# 这个函数用来处理用户的消息
def handle_message(message):
    # 如果消息以"add "开始，就调用add_sources函数处理
    if message.startswith("add "):
        response = add_sources(message)
    # 否则，调用query函数来回答问题
    else:
        response = query(message)
    # 返回处理后的回复
    return response

# 这个函数用来添加数据源给聊天机器人
def add_sources(message):
    # 分割消息，获取数据类型和URL或文本
    message_parts = message.split(" ", 2)
    # 检查是否分割得到了三部分
    if len(message_parts) == 3:
        data_type = message_parts[1]
        url_or_text = message_parts[2]
        # 尝试添加数据源
        try:
            chat_bot.add(data_type, url_or_text)
            # 如果成功，返回确认信息
            response = f"Added {data_type}: {url_or_text}"
        # 如果出错，返回错误信息
        except Exception as e:
            response = f"Failed to add {data_type}: {url_or_text}.\nError: {str(e)}"
    # 如果消息格式不对，给出提示
    else:
        response = "Invalid 'add' command format.\nUse: add <data_type> <url_or_text>"
    # 返回处理结果
    return response

# 这个函数用来查询并回答用户的问题
def query(message):
    # 尝试回答问题
    try:
        response = chat_bot.chat(message)
    # 如果出错，给出通用错误信息
    except Exception:
        response = "An error occurred. Please try again!"
    # 返回回答
    return response

# 如果直接运行这个脚本，启动Flask应用
if __name__ == "__main__":
    # 设置监听所有IP地址，端口8000，关闭调试模式
    app.run(host="0.0.0.0", port=8000, debug=False)

