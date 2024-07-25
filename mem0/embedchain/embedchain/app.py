# 导入一些我们需要的库和模块
import ast
import concurrent.futures
import json
import logging
import os
from typing import Any, Optional, Union

# 导入用于网络请求的库
import requests
# 导入用于处理YAML文件的库
import yaml
# 导入进度条显示库，让程序看起来更酷炫
from tqdm import tqdm

# 导入我们自己的模块，这些是这个程序的一部分
from mem0 import Memory
# 以下是一些与缓存相关的模块，它们帮助我们存储和快速检索信息
from embedchain.cache import (
    Config,
    ExactMatchEvaluation,
    SearchDistanceEvaluation,
    cache,
    gptcache_data_manager,
    gptcache_pre_function,
)
# 客户端模块，用于与用户交互
from embedchain.client import Client
# 这里是配置模块，帮助我们设置程序的各种选项
from embedchain.config import AppConfig, CacheConfig, ChunkerConfig, Mem0Config
# 数据库相关模块，用于管理数据存储
from embedchain.core.db.database import get_session, init_db, setup_engine
# 数据源模型，帮助我们理解数据来自哪里
from embedchain.core.db.models import DataSource
# 这是我们主程序的一部分，用于处理文本嵌入
from embedchain.embedchain import EmbedChain
# 嵌入器模块，它将文本转换成计算机可以理解的形式
from embedchain.embedder.base import BaseEmbedder
# 具体的嵌入器实现，这里是使用OpenAI的
from embedchain.embedder.openai import OpenAIEmbedder
# 评价模块，用于评估结果的质量
from embedchain.evaluation.base import BaseMetric
# 具体的评价指标实现
from embedchain.evaluation.metrics import AnswerRelevance, ContextRelevance, Groundedness
# 工厂模式模块，帮助我们创建不同的组件
from embedchain.factory import EmbedderFactory, LlmFactory, VectorDBFactory
# 这个模块帮助我们处理JSON序列化，使数据可以在不同系统之间传递
from embedchain.helpers.json_serializable import register_deserializable
# 语言模型模块，用于生成和理解自然语言
from embedchain.llm.base import BaseLlm
# 具体的语言模型实现，这里是使用OpenAI的
from embedchain.llm.openai import OpenAILlm
# 向量数据库模块，用于高效地存储和检索向量数据
from embedchain.vectordb.base import BaseVectorDB
# 具体的向量数据库实现，这里是使用ChromaDB的
from embedchain.vectordb.chroma import ChromaDB

# 初始化日志记录器，这样我们可以跟踪程序的行为
logger = logging.getLogger(__name__)

# 注册可反序列化的类，这使得我们可以从JSON格式的数据中恢复对象
@register_deserializable

class App(EmbedChain):

