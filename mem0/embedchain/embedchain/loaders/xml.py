# 导入一个叫做hashlib的库，它可以帮助我们生成一种特殊的编码，就像给东西贴上独一无二的标签。
import hashlib

# 尝试导入一个叫unstructured的库和一个叫UnstructuredXMLLoader的东西。如果没成功，就跳过这个库，但不会影响下面的代码。
try:
    import unstructured  # 这行代码告诉Python我们想用unstructured库，但是我们并不需要它在这里做任何事情，所以加上了注释。
    # 从langchain_community库中导入UnstructuredXMLLoader，它能帮我们从XML文件里读取数据。
    from langchain_community.document_loaders import UnstructuredXMLLoader
# 如果导入失败，会抛出ImportError错误，这时我们就告诉用户需要安装额外的依赖。
except ImportError:
    # 提示用户需要安装额外的包才能处理XML文件，并告诉他们怎么安装。
    raise ImportError(
        'XML文件需要额外的依赖包。请用命令`pip install "unstructured[local-inference, all-docs]"`来安装'
    ) from None

# 从embedchain的helpers模块中导入json_serializable，它可以帮助我们处理一些JSON相关的功能。
from embedchain.helpers.json_serializable import register_deserializable
# 导入BaseLoader类，它是所有加载器的基础，我们的XmlLoader类将基于它进行扩展。
from embedchain.loaders.base_loader import BaseLoader
# 导入一个叫做clean_string的函数，它可以帮助我们清理字符串中的杂乱字符。
from embedchain.utils.misc import clean_string

# 使用装饰器（register_deserializable）标记XmlLoader类，这样它就可以被序列化和反序列化了。
@register_deserializable
# 定义一个名为XmlLoader的类，它继承自BaseLoader，专门用于处理XML文件。
class XmlLoader(BaseLoader):
    # 定义一个方法load_data，它接受一个参数xml_url，这个参数是XML文件的地址。
    def load_data(self, xml_url):
        """从一个XML文件中加载数据。"""
        # 创建一个UnstructuredXMLLoader实例，传入XML文件的地址。
        loader = UnstructuredXMLLoader(xml_url)
        # 使用loader加载数据。
        data = loader.load()
        # 获取加载后的数据内容。
        content = data[0].page_content
        # 清理数据内容，去掉不需要的字符。
        content = clean_string(content)
        # 获取数据的元信息。
        metadata = data[0].metadata
        # 把元信息里的"source"字段改名为"url"。
        metadata["url"] = metadata["source"]
        # 删除元信息里的"source"字段，因为我们已经把它改名了。
        del metadata["source"]
        # 把处理好的内容和元信息打包成字典，然后放到一个列表里。
        output = [{"content": content, "meta_data": metadata}]
        # 生成一个基于内容和XML文件地址的唯一标识符（哈希值）。
        doc_id = hashlib.sha256((content + xml_url).encode()).hexdigest()
        # 最后，返回一个字典，里面包含文档的唯一标识符和处理好的数据。
        return {
            "doc_id": doc_id,
            "data": output,
        }

