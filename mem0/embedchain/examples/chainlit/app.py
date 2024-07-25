# 导入需要的模块
import os
# 导入chainlit这个库，它可以帮助我们快速建立聊天应用
import chainlit as cl
# 导入embedchain库中的App类，它可以帮助我们处理文本和生成回复
from embedchain import App

# 设置环境变量，这里设置了一个叫OPENAI_API_KEY的密钥，用于调用OpenAI的服务
os.environ["OPENAI_API_KEY"] = "sk-xxx"

# 定义一个函数，当聊天开始时会被调用
@cl.on_chat_start
async def on_chat_start():
    # 创建一个App对象，并通过传递一个配置字典来初始化它
    app = App.from_config(
        # 配置字典
        config={
            # 应用的基本配置
            "app": {"config": {"name": "chainlit-app"}},
            # 语言模型的配置
            "llm": {
                "config": {
                    # 是否启用流式传输（即逐步显示回复）
                    "stream": True,
                }
            },
        }
    )
    # 导入数据到应用中，这里是从一个网页导入数据
    app.add("https://www.forbes.com/profile/elon-musk/")
    # 禁用收集应用性能指标的功能
    app.collect_metrics = False
    # 把创建的应用对象保存到用户的会话中，方便后面使用
    cl.user_session.set("app", app)

# 定义一个函数，每当收到消息时会被调用
@cl.on_message
async def on_message(message: cl.Message):
    # 从用户会话中获取之前保存的应用对象
    app = cl.user_session.get("app")
    # 创建一个新的消息对象，用来发送回复
    msg = cl.Message(content="")
    # 通过应用对象获取回复，这里使用了异步的方式
    for chunk in await cl.make_async(app.chat)(message.content):
        # 逐步发送每个回复片段
        await msg.stream_token(chunk)

    # 发送完整的消息
    await msg.send()

