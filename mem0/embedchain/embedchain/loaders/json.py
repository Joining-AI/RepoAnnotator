# 导入所需的库
import hashlib  # 用于生成哈希值
import json     # 处理JSON数据
import os       # 文件操作
import re       # 正则表达式匹配
from typing import Union  # 类型注解

# 导入外部模块
import requests  # 发送HTTP请求

# 从其他文件导入类和函数
from embedchain.loaders.base_loader import BaseLoader  # 基础加载器类
from embedchain.utils.misc import clean_string, is_valid_json_string  # 清洗字符串和检查JSON字符串是否有效

# 定义了一个名为`JSONReader`的类，用于读取JSON数据
class JSONReader:
    def __init__(self) -> None:
        """初始化方法，这里没有做任何事情。"""
        pass

    # 这个静态方法用来从JSON结构中加载数据
    @staticmethod
    def load_data(json_data: Union[dict, str]) -> list[str]:
        """这个方法接收JSON数据（可以是字典或字符串形式），并返回其中的所有文本内容。

        参数:
            json_data (Union[dict, str]): 需要加载的JSON数据。

        返回:
            list[str]: 包含所有文本内容的列表。
        """
        # 如果输入的是字符串，则先尝试将它解析成字典
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        else:
            json_data = json_data

        # 将数据转为格式化的字符串
        json_output = json.dumps(json_data, indent=0)
        # 按行分割字符串
        lines = json_output.split("\n")
        # 筛选出有用的行（即不是空的或只有括号的行）
        useful_lines = [line for line in lines if not re.match(r"^[{}\[\],]*$", line)]
        # 将筛选后的行合并成一个字符串，并返回
        return ["\n".join(useful_lines)]

