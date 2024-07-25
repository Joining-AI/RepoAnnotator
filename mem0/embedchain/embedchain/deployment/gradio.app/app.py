# 这行代码是告诉电脑我们要使用操作系统的一些功能。
import os

# 这里我们告诉电脑，我们要用到一个叫做gradio的工具，它能帮助我们在网页上创建对话框。
import gradio as gr

# 我们还需要用到一个叫embedchain的工具，它能帮我们处理和理解文字信息。
from embedchain import App

# 下面这行代码是在设置一个秘密钥匙，这个钥匙是用来访问一个叫OpenAI的服务的。这里我们用"sk-xxx"代替了真实的钥匙，因为真实钥匙需要保密。
os.environ["OPENAI_API_KEY"] = "sk-xxx"

# 这里我们创建了一个App对象，它是用来处理和理解我们输入的文字的。
app = App()

# 定义一个函数，名字叫做query。这个函数接收两个参数：message（消息）和history（历史记录）。
def query(message, history):
    # 函数做的事情很简单，就是把message（消息）传给前面创建的app，然后返回app处理后的结果。
    return app.chat(message)

# 这里我们创建了一个演示界面，它会使用上面定义的query函数来处理用户在聊天框里输入的信息。
demo = gr.ChatInterface(query)

# 最后，我们运行这个演示界面，这样我们就可以在网页上看到聊天框并且开始聊天了。
demo.launch()

