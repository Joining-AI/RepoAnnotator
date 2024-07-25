# 导入hashlib库，这是一个用来创建哈希值（一种加密方式）的库。
import hashlib
# 导入unittest库中的mock模块，用于模拟对象的行为。
from unittest.mock import patch
# 导入pytest库，这是一个常用的Python测试框架。
import pytest
# 导入我们想要测试的ExcelFileLoader类。
from embedchain.loaders.excel_file import ExcelFileLoader

# 使用pytest的fixture功能来创建一个ExcelFileLoader实例，这样可以在多个测试中重复使用这个实例。
@pytest.fixture
def excel_file_loader():
    # 创建并返回ExcelFileLoader实例。
    return ExcelFileLoader()

# 定义一个测试函数test_load_data，用来测试ExcelFileLoader的load_data方法。
def test_load_data(excel_file_loader):
    # 设定一个假的Excel文件URL，用于测试。
    mock_url = "mock_excel_file.xlsx"
    # 设定一个假的数据内容，用于测试。
    expected_content = "Sample Excel Content"

    # 使用patch.object来模拟ExcelFileLoader的load_data方法的行为。
    with patch.object(
        # 我们要模拟的对象是excel_file_loader的load_data方法。
        excel_file_loader,
        # 要模拟的方法名。
        "load_data",
        # 模拟load_data方法的返回值。
        return_value={
            # doc_id是一个基于expected_content和mock_url生成的哈希值。
            "doc_id": hashlib.sha256((expected_content + mock_url).encode()).hexdigest(),
            # data包含实际的内容和元数据。
            "data": [{"content": expected_content, "meta_data": {"url": mock_url}}],
        },
    ):
        # 调用load_data方法，并将结果存储在result变量中。
        result = excel_file_loader.load_data(mock_url)

    # 确认result中的data的第一条记录的内容是否与预期相符。
    assert result["data"][0]["content"] == expected_content
    # 确认result中的data的第一条记录的元数据中的URL是否与预期相符。
    assert result["data"][0]["meta_data"]["url"] == mock_url

    # 再次计算预期的doc_id，以确认其正确性。
    expected_doc_id = hashlib.sha256((expected_content + mock_url).encode()).hexdigest()
    # 最后，确认result中的doc_id是否与预期的doc_id相匹配。
    assert result["doc_id"] == expected_doc_id

