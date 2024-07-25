# 这里导入了一些工具包，就像是我们做手工前准备的材料和工具。
import hashlib         # 用于生成独一无二的ID。
import logging         # 帮助我们记录程序运行时发生了什么。
import requests        # 让我们的程序可以访问互联网上的网页。

# 下面的代码是说如果需要一个特别的工具（BeautifulSoup）来解析网页，
# 而这个工具没有安装的话，它会告诉你怎么去安装它。
try:
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError(
        "我们需要一些额外的东西来读取网页。你可以用这句命令来安装：`pip install beautifulsoup4==4.12.3`"
    ) from None

# 这里是从其他地方引入一些帮助函数和类。
from embedchain.helpers.json_serializable import register_deserializable
from embedchain.loaders.base_loader import BaseLoader
from embedchain.utils.misc import clean_string

# 我们设置了一个日志记录器，就像是写日记，记录程序做了什么。
logger = logging.getLogger(__name__)

# 这个装饰器（@register_deserializable）告诉程序，这个类可以被保存和读取。
@register_deserializable
class WebPageLoader(BaseLoader):
    # 所有这个类的实例都会共享同一个网络请求工具，这样更高效。
    _session = requests.Session()

    # 这个方法是从网页上抓取数据。
    def load_data(self, url):
        # 设置一个假的用户代理，让网站以为我们是真正的浏览器。
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        }
        # 使用共享的网络请求工具获取网页内容。
        response = self._session.get(url, headers=headers, timeout=30)
        # 确保请求成功，如果没有，会抛出错误。
        response.raise_for_status()
        # 把网页的内容变成字节流。
        data = response.content
        # 清洗网页内容，去掉不需要的部分。
        content = self._get_clean_content(data, url)

        # 收集关于网页的一些信息。
        metadata = {"url": url}

        # 生成一个基于网页内容和网址的独一无二的ID。
        doc_id = hashlib.sha256((content + url).encode()).hexdigest()
        # 最后返回一个字典，里面包含了ID、清洗后的网页内容和元数据。
        return {
            "doc_id": doc_id,
            "data": [
                {
                    "content": content,
                    "meta_data": metadata,
                }
            ],
        }

    # 这个静态方法用来清洗HTML，去除不需要的标签和内容。
    @staticmethod
    def _get_clean_content(html, url) -> str:
        # 把HTML变成可以操作的格式。
        soup = BeautifulSoup(html, "html.parser")
        # 记录原始文本的长度。
        original_size = len(str(soup.get_text()))

        # 这里定义了一系列要删除的标签，它们通常不是我们想要的主要内容。
        tags_to_exclude = [
            "nav", "aside", "form", "header", "noscript", "svg", "canvas", "footer", "script", "style",
        ]
        # 遍历并删除这些不需要的标签。
        for tag in soup(tags_to_exclude):
            tag.decompose()

        # 还有一些特定ID的元素也要删除。
        ids_to_exclude = ["sidebar", "main-navigation", "menu-main-menu"]
        for id_ in ids_to_exclude:
            tags = soup.find_all(id=id_)
            for tag in tags:
                tag.decompose()

        # 同样，还有一些特定类名的元素要删除。
        classes_to_exclude = [
            "elementor-location-header", "navbar-header", "nav", "header-sidebar-wrapper", "blog-sidebar-wrapper", "related-posts",
        ]
        for class_name in classes_to_exclude:
            tags = soup.find_all(class_=class_name)
            for tag in tags:
                tag.decompose()

        # 再次获取文本，这次应该是更干净的了。
        content = soup.get_text()
        # 再次清洗文本，确保它是干净的。
        content = clean_string(content)

        # 计算清洗后的文本长度。
        cleaned_size = len(content)
        # 如果原始文本不是空的，就打印一些信息，告诉我们清洗的效果。
        if original_size != 0:
            logger.info(
                f"[{url}] 清洗后的页面大小：{cleaned_size}个字符，从原来的{original_size}个字符减少（减少了{original_size-cleaned_size}个字符，{round((1-(cleaned_size/original_size)) * 100, 2)}%）"
            )

        # 返回清洗后的文本。
        return content

    # 这个类方法在不再需要网络请求工具时关闭它。
    @classmethod
    def close_session(cls):
        cls._session.close()

