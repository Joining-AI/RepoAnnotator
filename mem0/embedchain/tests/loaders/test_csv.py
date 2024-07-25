# 导入我们需要的所有库，这些库帮助我们处理CSV文件、临时文件和测试。
import csv
import os
import pathlib
import tempfile
from unittest.mock import MagicMock, patch

import pytest

# 这是从embedchain库中导入的一个用于加载CSV文件的类。
from embedchain.loaders.csv import CsvLoader

# 定义一个测试函数，它会尝试使用不同的分隔符（如逗号、制表符等）来加载CSV文件。
@pytest.mark.parametrize("delimiter", [",", "\t", ";", "|"])
def test_load_data(delimiter):
    """
    这个函数测试CSV加载器是否能正确读取文件，检查元数据和内容是否准确无误。
    """
    # 创建一个临时的CSV文件，这个文件会在测试结束后被删除。
    with tempfile.NamedTemporaryFile(mode="w+", newline="", delete=False) as tmpfile:
        # 使用CSV库的writer对象写入文件。
        writer = csv.writer(tmpfile, delimiter=delimiter)
        # 写入表头。
        writer.writerow(["Name", "Age", "Occupation"])
        # 写入三行数据。
        writer.writerow(["Alice", "28", "Engineer"])
        writer.writerow(["Bob", "35", "Doctor"])
        writer.writerow(["Charlie", "22", "Student"])

        # 将文件指针移回文件开头，以便我们可以读取它。
        tmpfile.seek(0)
        # 获取临时文件的名字。
        filename = tmpfile.name

        # 使用CsvLoader加载CSV文件。
        loader = CsvLoader()
        result = loader.load_data(filename)
        # 从结果中获取数据部分。
        data = result["data"]

        # 检查数据长度是否为3，因为除了表头外有3行数据。
        assert len(data) == 3
        # 检查每行数据的内容是否正确。
        assert data[0]["content"] == "Name: Alice, Age: 28, Occupation: Engineer"
        # 检查元数据是否包含正确的文件名和行号。
        assert data[0]["meta_data"]["url"] == filename
        assert data[0]["meta_data"]["row"] == 1
        # 对剩余两行数据做同样的检查。
        assert data[1]["content"] == "Name: Bob, Age: 35, Occupation: Doctor"
        assert data[1]["meta_data"]["url"] == filename
        assert data[1]["meta_data"]["row"] == 2
        assert data[2]["content"] == "Name: Charlie, Age: 22, Occupation: Student"
        assert data[2]["meta_data"]["url"] == filename
        assert data[2]["meta_data"]["row"] == 3

        # 删除创建的临时文件。
        os.unlink(filename)

# 下面的测试函数与上一个类似，但是这次使用文件URI来加载文件。
@pytest.mark.parametrize("delimiter", [",", "\t", ";", "|"])
def test_load_data_with_file_uri(delimiter):
    """
    这个测试确保我们能通过文件URI加载CSV文件，并且所有信息都正确。
    """
    # 创建并写入临时CSV文件，与前一个测试相同。
    with tempfile.NamedTemporaryFile(mode="w+", newline="", delete=False) as tmpfile:
        writer = csv.writer(tmpfile, delimiter=delimiter)
        writer.writerow(["Name", "Age", "Occupation"])
        writer.writerow(["Alice", "28", "Engineer"])
        writer.writerow(["Bob", "35", "Doctor"])
        writer.writerow(["Charlie", "22", "Student"])

        tmpfile.seek(0)
        # 这次我们将文件路径转换为文件URI。
        filename = pathlib.Path(tmpfile.name).as_uri()

        # 加载文件并检查数据。
        loader = CsvLoader()
        result = loader.load_data(filename)
        data = result["data"]

        # 进行相同的断言检查，确保数据和元数据正确。
        assert len(data) == 3
        assert data[0]["content"] == "Name: Alice, Age: 28, Occupation: Engineer"
        assert data[0]["meta_data"]["url"] == filename
        assert data[0]["meta_data"]["row"] == 1
        assert data[1]["content"] == "Name: Bob, Age: 35, Occupation: Doctor"
        assert data[1]["meta_data"]["url"] == filename
        assert data[1]["meta_data"]["row"] == 2
        assert data[2]["content"] == "Name: Charlie, Age: 22, Occupation: Student"
        assert data[2]["meta_data"]["url"] == filename
        assert data[2]["meta_data"]["row"] == 3

        # 清理临时文件。
        os.unlink(tmpfile.name)

# 接下来，我们测试CsvLoader是否能正确处理不支持的URL类型。
@pytest.mark.parametrize("content", ["ftp://example.com", "sftp://example.com", "mailto://example.com"])
def test_get_file_content(content):
    # 我们期望当尝试加载不支持的URL时，会抛出一个错误。
    with pytest.raises(ValueError):
        loader = CsvLoader()
        loader._get_file_content(content)

# 最后，我们测试CsvLoader对HTTP和HTTPS类型的URL的支持情况。
@pytest.mark.parametrize("content", ["http://example.com", "https://example.com"])

# 定义一个叫做test_get_file_content_http的函数，这个函数需要一个参数content。
def test_get_file_content_http(content):
    """
    # 这个函数是用来测试CsvLoader类中的一个方法（_get_file_content），
    # 看看它是否能正确处理http和https类型的网址。
    """

    # 下面这一大段是在做模拟（假装）网络请求的事情。
    # 我们用一个叫做patch的东西，假装我们正在使用requests库里的get方法。
    # 这样我们就可以控制返回的结果，而不需要真的去网上下载东西。
    with patch("requests.get") as mock_get:
        
        # 我们创建了一个假装的响应对象mock_response。
        # 这个对象会有一个text属性，里面装着一些假装从网上读到的CSV数据。
        mock_response = MagicMock()
        # 这是假装的数据，看起来像是一个CSV文件的内容。
        mock_response.text = "Name,Age,Occupation\nAlice,28,Engineer\nBob,35,Doctor\nCharlie,22,Student"
        
        # 我们让我们的假装get方法返回上面创建的假装响应mock_response。
        mock_get.return_value = mock_response

        # 现在我们创建一个CsvLoader的对象，这个对象有一个方法叫_get_file_content。
        loader = CsvLoader()
        # 我们调用这个方法，传入content参数，假装我们要从content这个网址读取数据。
        file_content = loader._get_file_content(content)

        # 然后我们检查，确保我们的假装get方法确实被调用了一次，而且是用content作为参数。
        mock_get.assert_called_once_with(content)
        # 接下来我们检查，假装的响应对象的raise_for_status方法也被调用了一次，
        # 这个方法通常是用来检查网络请求是否成功的。
        mock_response.raise_for_status.assert_called_once()
        
        # 最后，我们断言（也就是检查），通过file_content读取的内容是否和我们假装的响应内容完全一样。
        # 如果一样，说明我们的方法工作正常。
        assert file_content.read() == mock_response.text

