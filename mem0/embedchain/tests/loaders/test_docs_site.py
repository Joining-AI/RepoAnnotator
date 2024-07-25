# 导入hashlib库，用于生成哈希值
import hashlib
# 导入Mock和patch，用于在测试中模拟对象的行为
from unittest.mock import Mock, patch
# 导入pytest库，用于编写单元测试
import pytest
# 导入Response类，用于创建响应对象
from requests import Response
# 导入DocsSiteLoader类，这是要测试的主要类
from embedchain.loaders.docs_site_loader import DocsSiteLoader

# 定义一个测试夹具，用于模拟requests.get函数
@pytest.fixture
def mock_requests_get():
    # 使用patch装饰器模拟requests.get函数
    with patch("requests.get") as mock_get:
        # 返回模拟的get函数，供测试使用
        yield mock_get

# 定义一个测试夹具，用于创建DocsSiteLoader实例
@pytest.fixture
def docs_site_loader():
    # 返回一个DocsSiteLoader的新实例
    return DocsSiteLoader()

# 测试递归获取子链接功能
def test_get_child_links_recursive(mock_requests_get, docs_site_loader):
    # 创建一个模拟的响应对象
    mock_response = Mock()
    # 设置响应状态码为200（成功）
    mock_response.status_code = 200
    # 设置响应文本，包含一些HTML链接
    mock_response.text = """
        <html>
            <a href="/page1">Page 1</a>
            <a href="/page2">Page 2</a>
        </html>
    """
    # 设置模拟的requests.get函数返回上述响应
    mock_requests_get.return_value = mock_response

    # 调用递归获取子链接的方法
    docs_site_loader._get_child_links_recursive("https://example.com")

    # 检查访问过的链接数量是否为2
    assert len(docs_site_loader.visited_links) == 2
    # 检查是否包含了预期的链接
    assert "https://example.com/page1" in docs_site_loader.visited_links
    assert "https://example.com/page2" in docs_site_loader.visited_links

# 测试当状态码不是200时，递归获取子链接的行为
def test_get_child_links_recursive_status_not_200(mock_requests_get, docs_site_loader):
    # 创建一个状态码为404的模拟响应
    mock_response = Mock()
    mock_response.status_code = 404
    # 设置模拟的requests.get函数返回上述响应
    mock_requests_get.return_value = mock_response

    # 调用递归获取子链接的方法
    docs_site_loader._get_child_links_recursive("https://example.com")

    # 检查访问过的链接数量是否为0
    assert len(docs_site_loader.visited_links) == 0

# 测试获取所有URL功能
def test_get_all_urls(mock_requests_get, docs_site_loader):
    # 创建一个模拟的响应对象
    mock_response = Mock()
    # 设置响应状态码为200（成功）
    mock_response.status_code = 200
    # 设置响应文本，包含一些HTML链接
    mock_response.text = """
        <html>
            <a href="/page1">Page 1</a>
            <a href="/page2">Page 2</a>
            <a href="https://example.com/external">External</a>
        </html>
    """
    # 设置模拟的requests.get函数返回上述响应
    mock_requests_get.return_value = mock_response

    # 调用获取所有URL的方法
    all_urls = docs_site_loader._get_all_urls("https://example.com")

    # 检查返回的URL数量是否为3
    assert len(all_urls) == 3
    # 检查是否包含了预期的URL
    assert "https://example.com/page1" in all_urls
    assert "https://example.com/page2" in all_urls
    assert "https://example.com/external" in all_urls

# 测试从URL加载数据功能
def test_load_data_from_url(mock_requests_get, docs_site_loader):
    # 创建一个模拟的响应对象
    mock_response = Mock()
    # 设置响应状态码为200（成功）
    mock_response.status_code = 200
    # 设置响应内容，包含一些HTML结构
    mock_response.content = """
        <html>
            <nav>
                <h1>Navigation</h1>
            </nav>
            <article class="bd-article">
                <p>Article Content</p>
            </article>
        </html>
    """.encode()
    # 设置模拟的requests.get函数返回上述响应
    mock_requests_get.return_value = mock_response

    # 调用从URL加载数据的方法
    data = docs_site_loader._load_data_from_url("https://example.com/page1")

    # 检查返回的数据长度是否为1
    assert len(data) == 1
    # 检查数据内容是否正确
    assert data[0]["content"] == "Article Content"
    # 检查元数据中的URL是否正确
    assert data[0]["meta_data"]["url"] == "https://example.com/page1"

# 测试当状态码不是200时，从URL加载数据的行为
def test_load_data_from_url_status_not_200(mock_requests_get, docs_site_loader):
    # 创建一个状态码为404的模拟响应
    mock_response = Mock()
    mock_response.status_code = 404
    # 设置模拟的requests.get函数返回上述响应
    mock_requests_get.return_value = mock_response

    # 调用从URL加载数据的方法
    data = docs_site_loader._load_data_from_url("https://example.com/page1")

    # 检查返回的数据是否为空列表
    assert data == []
    assert len(data) == 0

# 测试加载数据功能
def test_load_data(mock_requests_get, docs_site_loader):
    # 创建一个响应对象
    mock_response = Response()
    # 设置响应状态码为200（成功）
    mock_response.status_code = 200
    # 设置响应内容，包含一些HTML链接
    mock_response._content = """
        <html>
            <a href="/page1">Page 1</a>
            <a href="/page2">Page 2</a>
        """.encode()
    # 设置模拟的requests.get函数返回上述响应
    mock_requests_get.return_value = mock_response

    # 定义要加载数据的URL
    url = "https://example.com"
    # 调用加载数据的方法
    data = docs_site_loader.load_data(url)
    # 计算预期的文档ID
    expected_doc_id = hashlib.sha256((" ".join(docs_site_loader.visited_links) + url).encode()).hexdigest()

    # 检查返回的数据中的数据长度是否为2
    assert len(data["data"]) == 2
    # 检查返回的文档ID是否与预期相符
    assert data["doc_id"] == expected_doc_id

# 定义一个函数，名字叫做 test_if_response_status_not_200
def test_if_response_status_not_200(mock_requests_get, docs_site_loader):
    # 创建一个假的响应对象，就像网站返回的信息一样
    mock_response = Response()
    # 设置这个假响应的状态码为 404，表示网页找不到
    mock_response.status_code = 404
    # 告诉 mock_requests_get 这个工具，当它去请求网址时，就返回我们刚才创建的假响应
    mock_requests_get.return_value = mock_response

    # 设定一个测试用的网址
    url = "https://example.com"
    # 使用 docs_site_loader 这个工具去加载上面设定的网址的数据
    data = docs_site_loader.load_data(url)
    # 计算一个特殊的 ID（叫做 doc_id），这个 ID 是根据访问过的链接和当前的网址通过一种叫 sha256 的加密方式生成的
    expected_doc_id = hashlib.sha256((" ".join(docs_site_loader.visited_links) + url).encode()).hexdigest()

    # 检查从网址加载回来的数据中 "data" 字段的长度是否是 0，如果是，说明没有数据被加载回来
    assert len(data["data"]) == 0
    # 再检查数据中的 "doc_id" 是否和我们之前计算出来的特殊 ID 相同，如果相同，说明 ID 的生成逻辑是对的
    assert data["doc_id"] == expected_doc_id

