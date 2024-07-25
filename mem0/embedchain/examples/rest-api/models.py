# 导入需要的一些工具包
from typing import Optional  # 用于定义某些变量可以是“没有值”的情况

from database import Base  # 这是从一个叫做 database 的文件里导入一个叫做 Base 的类，用于数据库的操作
from pydantic import BaseModel, Field  # 导入 BaseModel 和 Field 类，用来定义数据模型和字段描述
from sqlalchemy import Column, Integer, String  # 导入 Column、Integer 和 String 类，用来定义数据库中的列类型

# 定义了一个叫做 QueryApp 的类，它继承了 BaseModel
class QueryApp(BaseModel):
    query: str = Field("", description="The query that you want to ask the App.")  # 定义了一个叫做 query 的字段，类型是字符串，默认值是空字符串，描述是你想问应用的问题

    # 这个字典是告诉程序如何在 JSON 格式下展示这个类的信息
    model_config = {
        "json_schema_extra": {
            "example": {  # 这里提供了一个示例
                "query": "Who is Elon Musk?",  # 示例问题：谁是埃隆·马斯克？
            }
        }
    }

# 定义了一个叫做 SourceApp 的类，它继承了 BaseModel
class SourceApp(BaseModel):
    source: str = Field("", description="The source that you want to add to the App.")  # 定义了一个叫做 source 的字段，类型是字符串，默认值是空字符串，描述是你想添加到应用的数据来源
    data_type: Optional[str] = Field("", description="The type of data to add, remove it for autosense.")  # 定义了一个叫做 data_type 的字段，类型是可以为空的字符串，默认值是空字符串，描述是数据的类型，如果不填则自动识别

    # 这个字典是告诉程序如何在 JSON 格式下展示这个类的信息
    model_config = {"json_schema_extra": {"example": {"source": "https://en.wikipedia.org/wiki/Elon_Musk"}}}  # 这里提供了一个示例 URL

# 定义了一个叫做 DeployAppRequest 的类，它继承了 BaseModel
class DeployAppRequest(BaseModel):
    api_key: str = Field("", description="The Embedchain API key for App deployments.")  # 定义了一个叫做 api_key 的字段，类型是字符串，默认值是空字符串，描述是部署应用所需的 API 密钥

    # 这个字典是告诉程序如何在 JSON 格式下展示这个类的信息
    model_config = {"json_schema_extra": {"example": {"api_key": "ec-xxx"}}}  # 这里提供了一个示例 API 密钥

# 定义了一个叫做 MessageApp 的类，它继承了 BaseModel
class MessageApp(BaseModel):
    message: str = Field("", description="The message that you want to send to the App.")  # 定义了一个叫做 message 的字段，类型是字符串，默认值是空字符串，描述是你想发送给应用的消息

# 定义了一个叫做 DefaultResponse 的类，它继承了 BaseModel
class DefaultResponse(BaseModel):
    response: str  # 定义了一个叫做 response 的字段，类型是字符串，用于表示默认的响应内容

# 定义了一个叫做 AppModel 的类，它继承了 Base（从 database 文件里导入的那个）
class AppModel(Base):
    __tablename__ = "apps"  # 指定这个类对应的数据库表的名字是 "apps"

    id = Column(Integer, primary_key=True, index=True)  # 定义了一个叫做 id 的整数型字段，它是主键并且有索引
    app_id = Column(String, unique=True, index=True)  # 定义了一个叫做 app_id 的字符串型字段，它的值必须是唯一的，并且有索引
    config = Column(String, unique=True, index=True)  # 定义了一个叫做 config 的字符串型字段，它的值也必须是唯一的，并且有索引

