# 导入我们需要的模块
from fastapi import FastAPI, responses  # 从FastAPI这个工具包里导入创建应用和响应重定向的功能
from pydantic import BaseModel  # 从pydantic包里导入BaseModel类，用于定义数据模型
from embedchain import App  # 从embedchain包里导入App类，用于创建嵌入式应用实例

# 创建一个FastAPI应用实例
app = FastAPI(title="Embedchain FastAPI App")  # 这行代码创建了一个新的FastAPI应用，并给它起了个名字
embedchain_app = App()  # 创建一个embedchain的应用实例

# 定义一个数据模型，用来表示数据源
class SourceModel(BaseModel):  # 这里我们定义了一个名为SourceModel的数据模型
    source: str  # 数据模型包含一个字符串类型的字段source，用来存储数据源信息

# 定义一个数据模型，用来表示问题
class QuestionModel(BaseModel):  # 这里我们定义了一个名为QuestionModel的数据模型
    question: str  # 数据模型包含一个字符串类型的字段question，用来存储问题

# 定义一个处理添加数据源的接口
@app.post("/add")  # 声明一个处理POST请求的路由，路径是"/add"
async def add_source(source_model: SourceModel):  # 定义一个异步函数add_source，参数是SourceModel类型的source_model
    """
    添加一个新的数据源到embedchain应用。
    需要一个JSON格式的数据，里面包含一个"source"键。
    """
    source = source_model.source  # 从传入的source_model中获取source字段的值
    embedchain_app.add(source)  # 把数据源添加到embedchain应用中
    return {"message": f"Source '{source}' added successfully."}  # 返回一个成功消息

# 定义一个处理查询请求的接口
@app.post("/query")  # 声明一个处理POST请求的路由，路径是"/query"
async def handle_query(question_model: QuestionModel):  # 定义一个异步函数handle_query，参数是QuestionModel类型的question_model
    """
    处理对embedchain应用的查询请求。
    需要一个JSON格式的数据，里面包含一个"question"键。
    """
    question = question_model.question  # 从传入的question_model中获取question字段的值
    answer = embedchain_app.query(question)  # 通过embedchain应用查询问题并获得答案
    return {"answer": answer}  # 返回答案

# 定义一个处理聊天请求的接口
@app.post("/chat")  # 声明一个处理POST请求的路由，路径是"/chat"
async def handle_chat(question_model: QuestionModel):  # 定义一个异步函数handle_chat，参数是QuestionModel类型的question_model
    """
    处理对embedchain应用的聊天请求。
    需要一个JSON格式的数据，里面包含一个"question"键。
    """
    question = question_model.question  # 从传入的question_model中获取question字段的值
    response = embedchain_app.chat(question)  # 通过embedchain应用处理聊天请求并获得回应
    return {"response": response}  # 返回回应

# 定义应用的根路径
@app.get("/")  # 声明一个处理GET请求的路由，路径是"/"
async def root():  # 定义一个异步函数root
    return responses.RedirectResponse(url="/docs")  # 将访问根路径的用户重定向到"/docs"页面

