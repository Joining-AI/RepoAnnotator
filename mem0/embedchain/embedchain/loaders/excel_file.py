# 导入hashlib库，这个库可以用来生成散列（就是一种特殊的安全编码）
import hashlib

# 导入importlib.util模块，这个模块可以帮助我们检查和加载其他Python模块
import importlib.util

# 尝试导入unstructured库，如果成功，虽然我们不会直接使用它，但我们需要它在背后工作
try:
    import unstructured  # 这个注释告诉某些工具忽略这个导入，因为我们不直接使用它
    # 从langchain_community库中导入UnstructuredExcelLoader类，用于处理Excel文件
    from langchain_community.document_loaders import UnstructuredExcelLoader
except ImportError:
    # 如果导入失败，抛出错误信息，告诉用户需要安装额外的依赖项
    raise ImportError(
        'Excel文件需要额外的依赖项。请使用`pip install "unstructured[local-inference, all-docs]"`命令来安装'
    ) from None

# 检查是否安装了openpyxl或xlrd库，这两个库是处理Excel文件所需的
if importlib.util.find_spec("openpyxl") is None and importlib.util.find_spec("xlrd") is None:
    # 如果没有找到这些库中的任何一个，抛出错误并告知用户如何安装
    raise ImportError("Excel文件需要额外的依赖项。请使用`pip install openpyxl xlrd`命令来安装") from None

# 从embedchain的helpers模块中导入json_serializable注册器，用于序列化和反序列化对象
from embedchain.helpers.json_serializable import register_deserializable
# 导入BaseLoader基类，所有加载器都应该继承自它
from embedchain.loaders.base_loader import BaseLoader
# 导入clean_string函数，用于清理字符串内容
from embedchain.utils.misc import clean_string

# 使用装饰器将ExcelFileLoader类注册为可序列化的
@register_deserializable
# 定义ExcelFileLoader类，继承自BaseLoader
class ExcelFileLoader(BaseLoader):
    # 定义load_data方法，接收一个参数excel_url，用于加载Excel文件的数据
    def load_data(self, excel_url):
        """从Excel文件加载数据"""
        # 创建UnstructuredExcelLoader实例，传入Excel文件的URL
        loader = UnstructuredExcelLoader(excel_url)
        # 使用loader加载并分割Excel文件的内容
        pages = loader.load_and_split()

        # 初始化一个空列表，用于存储处理后的数据
        data = []
        # 遍历每一页的内容
        for page in pages:
            # 获取页面的文本内容
            content = page.page_content
            # 清理文本内容，去除不必要的字符
            content = clean_string(content)

            # 获取页面的元数据
            metadata = page.metadata
            # 添加Excel文件的URL到元数据中
            metadata["url"] = excel_url

            # 将内容和元数据组合成字典，然后添加到data列表中
            data.append({"content": content, "meta_data": metadata})

        # 生成一个基于内容和URL的唯一标识符
        doc_id = hashlib.sha256((content + excel_url).encode()).hexdigest()
        # 返回包含文档ID和数据的字典
        return {
            "doc_id": doc_id,
            "data": data,
        }

