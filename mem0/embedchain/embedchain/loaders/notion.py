import hashlib
import logging
import os
from typing import Any, Optional

import requests

# 导入自定义模块，这些模块帮助处理JSON序列化和一些基本加载功能。
from embedchain.helpers.json_serializable import register_deserializable
from embedchain.loaders.base_loader import BaseLoader
from embedchain.utils.misc import clean_string

# 设置日志记录器，用来记录程序运行时的信息。
logger = logging.getLogger(__name__)

# 定义一个名为NotionLoader的类，它继承自BaseLoader这个爸爸类。
class NotionLoader(BaseLoader):

    # 这个函数用来从Notion的网址加载数据。
    def load_data(self, source):
        
        # 取出source字符串的最后32个字符，这些是Notion页面的ID。
        id = source[-32:]
        
        # 把取出的ID按照一定的格式整理一下，让它看起来更像一个标准的ID格式。
        formatted_id = f"{id[:8]}-{id[8:12]}-{id[12:16]}-{id[16:20]}-{id[20:]}"
        
        # 告诉电脑的日志系统，我们已经成功地提取了Notion页面的ID，并以格式化后的ID显示出来。
        logger.debug(f"Extracted notion page id as: {formatted_id}")

        # 从环境变量中获取Notion的集成令牌，这是访问Notion页面所需的密钥。
        integration_token = os.getenv("NOTION_INTEGRATION_TOKEN")
        
        # 创建一个NotionPageLoader对象，需要传入上面得到的令牌。
        reader = NotionPageLoader(integration_token=integration_token)
        
        # 使用这个对象去加载数据，传入的是我们之前格式化过的页面ID列表。
        documents = reader.load_data(page_ids=[formatted_id])

        # 从加载回来的数据中取出文本内容。
        raw_text = documents[0].text

        # 清理文本，去除可能存在的杂质或不需要的部分。
        text = clean_string(raw_text)
        
        # 使用一种叫做SHA256的加密方式，对清理后的文本和原始网址进行加密，生成一个唯一的标识符。
        doc_id = hashlib.sha256((text + source).encode()).hexdigest()
        
        # 最后返回一个字典，里面包含了我们生成的唯一标识符和数据。
        # 数据包括文本内容和元数据，元数据里有一个网址，网址是以"Notion-"开头加上我们之前格式化的ID。
        return {
            "doc_id": doc_id,
            "data": [
                {
                    "content": text,
                    "meta_data": {"url": f"notion-{formatted_id}"},
                }
            ],
        }

