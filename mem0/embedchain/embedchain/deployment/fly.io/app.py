# 导入环境变量加载模块
from dotenv import load_dotenv
# 导入FastAPI框架和响应模块
from fastapi import FastAPI, responses
# 导入Pydantic中的BaseModel类，用于定义数据模型
from pydantic import BaseModel

# 导入embedchain应用模块
from embedchain import App

# 加载.env文件中的环境变量
load_dotenv(".env")

# 创建一个FastAPI应用实例，并给它起个名字叫 "Embedchain FastAPI App"
app = FastAPI(title="Embedchain FastAPI App")
# 创建一个embedchain应用实例
embedchain_app = App()

# 定义一个数据模型SourceModel，里面有一个字段叫source
class SourceModel(BaseModel):
    source: str

# 定义一个数据模型QuestionModel，里面有一个字段叫question
class QuestionModel(BaseModel):
    question: str

# 定义一个名为"/add"的POST接口
@app.post("/add")
async def add_source(source_model: SourceModel):
    """
    这个函数处理"/add"请求。
    需要接收一个JSON格式的数据，里面包含一个"source"键。
    然后会把这个数据添加到embedchain应用中。
    """
    # 从传入的参数source_model中获取source字段的值
    source = source_model.source
    # 把source添加到embedchain应用中
    embedchain_app.add(source)
    # 返回一条消息告诉用户数据添加成功
    return {"message": f"Source '{source}' added successfully."}

# 定义一个名为"/query"的POST接口
@app.post("/query")
async def handle_query(question_model: QuestionModel):
    """
    这个函数处理"/query"请求。
    需要接收一个JSON格式的数据，里面包含一个"question"键。
    根据问题查询embedchain应用并返回答案。
    """
    # 从传入的参数question_model中获取question字段的值
    question = question_model.question
    # 向embedchain应用询问问题并获取答案
    answer = embedchain_app.query(question)
    # 把答案返回给用户
    return {"answer": answer}

# 定义一个名为"/chat"的POST接口
@app.post("/chat")
async def handle_chat(question_model: QuestionModel):
    """
    这个函数处理"/chat"请求。
    需要接收一个JSON格式的数据，里面包含一个"question"键。
    根据问题与embedchain应用进行聊天并返回回复。
    """
    # 从传入的参数question_model中获取question字段的值
    question = question_model.question
    # 向embedchain应用发送问题并获取回复
    response = embedchain_app.chat(question)
    # 把回复返回给用户
    return {"response": response}

# 定义一个名为"/"的GET接口（首页）
@app.get("/")
async def root():
    # 当访问首页时，自动重定向到文档页面
    return responses.RedirectResponse(url="/docs")

