# 导入需要的库
import json  # 这个库用来处理JSON数据，就像是处理一种特殊的文字游戏。
import logging  # 用来记录程序运行时发生了什么，就像写日记一样。
import os  # 用来处理文件和文件夹，就像是整理房间。
import time  # 用来处理时间，比如计时。
import uuid  # 生成独一无二的ID，就像是每个人都有自己的名字。
from typing import Any, Dict, Optional  # 用来定义变量可以是哪些类型。

# 导入一些特殊的工具和模型
from pydantic import BaseModel, Field, ValidationError  # 用于创建数据模型，就像是搭积木。
from mem0.llms.utils.tools import (  # 导入一些工具，用于操作记忆盒子。
    ADD_MEMORY_TOOL,  # 添加记忆的工具
    DELETE_MEMORY_TOOL,  # 删除记忆的工具
    UPDATE_MEMORY_TOOL,  # 更新记忆的工具
)
from mem0.configs.prompts import MEMORY_DEDUCTION_PROMPT  # 导入提示信息，帮助理解记忆内容。
from mem0.memory.base import MemoryBase  # 导入记忆的基础类。
from mem0.memory.setup import mem0_dir, setup_config  # 设置配置信息，就像是准备工具箱。
from mem0.memory.storage import SQLiteManager  # 使用SQLite数据库来保存历史记录。
from mem0.memory.telemetry import capture_event  # 记录重要的事件，就像是拍照片。
from mem0.memory.utils import get_update_memory_messages  # 获取更新记忆所需的信息。
from mem0.vector_stores.configs import VectorStoreConfig  # 矢量存储的配置信息。
from mem0.llms.configs import LlmConfig  # 语言模型的配置信息。
from mem0.embeddings.configs import EmbedderConfig  # 嵌入模型的配置信息。
from mem0.vector_stores.qdrant import Qdrant  # 特殊的矢量存储方式。
from mem0.utils.factory import LlmFactory, EmbedderFactory  # 创建语言模型和嵌入模型的工厂。

# 设置用户配置
setup_config()

# 定义一个记忆条目模型
class MemoryItem(BaseModel):  # 创建一个模型，就像是设计一个记忆卡片。
    id: str = Field(..., description="The unique identifier for the text data")  # 每个记忆卡片都有一个唯一的ID。
    text: str = Field(..., description="The text content")  # 卡片上会写有文本内容。
    # 元数据可以是任何类型的数据，不仅仅是字符串。这里先这样定义。
    metadata: Dict[str, Any] = Field(  # 卡片上还可以有一些额外的信息，叫做元数据。
        default_factory=dict, description="Additional metadata for the text data"
    )
    score: Optional[float] = Field(  # 卡片上的信息还可以有一个分数。
        None, description="The score associated with the text data"
    )

# 定义一个记忆配置模型
class MemoryConfig(BaseModel):  # 创建一个模型，用来配置整个记忆盒子。
    vector_store: VectorStoreConfig = Field(  # 配置矢量存储，就像是选择一个特别的柜子来放记忆卡片。
        description="Configuration for the vector store",
        default_factory=VectorStoreConfig,  # 默认使用一个标准的配置。
    )
    llm: LlmConfig = Field(  # 配置语言模型，就像是选择一个讲故事的人。
        description="Configuration for the language model",
        default_factory=LlmConfig,  # 默认使用一个标准的配置。
    )
    embedder: EmbedderConfig = Field(  # 配置嵌入模型，就像是选择一个特别的方法来制作记忆卡片。
        description="Configuration for the embedding model",
        default_factory=EmbedderConfig,  # 默认使用一个标准的配置。
    )
    history_db_path: str = Field(  # 设置历史记录数据库的位置。
        description="Path to the history database",
        default=os.path.join(mem0_dir, "history.db"),  # 默认位置是在某个特定文件夹里的`history.db`文件。
    )
    collection_name: str = Field(  # 设置记忆集合的名字。
        default="mem0", description="Name of the collection"
    )
    embedding_model_dims: int = Field(  # 设置嵌入模型的维度。
        default=1536, description="Dimensions of the embedding model"  # 默认是1536维。
    )

class Memory(MemoryBase):

