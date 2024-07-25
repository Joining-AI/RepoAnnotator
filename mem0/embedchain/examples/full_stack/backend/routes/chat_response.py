# 导入我们需要的一些工具，就像是准备好我们的工具箱。
import os

# 这里我们从Flask这个大工具包里拿出Blueprint和其它几个小工具。
from flask import Blueprint, jsonify, make_response, request
# 我们还需要从models文件夹里拿出APIKey这个工具，它帮助我们管理密钥。
from models import APIKey
# 接下来是从paths文件夹中拿出DB_DIRECTORY_OPEN_AI，这是个路径，告诉我们数据存储在哪里。
from paths import DB_DIRECTORY_OPEN_AI

# 引入embedchain库中的App类，这是一个智能助手，可以帮我们处理问题。
from embedchain import App

# 创建一个名为"chat_response"的小程序蓝图，就像是规划一个小型游乐场的布局图。
chat_response_bp = Blueprint("chat_response", __name__)

# 定义一个路由，就像是告诉游乐场里的游客，有一个地方可以提问并得到答案。
@chat_response_bp.route("/api/get_answer", methods=["POST"])
def get_answer():
    # 尝试做下面的事情，如果出错会跳到except部分。
    try:
        # 先从游客那里接收信息，看看他们问了什么问题。
        data = request.get_json()
        # 从数据中找出游客的问题是什么。
        query = data.get("query")
        # 看看他们想要哪种模型来回答问题（比如，是不是要用OpenAI的模型）。
        embedding_model = data.get("embedding_model")
        # 再看看他们希望用哪种方式获取答案（比如，是用App方式）。
        app_type = data.get("app_type")

        # 如果他们选择的是OpenAI模型，我们就需要做一些准备。
        if embedding_model == "open_ai":
            # 首先，我们要切换到存储OpenAI数据的文件夹。
            os.chdir(DB_DIRECTORY_OPEN_AI)
            # 然后，我们从数据库中找出OpenAI的密钥。
            api_key = APIKey.query.first().key
            # 把这个密钥设置为环境变量，这样我们的智能助手就可以使用它了。
            os.environ["OPENAI_API_KEY"] = api_key
            # 如果他们选择的是App方式，我们就创建一个智能助手实例。
            if app_type == "app":
                chat_bot = App()

        # 现在，让我们的智能助手去回答游客的问题。
        response = chat_bot.chat(query)
        # 准备好答案，打包成一个响应，然后发送给游客。
        return make_response(jsonify({"response": response}), 200)

    # 如果在尝试过程中出现任何错误，我们会捕捉到这个错误。
    except Exception as e:
        # 把错误信息包装好，告诉游客出了什么问题。
        return make_response(jsonify({"error": str(e)}), 400)

