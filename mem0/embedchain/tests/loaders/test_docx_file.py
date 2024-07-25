# 导入 hashlib 模块，这是一个用于生成哈希值的模块。
import hashlib
# 导入 MagicMock 和 patch 这两个工具，它们可以帮助我们模拟（也就是假装）一些对象的行为。
from unittest.mock import MagicMock, patch
# 导入 pytest，这是一个用于编写测试用例的库。
import pytest
# 导入 DocxFileLoader 类，这是我们想要测试的对象。
from embedchain.loaders.docx_file import DocxFileLoader

# 定义一个测试用例的辅助函数，用来模拟 Docx2txtLoader 的行为。
@pytest.fixture
def mock_docx2txt_loader():
    # 使用上下文管理器来模拟 Docx2txtLoader 的行为。
    with patch("embedchain.loaders.docx_file.Docx2txtLoader") as mock_loader:
        # 让其他部分的代码可以使用这个模拟的对象。
        yield mock_loader

# 定义另一个测试用例的辅助函数，它创建了一个真实的 DocxFileLoader 实例。
@pytest.fixture
def docx_file_loader():
    # 创建并返回一个 DocxFileLoader 的实例。
    return DocxFileLoader()

# 定义一个测试函数，用来验证 DocxFileLoader 的 load_data 方法是否正确工作。
def test_load_data(mock_docx2txt_loader, docx_file_loader):
    # 假设的 .docx 文件的 URL 或路径。
    mock_url = "mock_docx_file.docx"

    # 创建一个模拟的 Docx2txtLoader 实例。
    mock_loader = MagicMock()
    # 设置模拟对象的 load 方法，让它返回一个包含文档内容和元数据的列表。
    mock_loader.load.return_value = [MagicMock(page_content="Sample Docx Content", metadata={"url": "local"})]

    # 让模拟的 Docx2txtLoader 返回上面定义的模拟对象。
    mock_docx2txt_loader.return_value = mock_loader

    # 调用 DocxFileLoader 的 load_data 方法，并传入一个假定的文件路径。
    result = docx_file_loader.load_data(mock_url)

    # 检查返回的结果中是否包含 "doc_id" 这个键。
    assert "doc_id" in result
    # 检查返回的结果中是否包含 "data" 这个键。
    assert "data" in result

    # 我们期望的内容是 "Sample Docx Content"。
    expected_content = "Sample Docx Content"
    # 确认结果中的内容是否与我们期望的一致。
    assert result["data"][0]["content"] == expected_content

    # 确认结果中的元数据中的 "url" 是否与我们期望的一致，这里是 "local"。
    assert result["data"][0]["meta_data"]["url"] == "local"

    # 生成一个哈希值，这个哈希值是由期望的内容和文件路径组合起来的。
    expected_doc_id = hashlib.sha256((expected_content + mock_url).encode()).hexdigest()
    # 确认结果中的 "doc_id" 是否与我们期望的哈希值一致。
    assert result["doc_id"] == expected_doc_id

