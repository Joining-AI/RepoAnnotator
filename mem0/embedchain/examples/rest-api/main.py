# 导入日志模块
import logging
# 导入操作系统模块
import os

# 导入异步文件操作模块
import aiofiles
# 导入YAML数据处理模块
import yaml
# 从database模块导入数据库基类、本地会话和引擎
from database import Base, SessionLocal, engine
# 从fastapi框架导入依赖项管理器、FastAPI应用、HTTP异常和上传文件模型
from fastapi import Depends, FastAPI, HTTPException, UploadFile
# 从models模块导入默认响应、部署应用请求、查询应用和源应用模型
from models import DefaultResponse, DeployAppRequest, QueryApp, SourceApp
# 从services模块导入获取应用、获取所有应用、移除应用和保存应用的服务函数
from services import get_app, get_apps, remove_app, save_app
# 从SQLAlchemy ORM导入会话管理器
from sqlalchemy.orm import Session
# 从utils模块导入生成API密钥错误信息的工具函数
from utils import generate_error_message_for_api_keys

# 导入embedchain应用和客户端模块
from embedchain import App
from embedchain.client import Client

# 配置日志记录器
logger = logging.getLogger(__name__)

# 使用数据库引擎创建所有表结构
Base.metadata.create_all(bind=engine)


# 定义一个生成数据库会话的函数
def get_db():
    # 创建一个新的数据库会话
    db = SessionLocal()
    try:
        # 返回会话对象以供使用（使用yield关键字）
        yield db
    finally:
        # 确保在使用后关闭会话
        db.close()


# 初始化FastAPI应用，设置标题、描述、版本和许可证信息
app = FastAPI(
    title="Embedchain REST API",
    description="这是Embedchain的REST API。",
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://github.com/embedchain/embedchain/blob/main/LICENSE",
    },
)


# 定义一个检查API状态的路由
@app.get("/ping", tags=["Utility"])
def check_status():
    """
    检查API是否正常运行。
    """
    # 返回一个简单的响应，表示API正常
    return {"ping": "pong"}


# 定义一个获取所有应用的路由
@app.get("/apps", tags=["Apps"])
async def get_all_apps(db: Session = Depends(get_db)):
    """
    获取所有应用的信息。
    """
    # 调用服务函数获取所有应用
    apps = get_apps(db)
    # 将应用列表包装成响应格式返回
    return {"results": apps}


# 定义一个创建新应用的路由
@app.post("/create", tags=["Apps"], response_model=DefaultResponse)
async def create_app_using_default_config(app_id: str, config: UploadFile = None, db: Session = Depends(get_db)):
    """
    使用提供的ID创建新的应用。如果没有提供配置文件，将使用默认配置。
    app_id: 应用的唯一标识符。
    config: 可选的YAML配置文件。
    """
    try:
        # 如果没有提供app_id，抛出错误
        if app_id is None:
            raise HTTPException(detail="未提供应用ID。", status_code=400)

        # 如果应用已经存在，抛出错误
        if get_app(db, app_id) is not None:
            raise HTTPException(detail=f"ID为'{app_id}'的应用已存在。", status_code=400)

        # 默认配置文件路径
        yaml_path = "default.yaml"
        # 如果提供了配置文件
        if config is not None:
            # 读取配置文件内容
            contents = await config.read()
            try:
                # 解析YAML数据，确保格式正确
                yaml.safe_load(contents)
                # TODO: 在这里验证配置文件
                # 设置自定义配置文件路径
                yaml_path = f"configs/{app_id}.yaml"
                # 异步写入配置文件到磁盘
                async with aiofiles.open(yaml_path, mode="w") as file_out:
                    await file_out.write(str(contents, "utf-8"))
            except yaml.YAMLError as exc:
                # 如果解析YAML失败，抛出错误
                raise HTTPException(detail=f"解析YAML时出错: {exc}", status_code=400)

        # 保存应用到数据库
        save_app(db, app_id, yaml_path)

        # 返回成功创建应用的响应
        return DefaultResponse(response=f"应用创建成功。应用ID: {app_id}")
    except Exception as e:
        # 记录异常信息
        logger.warning(str(e))
        # 抛出HTTP异常，包含错误信息
        raise HTTPException(detail=f"创建应用时出错: {str(e)}", status_code=400)


# 定义一个获取特定应用数据的路由（代码片段被截断，未完全展示）
@app.get(
    "/{app_id}/data",
    tags=["Apps"],
)

