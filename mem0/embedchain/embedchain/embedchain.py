# 导入一个叫做 hashlib 的库，这个库用来创建唯一的标识符（像是文档的指纹）。
import hashlib
# 导入一个叫做 json 的库，用来处理像字典一样的数据结构，让它们可以在程序之间共享。
import json
# 导入一个叫做 logging 的库，帮助记录程序运行时的信息。
import logging
# 导入一个叫做 typing 的库里的 Any, Optional, Union 几个工具，这些工具可以让代码更清楚地告诉别人每个变量可以是什么类型。
from typing import Any, Optional, Union

# 从一个叫做 dotenv 的库导入 load_dotenv 工具，这个工具能帮我们加载环境变量，就像是游戏里的设置一样。
from dotenv import load_dotenv
# 从一个叫做 langchain 的库里的 docstore 模块导入 Document 类，这个类是用来表示文档的。
from langchain.docstore.document import Document

# 以下是从我们自己写的代码里导入的一些东西：
# 导入一些缓存相关的函数和类，就像是给程序加上记忆功能，记住之前做过的事情。
from embedchain.cache import adapt, get_gptcache_session, gptcache_data_convert, gptcache_update_cache_callback
# 导入 BaseChunker 这个类，它帮助把大段的文字拆成小块。
from embedchain.chunkers.base_chunker import BaseChunker
# 导入一些配置类，就像是设定游戏规则一样。
from embedchain.config import AddConfig, BaseLlmConfig, ChunkerConfig
# 再导入一个配置类，这个是关于应用的基本配置。
from embedchain.config.base_app_config import BaseAppConfig
# 导入两个模型类，它们是用来存储数据的，就像是游戏里的数据库。
from embedchain.core.db.models import ChatHistory, DataSource
# 导入一个数据格式化类，它帮助整理数据，让数据看起来更整齐。
from embedchain.data_formatter import DataFormatter
# 导入一个嵌入器基类，它负责理解文本的意思并转换成计算机容易比较的形式。
from embedchain.embedder.base import BaseEmbedder
# 导入一个基类，它帮助我们处理与语言模型的交互。
from embedchain.llm.base import BaseLlm
# 导入一个加载器基类，它帮助加载不同类型的数据。
from embedchain.loaders.base_loader import BaseLoader
# 导入一个数据类型枚举，它列出了所有支持的数据类型，就像是游戏里的物品类别。
from embedchain.models.data_type import DataType, DirectDataType, IndirectDataType, SpecialDataType
# 导入一个工具，它可以帮助检测数据的类型，就像是识别游戏里的物品。
from embedchain.utils.misc import detect_datatype, is_valid_json_string
# 导入一个向量数据库基类，它用来存储和检索数据的向量表示，就像是游戏里的地图系统。
from embedchain.vectordb.base import BaseVectorDB

# 加载环境变量，就像是读取游戏里的设置文件。
load_dotenv()

# 创建一个日志记录器，就像是游戏里的日记本，记录发生的事情。
logger = logging.getLogger(__name__)

