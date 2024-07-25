# 导入一个叫做hashlib的库，它能帮我们做加密。
import hashlib

# 导入pytest库，这是一个帮助我们测试代码是否正确的工具。
import pytest

# 从embedchain这个大工具箱里拿出一个叫LocalTextLoader的小工具。
from embedchain.loaders.local_text import LocalTextLoader


# 这个函数是pytest的一个特别设置，它会先准备好我们需要的LocalTextLoader工具。
@pytest.fixture
def text_loader():
    # 返回一个LocalTextLoader的实例，这样在测试的时候就可以直接用了。
    return LocalTextLoader()


# 这个函数是用来测试LocalTextLoader工具的。
def test_load_data(text_loader):
    # 假装这是我们要加载的一段文本。
    mock_content = "This is a sample text content."

    # 使用text_loader工具去加载这段文本，看看它能不能正确工作。
    result = text_loader.load_data(mock_content)

    # 确认返回的结果里有"doc_id"这个部分。
    assert "doc_id" in result
    # 确认返回的结果里有"data"这个部分。
    assert "data" in result

    # 我们假设这段文本来自一个叫"local"的地方。
    url = "local"
    # 检查加载后的数据里，内容是不是和我们输入的一样。
    assert result["data"][0]["content"] == mock_content

    # 检查加载后的数据里的元数据（就是一些额外的信息），确认它的URL是我们假设的那个"local"。
    assert result["data"][0]["meta_data"]["url"] == url

    # 使用hashlib库里的sha256算法，把文本内容和URL组合起来加密，得到一个独特的ID。
    expected_doc_id = hashlib.sha256((mock_content + url).encode()).hexdigest()
    # 检查加载后的数据里的"doc_id"是不是和我们预期的一样。
    assert result["doc_id"] == expected_doc_id

