# 导入需要的库和模块
from dotenv import load_dotenv
# 这行代码导入了一个库，它能帮助我们从一个名为 .env 的文件中加载环境变量。

from fastapi import Body, FastAPI, responses
# 这里导入了 FastAPI 框架的一些组件，FastAPI 是一个现代的 Web 应用框架。
# `Body` 用于处理 HTTP 请求中的正文部分，
# `FastAPI` 用于创建应用实例，
# `responses` 用于发送响应给客户端。

from modal import Image, Secret, Stub, asgi_app
# 这里导入了一些库来帮助我们定义应用的运行环境，比如安装依赖、管理密钥等。

from embedchain import App
# 这行代码导入了一个叫 `embedchain` 的库，它提供了一个 `App` 类，用于构建应用程序。

load_dotenv(".env")
# 加载 .env 文件中的环境变量。

image = Image.debian_slim().pip_install(
    "embedchain",
    "lanchain_community==0.2.6",
    "youtube-transcript-api==0.6.1",
    "pytube==15.0.0",
    "beautifulsoup4==4.12.3",
    "slack-sdk==3.21.3",
    "huggingface_hub==0.23.0",
    "gitpython==3.1.38",
    "yt_dlp==2023.11.14",
    "PyGithub==1.59.1",
    "feedparser==6.0.10",
    "newspaper3k==0.2.8",
    "listparser==0.19",
)
# 定义了一个基础镜像，并在这个镜像上安装了一系列的 Python 包，这些包是应用程序需要用到的。

stub = Stub(
    name="embedchain-app",
    image=image,
    secrets=[Secret.from_dotenv(".env")],
)
# 创建了一个 `Stub` 对象，它代表了应用程序的配置，包括名称、镜像和密钥来源。

web_app = FastAPI()
# 创建了一个 FastAPI 实例，这是我们的 Web 应用的基础。

embedchain_app = App(name="embedchain-modal-app")
# 创建了一个 `embedchain` 的应用实例。

@web_app.post("/add")
async def add(
    source: str = Body(..., description="Source to be added"),
    data_type: str | None = Body(None, description="Type of the data source"),
):
    # 定义了一个处理 `/add` 路径的 POST 请求的异步函数。
    # 这个函数接受两个参数：`source` 和 `data_type`。
    # `source` 表示要添加的数据源，`data_type` 表示数据源的类型（可选）。

    if source and data_type:
        embedchain_app.add(source, data_type)
    # 如果 `source` 和 `data_type` 都有值，就调用 `embedchain_app` 的 `add` 方法添加数据源。

    elif source:
        embedchain_app.add(source)
    # 如果只有 `source` 有值，也调用 `add` 方法添加数据源，但不指定类型。

    else:
        return {"message": "No source provided."}
    # 如果 `source` 没有值，则返回一个错误信息。

    return {"message": f"Source '{source}' added successfully."}
    # 如果一切正常，返回一个成功消息。

@web_app.post("/query")
async def query(question: str = Body(..., description="Question to be answered")):
    # 定义了一个处理 `/query` 路径的 POST 请求的异步函数。
    # 这个函数接受一个参数 `question`，表示用户提出的问题。

    if not question:
        return {"message": "No question provided."}
    # 如果没有问题，返回一个错误信息。

    answer = embedchain_app.query(question)
    # 否则，调用 `embedchain_app` 的 `query` 方法来获取答案。

    return {"answer": answer}
    # 返回答案。

@web_app.get("/chat")
async def chat(question: str = Body(..., description="Question to be answered")):
    # 定义了一个处理 `/chat` 路径的 GET 请求的异步函数。
    # 这个函数同样接受一个问题 `question`。

    if not question:
        return {"message": "No question provided."}
    # 如果没有问题，返回一个错误信息。

    response = embedchain_app.chat(question)
    # 否则，调用 `embedchain_app` 的 `chat` 方法来获取回复。

    return {"response": response}
    # 返回回复。

@web_app.get("/")
async def root():
    return responses.RedirectResponse(url="/docs")
# 定义了一个处理根路径 `/` 的 GET 请求的异步函数。
# 当访问根路径时，会自动重定向到文档页面。

@stub.function(image=image)
@asgi_app()
def fastapi_app():
    return web_app
# 这里定义了一个函数，该函数将我们的 `web_app` 返回出去。
# 使用了装饰器来配置函数的运行环境，并使其能够与外部服务交互。