# 定义一个类EmbedChain，它继承自JSONSerializable
class EmbedChain(JSONSerializable):
    # 初始化方法，设置实例属性
    def __init__(
        self,
        config: BaseAppConfig,  # 应用配置
        llm: BaseLlm,           # 大型语言模型实例
        db: BaseVectorDB = None,# 矢量数据库实例，默认为None
        embedder: BaseEmbedder = None,  # 嵌入器实例，默认为None
        system_prompt: Optional[str] = None,  # 系统提示，默认为None
    ):
        # 将传入的参数赋值给实例变量
        self.config = config
        self.cache_config = None
        self.memory_config = None
        self.mem0_memory = None
        # 设置语言模型实例
        self.llm = llm
        # 如果没有提供数据库或数据库配置无效，则抛出错误
        if db is None and (not hasattr(self.config, "db") or self.config.db is None):
            raise ValueError("App requires Database.")
        # 设置矢量数据库实例
        self.db = db or self.config.db
        # 如果没有提供嵌入器，则抛出错误
        if embedder is None:
            raise ValueError("App requires Embedder.")
        # 设置嵌入器实例
        self.embedder = embedder
        # 初始化数据库，设置嵌入器并初始化数据库
        self.db._set_embedder(self.embedder)
        self.db._initialize()
        # 根据应用配置设置集合名称
        if config.collection_name:
            self.db.set_collection_name(config.collection_name)
        # 如果提供了系统提示，更新语言模型的配置
        if system_prompt:
            self.llm.config.system_prompt = system_prompt
        # 从数据库中获取历史记录
        self.llm.update_history(app_id=self.config.id)
        # 初始化用户询问列表
        self.user_asks = []
        # 初始化分块器配置
        self.chunker: Optional[ChunkerConfig] = None

    # 属性收集指标，返回配置中的收集指标属性
    @property
    def collect_metrics(self):
        return self.config.collect_metrics

    # 设置收集指标属性，确保传入的是布尔值
    @collect_metrics.setter
    def collect_metrics(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"Boolean value expected but got {type(value)}.")
        self.config.collect_metrics = value

    # 属性在线状态，返回语言模型配置中的在线状态
    @property
    def online(self):
        return self.llm.config.online

    # 设置在线状态属性，确保传入的是布尔值
    @online.setter
    def online(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"Boolean value expected but got {type(value)}.")
        self.llm.config.online = value

    # 添加数据到矢量数据库的方法
    def add(
        self,
        source: Any,  # 数据源
        data_type: Optional[DataType] = None,  # 数据类型，默认为None
        metadata: Optional[dict[str, Any]] = None,  # 元数据，默认为None
        config: Optional[AddConfig] = None,  # 配置，默认为None
        dry_run=False,  # 干运行模式，默认为False
        loader: Optional[BaseLoader] = None,  # 加载器，默认为None
        chunker: Optional[BaseChunker] = None,  # 分块器，默认为None
        **kwargs: Optional[dict[str, Any]],  # 其他参数
    ):
        # ...（此处省略了方法体的详细注释，但逻辑与之前类似）
        # 这个方法主要负责加载、分块、嵌入数据，并将其存储到矢量数据库中。
        # 如果在干运行模式下，将返回分块信息而不实际存储数据。
        # 返回数据的MD5哈希值。

    # ...（后续方法的注释类似，涉及查询、搜索、重置、获取历史等操作）

    # 重置数据库，删除所有嵌入，但不需要重新初始化应用
    def reset(self):
        # ...（此处省略了方法体的详细注释）
        # 清空数据库和聊天历史记录。

    # 获取历史记录
    def get_history(
        self,
        num_rounds: int = 10,  # 轮数，默认为10
        display_format: bool = True,  # 显示格式，默认为True
        session_id: Optional[str] = "default",  # 会话ID，默认为"default"
        fetch_all: bool = False,  # 获取全部，默认为False
    ):
        # 返回历史记录
        history = self.llm.memory.get(
            app_id=self.config.id,
            session_id=session_id,
            num_rounds=num_rounds,
            display_format=display_format,
            fetch_all=fetch_all,
        )
        return history

    # 删除特定会话的聊天历史记录
    def delete_session_chat_history(self, session_id: str = "default"):
        # 删除指定会话的历史记录
        self.llm.memory.delete(app_id=self.config.id, session_id=session_id)
        self.llm.update_history(app_id=self.config.id)

    # 删除所有聊天历史记录
    def delete_all_chat_history(self, app_id: str):
        # 删除所有历史记录
        self.llm.memory.delete(app_id=app_id)
        self.llm.update_history(app_id=app_id)

    # 删除数据
    def delete(self, source_id: str):
        # 删除数据库中的数据
        # ...（此处省略了方法体的详细注释）

