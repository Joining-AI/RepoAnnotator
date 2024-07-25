# 引入了一个叫做hashlib的工具包，它能帮我们做加密处理。
import hashlib

# 尝试从一个叫langchain_community的工具包里找到Docx2txtLoader这个类，
# 这个类能帮助我们读取.docx文件的内容。
try:
    from langchain_community.document_loaders import Docx2txtLoader
# 如果上面那步没有成功（也就是说找不到这个类），
# 我们就告诉用户需要安装额外的工具包，具体是通过pip命令来安装。
except ImportError:
    raise ImportError("Docx file requires extra dependencies. Install with `pip install docx2txt==0.8`") from None

# 从embedchain的helpers模块里引入json_serializable这个工具，
# 它可以帮助我们把数据变成JSON格式，方便存储和传输。
from embedchain.helpers.json_serializable import register_deserializable
# 从embedchain的loaders模块里引入BaseLoader这个类，
# 这个类是我们后面要创建的类的“爸爸”，会有一些基本的功能。
from embedchain.loaders.base_loader import BaseLoader


# 使用装饰器（就是这个小帽子＠）告诉系统我们要注册一个新的可以序列化的类，
# 这样我们的类就可以被转换成JSON格式了。
@register_deserializable
# 创建一个叫DocxFileLoader的新类，继承自BaseLoader，也就是说它是BaseLoader的孩子。
class DocxFileLoader(BaseLoader):
    # 定义一个方法load_data，这个方法接受一个参数url，也就是文件的路径。
    def load_data(self, url):
        """Load data from a .docx file."""
        # 创建一个Docx2txtLoader对象，传入文件路径，准备加载文件内容。
        loader = Docx2txtLoader(url)
        # 初始化一个空列表output，用来存放处理后的数据。
        output = []
        # 使用loader加载数据，得到的结果存到data变量里。
        data = loader.load()
        # 从data中取出第0个元素的page_content，这是文件的主要内容。
        content = data[0].page_content
        # 同样地，取出第0个元素的metadata，这是关于文件的一些信息。
        metadata = data[0].metadata
        # 把"local"这个字符串加到metadata里面，表示数据来源是本地的。
        metadata["url"] = "local"
        # 把content和metadata打包成一个字典，然后添加到output列表里。
        output.append({"content": content, "meta_data": metadata})
        # 使用hashlib里的sha256函数对content和url的组合进行加密，
        # 然后把结果转成16进制的字符串，这就是文件的唯一标识符（doc_id）。
        doc_id = hashlib.sha256((content + url).encode()).hexdigest()
        # 最后，返回一个字典，包含doc_id和output两部分，
        # 这样我们就完成了对.docx文件的读取和处理。
        return {
            "doc_id": doc_id,
            "data": output,
        }

