# 导入base64模块，它用来处理Base64编码。
import base64
# 导入hashlib模块，这个模块可以用来生成哈希值（一种加密方法）。
import hashlib
# 导入logging模块，用于记录程序运行时的信息。
import logging
# 导入os模块，它提供了许多与操作系统交互的功能。
import os
# 从email模块中导入message_from_bytes函数，这个函数可以把字节数据转换成邮件对象。
from email import message_from_bytes
# 从email.utils模块中导入parsedate_to_datetime函数，这个函数可以把邮件中的日期格式转换成Python的日期时间格式。
from email.utils import parsedate_to_datetime
# 从textwrap模块中导入dedent函数，这个函数可以去掉字符串前的缩进。
from textwrap import dedent
# 从typing模块中导入Optional类型提示，表示某个变量可能是什么类型或可能是None。
from typing import Optional

# 从bs4模块中导入BeautifulSoup类，这是一个解析HTML和XML文档的库，这里用来解析邮件中的HTML内容。
from bs4 import BeautifulSoup

# 尝试导入一些和Google API相关的库，这些库用于和Gmail服务通信。
try:
    # 从google.auth.transport.requests模块导入Request类，用于发送HTTP请求。
    from google.auth.transport.requests import Request
    # 从google.oauth2.credentials模块导入Credentials类，这是用来保存认证信息的。
    from google.oauth2.credentials import Credentials
    # 从google_auth_oauthlib.flow模块导入InstalledAppFlow类，用于处理OAuth2授权流程。
    from google_auth_oauthlib.flow import InstalledAppFlow
    # 从googleapiclient.discovery模块导入build函数，用于构建API服务对象。
    from googleapiclient.discovery import build
# 如果上述尝试导入失败，则抛出ImportError异常，并提示用户需要安装额外的依赖包。
except ImportError:
    raise ImportError(
        # 提示信息，告诉用户如何安装所需的额外依赖包。
        'Gmail requires extra dependencies. Install with `pip install --upgrade "embedchain[gmail]"`'
    ) from None

# 从embedchain.loaders.base_loader模块导入BaseLoader类，这是自定义加载器的基础类。
from embedchain.loaders.base_loader import BaseLoader
# 从embedchain.utils.misc模块导入clean_string函数，这个函数用来清理文本字符串。
from embedchain.utils.misc import clean_string

# 初始化日志记录器，命名为__name__（通常是模块名），这样就可以记录这个文件里的日志了。
logger = logging.getLogger(__name__)

class GmailReader:

# 定义了一个名为GmailLoader的类，它继承自BaseLoader。
class GmailLoader(BaseLoader):
    # 这个方法用于加载数据，需要传入一个查询字符串作为参数。
    def load_data(self, query: str):
        # 创建一个GmailReader对象，将查询字符串传递给它。
        reader = GmailReader(query=query)
        # 使用GmailReader对象加载邮件。
        emails = reader.load_emails()
        # 打印日志信息，告诉我们找到了多少封邮件，以及查询的内容是什么。
        logger.info(f"Gmail Loader: {len(emails)} emails found for query '{query}'")

        # 初始化一个空列表，用来存放处理后的邮件数据。
        data = []
        # 遍历所有找到的邮件。
        for email in emails:
            # 调用一个私有方法来处理每一封邮件。
            content = self._process_email(email)
            # 将处理后的邮件内容和原始邮件信息打包成字典，然后添加到data列表中。
            data.append({"content": content, "meta_data": email})

        # 返回一个字典，其中包含生成的文档ID和处理后的数据列表。
        return {"doc_id": self._generate_doc_id(query, data), "data": data}

    # 这是一个静态方法，用于处理邮件的文本内容。
    @staticmethod
    def _process_email(email: dict) -> str:
        # 使用BeautifulSoup解析邮件正文中的HTML，提取纯文本内容。
        content = BeautifulSoup(email["body"], "html.parser").get_text()
        # 清洗字符串，去除不必要的字符或格式。
        content = clean_string(content)
        # 格式化邮件信息，包括发件人、收件人、主题、日期和内容。
        return dedent(
            f"""
            Email from '{email['from']}' to '{email['to']}'
            Subject: {email['subject']}
            Date: {email['date']}
            Content: {content}
        """
        )

    # 这是另一个静态方法，用于生成文档ID。
    @staticmethod
    def _generate_doc_id(query: str, data: list[dict]) -> str:
        # 提取数据列表中每封邮件的内容部分，组成一个新的列表。
        content_strings = [email["content"] for email in data]
        # 使用hashlib库的sha256算法，对查询字符串和所有邮件内容进行哈希运算，生成文档ID。
        return hashlib.sha256((query + ", ".join(content_strings)).encode()).hexdigest()

