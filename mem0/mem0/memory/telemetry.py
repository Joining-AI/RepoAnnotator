# 导入一些工具库
import platform
import sys

# 导入Posthog这个库用来发送数据
from posthog import Posthog

# 导入自定义的一些函数和配置
from mem0.memory.setup import get_user_id, setup_config


# 定义了一个叫做AnonymousTelemetry的类
class AnonymousTelemetry:
    # 初始化函数，当创建这个类的对象时会自动运行
    def __init__(self, project_api_key, host):
        # 创建Posthog对象并保存在这个类的一个属性里
        self.posthog = Posthog(project_api_key=project_api_key, host=host)
        # 调用setup_config函数确保用户ID已经生成
        setup_config()
        # 获取用户的ID并保存在self.user_id里
        self.user_id = get_user_id()

    # 这个函数用来记录事件
    def capture_event(self, event_name, properties=None):
        # 如果没有传入属性，则创建一个空字典
        if properties is None:
            properties = {}
        # 添加一些系统信息到属性中
        properties = {
            "python_version": sys.version,  # Python版本
            "os": sys.platform,  # 操作系统类型
            "os_version": platform.version(),  # 操作系统版本
            "os_release": platform.release(),  # 操作系统发行版
            "processor": platform.processor(),  # 处理器信息
            "machine": platform.machine(),  # 硬件架构
            **properties,  # 合并之前可能有的属性
        }
        # 使用Posthog对象记录事件
        self.posthog.capture(
            distinct_id=self.user_id,  # 用户ID
            event=event_name,  # 事件名称
            properties=properties  # 事件属性
        )

    # 这个函数用来标识用户
    def identify_user(self, user_id, properties=None):
        # 如果没有传入属性，则创建一个空字典
        if properties is None:
            properties = {}
        # 使用Posthog对象标识用户
        self.posthog.identify(distinct_id=user_id, properties=properties)

    # 这个函数用来关闭Posthog连接
    def close(self):
        self.posthog.shutdown()


# 创建一个AnonymousTelemetry类的实例
telemetry = AnonymousTelemetry(
    project_api_key="phc_hgJkUVJFYtmaJqrvf6CYN67TIQ8yhXAkWzUn9AMU4yX",  # 项目API密钥
    host="https://us.i.posthog.com",  # 数据服务器地址
)


# 这个函数用来捕捉与内存实例相关的事件
def capture_event(event_name, memory_instance, additional_data=None):
    # 创建一个包含内存实例信息的字典
    event_data = {
        "collection": memory_instance.collection_name,  # 集合名称
        "vector_size": memory_instance.embedding_model.dims,  # 向量大小
        "history_store": "sqlite",  # 历史存储方式
        "vector_store": f"{memory_instance.vector_store.__class__.__module__}.{memory_instance.vector_store.__class__.__name__}",  # 向量存储类的信息
        "llm": f"{memory_instance.llm.__class__.__module__}.{memory_instance.llm.__class__.__name__}",  # 语言模型类的信息
        "embedding_model": f"{memory_instance.embedding_model.__class__.__module__}.{memory_instance.embedding_model.__class__.__name__}",  # 嵌入模型类的信息
        "function": f"{memory_instance.__class__.__module__}.{memory_instance.__class__.__name__}",  # 内存实例类的信息
    }
    # 如果有额外的数据，则合并进event_data
    if additional_data:
        event_data.update(additional_data)

    # 使用telemetry对象记录事件
    telemetry.capture_event(event_name, event_data)


# 这个函数用来捕捉与客户端实例相关的事件
def capture_client_event(event_name, instance, additional_data=None):
    # 创建一个包含客户端实例信息的字典
    event_data = {
        "function": f"{instance.__class__.__module__}.{instance.__class__.__name__}",  # 客户端实例类的信息
    }
    # 如果有额外的数据，则合并进event_data
    if additional_data:
        event_data.update(additional_data)

    # 使用telemetry对象记录事件
    telemetry.capture_event(event_name, event_data)

