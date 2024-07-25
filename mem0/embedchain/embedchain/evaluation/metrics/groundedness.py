# 导入一些可以同时运行多个任务的工具
import concurrent.futures

# 导入日志记录模块，用来记录程序运行过程中的信息
import logging

# 导入操作系统相关的功能，比如读取环境变量等
import os

# 导入处理字符串模板的库，可以方便地替换字符串中的占位符
from string import Template

# 导入类型提示，帮助代码阅读者理解变量的类型
from typing import Optional

# 导入numpy库，这是一个强大的数学计算库
import numpy as np

# 导入OpenAI的API客户端，用于与OpenAI的模型进行交互
from openai import OpenAI

# 导入进度条模块，可以让程序显示任务的完成进度
from tqdm import tqdm

# 导入嵌链（embedchain）项目中关于评估配置的基类
from embedchain.config.evaluation.base import GroundednessConfig

# 导入嵌链项目中关于评估的基类
from embedchain.evaluation.base import BaseMetric

# 导入嵌链项目中关于评估数据和指标的一些实用函数
from embedchain.utils.evaluation import EvalData, EvalMetric

# 创建一个日志记录器，用来记录这个模块的日志信息
logger = logging.getLogger(__name__)

