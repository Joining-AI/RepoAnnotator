# 导入一些库，这些库帮助我们处理代码中的不同部分。
import hashlib
from unittest.mock import Mock, patch
import pytest

# 导入我们需要测试的 `WebPageLoader` 类。
from embedchain.loaders.web_page import WebPageLoader

# 使用 `@pytest.fixture` 装饰器定义了一个函数 `web_page_loader`，它返回一个 `WebPageLoader` 的实例。
@pytest.fixture
def web_page_loader():
    return WebPageLoader()

# 定义了一个测试函数 `test_load_data`，用来测试 `WebPageLoader` 类的 `load_data` 方法是否能正确工作。
def test_load_data(web_page_loader):
    # 设置一个示例网页的 URL。
    page_url = "https://example.com/page"
    
    # 创建一个模拟的 HTTP 响应对象 `mock_response`，并设置它的状态码和内容。
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = """
        <html>
            <head>
                <title>Test Page</title>
            </head>
            <body>
                <div id="content">
                    <p>This is some test content.</p>
                </div>
            </body>
        </html>
    """
    
    # 使用 `patch` 来模拟 `WebPageLoader` 类中的 `_session.get` 方法，让它返回我们创建的 `mock_response`。
    with patch("embedchain.loaders.web_page.WebPageLoader._session.get", return_value=mock_response):
        # 调用 `load_data` 方法，并将结果保存在变量 `result` 中。
        result = web_page_loader.load_data(page_url)

    # 从模拟响应的内容中获取清理过后的文本，并计算一个文档 ID。
    content = web_page_loader._get_clean_content(mock_response.content, page_url)
    expected_doc_id = hashlib.sha256((content + page_url).encode()).hexdigest()
    
    # 检查实际得到的文档 ID 是否与预期相符。
    assert result["doc_id"] == expected_doc_id

    # 设置一个期望的数据格式，包含清理过的文本内容和其他元数据。
    expected_data = [
        {
            "content": content,
            "meta_data": {
                "url": page_url,
            },
        }
    ]
    
    # 确认实际得到的数据是否与期望的数据一致。
    assert result["data"] == expected_data

