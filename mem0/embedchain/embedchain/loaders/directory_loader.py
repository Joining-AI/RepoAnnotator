# 导入所需的库和模块
import hashlib
import logging
from pathlib import Path
from typing import Any, Optional

# 导入自定义配置类
from embedchain.config import AddConfig
# 导入数据格式化处理类
from embedchain.data_formatter.data_formatter import DataFormatter
# 导入帮助处理JSON序列化的装饰器
from embedchain.helpers.json_serializable import register_deserializable
# 导入基础加载器类
from embedchain.loaders.base_loader import BaseLoader
# 导入文本文件加载器类
from embedchain.loaders.text_file import TextFileLoader
# 导入检测文件类型的方法
from embedchain.utils.misc import detect_datatype

# 创建日志记录器
logger = logging.getLogger(__name__)

# 使用装饰器注册可序列化的类
@register_deserializable
# 定义目录加载器类
class DirectoryLoader(BaseLoader):
    """从目录中加载数据。"""

    # 初始化方法
    def __init__(self, config: Optional[dict[str, Any]] = None):
        # 调用父类构造方法
        super().__init__()
        # 如果没有传入配置，则设置为空字典
        config = config or {}
        # 设置是否递归加载子目录，默认为True
        self.recursive = config.get("recursive", True)
        # 设置要加载的文件扩展名列表，默认为None（即加载所有文件）
        self.extensions = config.get("extensions", None)
        # 用于记录错误信息的列表
        self.errors = []

    # 加载指定路径下的数据
    def load_data(self, path: str):
        # 将路径转换为Path对象
        directory_path = Path(path)
        # 检查路径是否为有效目录
        if not directory_path.is_dir():
            # 如果不是目录，抛出异常
            raise ValueError(f"无效路径: {path}")

        # 记录日志，表示正在加载目录中的数据
        logger.info(f"正在从目录加载数据: {path}")
        # 处理目录并获取数据列表
        data_list = self._process_directory(directory_path)
        # 根据数据内容和目录路径生成文档ID
        doc_id = hashlib.sha256((str(data_list) + str(directory_path)).encode()).hexdigest()

        # 遍历错误列表，记录每个错误的日志警告
        for error in self.errors:
            logger.warning(error)

        # 返回包含文档ID和数据列表的字典
        return {"doc_id": doc_id, "data": data_list}

    # 处理目录中的文件和子目录
    def _process_directory(self, directory_path: Path):
        # 初始化空的数据列表
        data_list = []
        # 如果是递归模式，则遍历当前目录及其所有子目录；否则只遍历当前目录
        for file_path in directory_path.rglob("*") if self.recursive else directory_path.glob("*"):
            # 忽略以`.`开头的隐藏文件或目录
            if file_path.name.startswith("."):
                continue
            # 如果是文件并且符合扩展名条件（如果设置了扩展名的话），则进行加载
            if file_path.is_file() and (not self.extensions or any(file_path.suffix == ext for ext in self.extensions)):
                # 预测并创建适合该文件类型的加载器
                loader = self._predict_loader(file_path)
                # 使用加载器加载文件数据
                data_list.extend(loader.load_data(str(file_path))["data"])
            # 如果是目录，则继续处理
            elif file_path.is_dir():
                # 记录日志，表示正在加载子目录中的数据
                logger.info(f"正在从目录加载数据: {file_path}")
        # 返回收集到的所有数据
        return data_list

    # 根据文件路径预测合适的加载器
    def _predict_loader(self, file_path: Path) -> BaseLoader:
        try:
            # 检测文件的数据类型
            data_type = detect_datatype(str(file_path))
            # 创建加载配置
            config = AddConfig()
            # 根据数据类型获取相应的加载器
            return DataFormatter(data_type=data_type, config=config)._get_loader(
                data_type=data_type, config=config.loader, loader=None
            )
        # 如果发生异常，则记录错误信息并返回文本文件加载器
        except Exception as e:
            self.errors.append(f"处理{file_path}时出现错误: {e}")
            return TextFileLoader()

