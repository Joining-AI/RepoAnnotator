# 导入必要的库和模块
import hashlib  # 用于生成哈希值
from unittest.mock import MagicMock  # 用于创建模拟对象来进行测试
import pytest  # 一个用于编写单元测试的库

# 导入自定义的类和配置
from embedchain.chunkers.base_chunker import BaseChunker  # 这是我们要测试的主要类
from embedchain.config.add_config import ChunkerConfig  # 配置类，用于设置chunk的大小等参数
from embedchain.models.data_type import DataType  # 数据类型枚举类

# 使用pytest的fixture功能来创建一个模拟的文本分割器
@pytest.fixture
def text_splitter_mock():
    return MagicMock()  # 返回一个模拟的文本分割器对象

# 创建一个模拟的数据加载器
@pytest.fixture
def loader_mock():
    return MagicMock()  # 返回一个模拟的数据加载器对象

# 创建一个测试应用ID
@pytest.fixture
def app_id():
    return "test_app"  # 返回一个字符串作为应用ID

# 创建一个数据类型
@pytest.fixture
def data_type():
    return DataType.TEXT  # 返回一个数据类型，这里是文本类型

# 创建一个BaseChunker实例
@pytest.fixture
def chunker(text_splitter_mock, data_type):
    text_splitter = text_splitter_mock  # 使用之前创建的模拟文本分割器
    chunker = BaseChunker(text_splitter)  # 创建BaseChunker实例
    chunker.set_data_type(data_type)  # 设置数据类型
    return chunker  # 返回BaseChunker实例

# 测试create_chunks方法，传入配置
def test_create_chunks_with_config(chunker, text_splitter_mock, loader_mock, app_id, data_type):
    text_splitter_mock.split_text.return_value = ["Chunk 1", "long chunk"]  # 模拟返回两个文本块
    loader_mock.load_data.return_value = {  # 模拟返回加载的数据
        "data": [{"content": "Content 1", "meta_data": {"url": "URL 1"}}],  # 内容及其元数据
        "doc_id": "DocID",  # 文档ID
    }
    config = ChunkerConfig(chunk_size=50, chunk_overlap=0, length_function=len, min_chunk_size=10)  # 配置chunk的大小等
    result = chunker.create_chunks(loader_mock, "test_src", app_id, config)  # 调用create_chunks方法
    assert result["documents"] == ["long chunk"]  # 检查结果是否符合预期

# 测试create_chunks方法，没有传入配置
def test_create_chunks(chunker, text_splitter_mock, loader_mock, app_id, data_type):
    text_splitter_mock.split_text.return_value = ["Chunk 1", "Chunk 2"]  # 模拟返回两个文本块
    loader_mock.load_data.return_value = {  # 模拟返回加载的数据
        "data": [{"content": "Content 1", "meta_data": {"url": "URL 1"}}],  # 内容及其元数据
        "doc_id": "DocID",  # 文档ID
    }
    result = chunker.create_chunks(loader_mock, "test_src", app_id)  # 调用create_chunks方法
    expected_ids = [  # 计算预期的ID列表
        f"{app_id}--" + hashlib.sha256(("Chunk 1" + "URL 1").encode()).hexdigest(),  # 计算第一个文本块的ID
        f"{app_id}--" + hashlib.sha256(("Chunk 2" + "URL 1").encode()).hexdigest(),  # 计算第二个文本块的ID
    ]
    assert result["documents"] == ["Chunk 1", "Chunk 2"]  # 检查结果是否符合预期
    assert result["ids"] == expected_ids  # 检查ID是否正确
    assert result["metadatas"] == [  # 检查元数据是否正确
        {
            "url": "URL 1",  # URL
            "data_type": data_type.value,  # 数据类型
            "doc_id": f"{app_id}--DocID",  # 文档ID
        },
        {
            "url": "URL 1",  # URL
            "data_type": data_type.value,  # 数据类型
            "doc_id": f"{app_id}--DocID",  # 文档ID
        },
    ]
    assert result["doc_id"] == f"{app_id}--DocID"  # 检查文档ID是否正确

# 测试get_chunks方法
def test_get_chunks(chunker, text_splitter_mock):
    text_splitter_mock.split_text.return_value = ["Chunk 1", "Chunk 2"]  # 模拟返回两个文本块
    content = "This is a test content."  # 一些测试内容
    result = chunker.get_chunks(content)  # 调用get_chunks方法
    assert len(result) == 2  # 检查返回的chunk数量
    assert result == ["Chunk 1", "Chunk 2"]  # 检查返回的内容

# 测试set_data_type方法
def test_set_data_type(chunker):
    chunker.set_data_type(DataType.MDX)  # 设置数据类型为MDX
    assert chunker.data_type == DataType.MDX  # 检查数据类型是否正确设置

# 测试get_word_count方法
def test_get_word_count(chunker):
    documents = ["This is a test.", "Another test."]  # 一些文档
    result = chunker.get_word_count(documents)  # 调用get_word_count方法
    assert result == 6  # 检查总词数是否正确