# 这个函数帮我们找到与某个应用关联的所有数据源。
async def get_datasources_associated_with_app_id(app_id: str, db: Session = Depends(get_db)):
    """
    获取某个应用的所有数据源。
    app_id: 应用的ID。如果要找默认的应用，就用 "default"。
    """
    # 如果没有给定 app_id，会提示错误信息。
    try:
        if app_id is None:
            raise HTTPException(
                detail="没有提供应用ID哦。如果你想用默认的应用，记得写 'default'。",
                status_code=400,  # 这个数字表示错误类型，400 意味着请求有问题。
            )

        db_app = get_app(db, app_id)  # 从数据库中查找应用的信息。

        if db_app is None:
            # 如果找不到应用，也会提示错误信息。
            raise HTTPException(detail=f"找不到ID为 {app_id} 的应用，请先创建它。",
                                status_code=400)

        app = App.from_config(config_path=db_app.config)  # 根据配置创建应用对象。

        response = app.get_data_sources()  # 通过应用对象获取所有数据源。
        return {"results": response}  # 把数据源作为结果返回。
    # 如果遇到一些特定的错误，比如值错误（ValueError），就会记录错误并提示用户。
    except ValueError as ve:
        logger.warning(str(ve))  # 记录错误信息。
        raise HTTPException(
            detail=generate_error_message_for_api_keys(ve),  # 生成更详细的错误提示。
            status_code=400,
        )
    # 如果遇到其他任何错误，同样记录并提示。
    except Exception as e:
        logger.warning(str(e))
        raise HTTPException(detail=f"出错了：{str(e)}", status_code=400)

# 下面的函数用来向现有的应用添加数据源。
@app.post(
    "/{app_id}/add",
    tags=["Apps"],
    response_model=DefaultResponse,  # 定义返回的数据格式。
)
async def add_datasource_to_an_app(body: SourceApp, app_id: str, db: Session = Depends(get_db)):
    """
    向现有应用添加数据源。
    app_id: 应用的ID。如果要找默认的应用，就用 "default"。
    source: 要添加的数据源。
    data_type: 数据源的类型。如果不指定，系统会自动检测。
    """
    try:
        if app_id is None:
            raise HTTPException(
                detail="没有提供应用ID哦。如果你想用默认的应用，记得写 'default'。",
                status_code=400,
            )

        db_app = get_app(db, app_id)  # 从数据库中查找应用的信息。

        if db_app is None:
            raise HTTPException(detail=f"找不到ID为 {app_id} 的应用，请先创建它。",
                                status_code=400)

        app = App.from_config(config_path=db_app.config)  # 根据配置创建应用对象。

        response = app.add(source=body.source, data_type=body.data_type)  # 添加数据源到应用。
        return DefaultResponse(response=response)  # 返回添加结果。
    # 错误处理部分和上面的函数类似。
    except ValueError as ve:
        logger.warning(str(ve))
        raise HTTPException(
            detail=generate_error_message_for_api_keys(ve),
            status_code=400,
        )
    except Exception as e:
        logger.warning(str(e))
        raise HTTPException(detail=f"出错了：{str(e)}", status_code=400)

# 最后一个函数允许我们向应用提问。
@app.post(
    "/{app_id}/query",
    tags=["Apps"],
    response_model=DefaultResponse,  # 定义返回的数据格式。
)
async def query_an_app(body: QueryApp, app_id: str, db: Session = Depends(get_db)):
    """
    向现有应用提问。
    app_id: 应用的ID。如果要找默认的应用，就用 "default"。
    query: 提问的内容。
    """
    try:
        if app_id is None:
            raise HTTPException(
                detail="没有提供应用ID哦。如果你想用默认的应用，记得写 'default'。",
                status_code=400,
            )

        db_app = get_app(db, app_id)  # 从数据库中查找应用的信息。

        if db_app is None:
            raise HTTPException(detail=f"找不到ID为 {app_id} 的应用，请先创建它。",
                                status_code=400)

        app = App.from_config(config_path=db_app.config)  # 根据配置创建应用对象。

        response = app.query(body.query)  # 向应用提问。
        return DefaultResponse(response=response)  # 返回提问的结果。
    # 错误处理部分和前面的函数相似。
    except ValueError as ve:
        logger.warning(str(ve))
        raise HTTPException(
            detail=generate_error_message_for_api_keys(ve),
            status_code=400,
        )
    except Exception as e:
        logger.warning(str(e))
        raise HTTPException(detail=f"出错了：{str(e)}", status_code=400)

