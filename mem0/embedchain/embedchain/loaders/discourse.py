# 导入一些需要的库
import hashlib
import logging
import time
from typing import Any, Optional

import requests

# 导入这个项目里其他自己写的代码
from embedchain.loaders.base_loader import BaseLoader
from embedchain.utils.misc import clean_string

# 设置日志系统，方便记录程序运行过程中的信息
logger = logging.getLogger(__name__)

# 定义一个类，名字叫 DiscourseLoader，专门用来从 Discourse 论坛加载数据
class DiscourseLoader(BaseLoader):
    # 初始化函数，创建这个类的对象时会自动运行
    def __init__(self, config: Optional[dict[str, Any]] = None):
        # 调用父类的初始化方法
        super().__init__()
        # 如果没有提供配置信息，则报错
        if not config:
            raise ValueError(
                "DiscourseLoader 需要一个配置文件。请查看文档以获取正确的格式 - `https://docs.embedchain.ai/components/data-sources/discourse`"
            )
        
        # 从配置文件中获取论坛的域名
        self.domain = config.get("domain")
        # 如果没有域名也报错
        if not self.domain:
            raise ValueError(
                "DiscourseLoader 需要一个域名。请查看文档以获取正确的格式 - `https://docs.embedchain.ai/components/data-sources/discourse`"
            )

    # 检查查询字符串是否正确
    def _check_query(self, query):
        # 如果查询为空或者不是字符串类型，就报错
        if not query or not isinstance(query, str):
            raise ValueError(
                "DiscourseLoader 需要一个查询字符串。请查看文档以获取正确的格式 - `https://docs.embedchain.ai/components/data-sources/discourse`"
            )

    # 加载单个帖子的内容
    def _load_post(self, post_id):
        # 构造帖子的 URL
        post_url = f"{self.domain}posts/{post_id}.json"
        # 发送 HTTP 请求获取帖子内容
        response = requests.get(post_url)
        try:
            # 如果请求成功则继续执行
            response.raise_for_status()
        except Exception as e:
            # 如果请求失败，记录错误并返回
            logger.error(f"加载帖子 {post_id} 失败: {e}")
            return
        # 解析响应中的 JSON 数据
        response_data = response.json()
        # 清洗帖子内容（例如去除特殊字符）
        post_contents = clean_string(response_data.get("raw"))
        # 提取元数据
        metadata = {
            "url": post_url,
            "created_at": response_data.get("created_at", ""),
            "username": response_data.get("username", ""),
            "topic_slug": response_data.get("topic_slug", ""),
            "score": response_data.get("score", ""),
        }
        # 整理成统一的数据结构
        data = {
            "content": post_contents,
            "meta_data": metadata,
        }
        # 返回整理好的数据
        return data

    # 主要的数据加载函数
    def load_data(self, query):
        # 检查查询字符串是否有效
        self._check_query(query)
        # 准备收集的数据列表
        data = []
        data_contents = []
        # 记录日志，说明正在搜索的内容
        logger.info(f"在 Discourse 地址：{self.domain} 上搜索查询：{query}")
        # 构造搜索的 URL
        search_url = f"{self.domain}search.json?q={query}"
        # 发送 HTTP 请求进行搜索
        response = requests.get(search_url)
        try:
            # 如果请求成功则继续执行
            response.raise_for_status()
        except Exception as e:
            # 如果请求失败，则报错
            raise ValueError(f"搜索查询 {query} 失败: {e}")
        # 解析响应中的 JSON 数据
        response_data = response.json()
        # 获取帖子 ID 列表
        post_ids = response_data.get("grouped_search_result").get("post_ids")
        # 循环遍历每个帖子 ID
        for id in post_ids:
            # 加载单个帖子的内容
            post_data = self._load_post(id)
            # 如果帖子内容加载成功，则添加到收集的数据列表中
            if post_data:
                data.append(post_data)
                data_contents.append(post_data.get("content"))
            # 等待 0.4 秒，避免被服务器限制访问频率
            time.sleep(0.4)
        # 生成一个唯一的文档 ID
        doc_id = hashlib.sha256((query + ", ".join(data_contents)).encode()).hexdigest()
        # 整理最终返回的数据
        response_data = {"doc_id": doc_id, "data": data}
        # 返回整理好的数据
        return response_data

