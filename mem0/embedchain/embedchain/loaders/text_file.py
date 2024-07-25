# 导入hashlib库，这个库可以用来生成哈希值（一种特殊的指纹）
import hashlib
# 导入os库，这个库可以让我们和操作系统进行交互，比如读取文件
import os

# 导入一个装饰器函数，用于注册可序列化的类
from embedchain.helpers.json_serializable import register_deserializable
# 导入基类加载器，这里定义了一个基础的加载器框架
from embedchain.loaders.base_loader import BaseLoader

# 使用装饰器来注册这个类，使其支持序列化功能
@register_deserializable
# 定义一个名为TextFileLoader的类，继承自BaseLoader
class TextFileLoader(BaseLoader):
    # 定义一个方法load_data，它接受一个参数url（实际上是文件路径）
    def load_data(self, url: str):
        # 如果文件不存在，则抛出一个错误告诉用户文件不存在
        if not os.path.exists(url):
            raise FileNotFoundError(f"文件在 {url} 这个位置找不到。")

        # 用with语句打开文件，这样文件使用完毕后会自动关闭
        with open(url, "r", encoding="utf-8") as file:
            # 读取文件内容
            content = file.read()

        # 使用文件的内容和路径生成一个唯一的哈希值作为文档ID
        doc_id = hashlib.sha256((content + url).encode()).hexdigest()

        # 获取一些元数据：文件的大小、文件类型
        metadata = {
            "url": url,  # 文件路径
            "file_size": os.path.getsize(url),  # 文件大小
            "file_type": url.split(".")[-1]  # 文件扩展名
        }

        # 返回一个字典，包含文档ID和数据
        return {
            "doc_id": doc_id,  # 文档ID
            "data": [  # 数据列表
                {
                    "content": content,  # 文件内容
                    "meta_data": metadata,  # 元数据
                }
            ],
        }

