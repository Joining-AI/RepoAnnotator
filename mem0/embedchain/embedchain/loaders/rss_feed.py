# 导入一个叫做hashlib的库，这个库是用来生成一种特殊的编码（哈希值）。
import hashlib

# 下面这两行代码是从其他文件中导入一些有用的工具。
from embedchain.helpers.json_serializable import register_deserializable
from embedchain.loaders.base_loader import BaseLoader

# 这个装饰器（register_deserializable）告诉程序这个类可以被特殊的方式处理，方便保存和读取。
@register_deserializable
# 定义了一个名为RSSFeedLoader的新类，它继承自BaseLoader。这个类是专门用来从RSS源加载数据的。
class RSSFeedLoader(BaseLoader):
    # 这是一个字符串，用来描述这个类是干什么的。
    """Loader for RSS Feed."""

    # 定义一个方法load_data，输入是一个URL，输出是从RSS源获取的数据。
    def load_data(self, url):
        """Load data from a rss feed."""
        # 调用get_rss_content方法，传入url参数，得到内容。
        output = self.get_rss_content(url)
        # 使用hashlib库中的sha256算法，把output和url转换成字符串，然后编码，最后生成一个唯一的哈希值作为文档ID。
        doc_id = hashlib.sha256((str(output) + url).encode()).hexdigest()
        # 返回一个字典，包含生成的文档ID和获取到的内容。
        return {
            "doc_id": doc_id,
            "data": output,
        }

    # 定义一个静态方法serialize_metadata，用于将元数据中的非字符串类型转换为字符串。
    @staticmethod
    def serialize_metadata(metadata):
        # 遍历传入的元数据字典。
        for key, value in metadata.items():
            # 如果值不是字符串、整数、浮点数或布尔值，就把它转换成字符串。
            if not isinstance(value, (str, int, float, bool)):
                metadata[key] = str(value)

        # 返回处理后的元数据。
        return metadata

    # 定义一个静态方法get_rss_content，输入是一个URL，返回从该URL获取的RSS内容。
    @staticmethod
    def get_rss_content(url: str):
        # 尝试从langchain_community.document_loaders导入RSSFeedLoader类。
        try:
            from langchain_community.document_loaders import RSSFeedLoader as LangchainRSSFeedLoader
        # 如果导入失败，则抛出ImportError并给出安装必要依赖的提示。
        except ImportError:
            raise ImportError(
                """RSSFeedLoader file requires extra dependencies.
                Install with `pip install feedparser==6.0.10 newspaper3k==0.2.8 listparser==0.19`"""
            ) from None

        # 初始化一个空列表，用于存放结果。
        output = []
        # 创建LangchainRSSFeedLoader实例，传入需要加载的RSS源URL。
        loader = LangchainRSSFeedLoader(urls=[url])
        # 加载数据。
        data = loader.load()

        # 遍历加载到的数据。
        for entry in data:
            # 把entry的元数据进行字符串化处理。
            metadata = RSSFeedLoader.serialize_metadata(entry.metadata)
            # 在元数据中添加URL信息。
            metadata.update({"url": url})
            # 把内容和元数据组合起来，添加到结果列表中。
            output.append(
                {
                    "content": entry.page_content,
                    "meta_data": metadata,
                }
            )

        # 返回最终的结果列表。
        return output

