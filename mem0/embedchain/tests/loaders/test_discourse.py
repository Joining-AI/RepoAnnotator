# 导入需要的库
import pytest
import requests

# 导入 DiscourseLoader 类
from embedchain.loaders.discourse import DiscourseLoader

# 这个函数用来设置 DiscourseLoader 需要的一些基本信息
@pytest.fixture
def discourse_loader_config():
    # 返回一个字典，里面包含我们要访问的论坛网址
    return {
        "domain": "https://example.com/",
    }

# 这个函数用来创建一个 DiscourseLoader 实例
@pytest.fixture
def discourse_loader(discourse_loader_config):
    # 使用上面设置的信息创建 DiscourseLoader
    return DiscourseLoader(config=discourse_loader_config)

# 这个测试函数检查是否能正确初始化 DiscourseLoader
def test_discourse_loader_init_with_valid_config():
    # 设置正确的配置信息
    config = {"domain": "https://example.com/"}
    # 创建 DiscourseLoader 实例
    loader = DiscourseLoader(config=config)
    # 检查创建的实例中的网址是否和我们设置的一样
    assert loader.domain == "https://example.com/"

# 这个测试函数检查如果没有提供必要的配置会发生什么
def test_discourse_loader_init_with_missing_config():
    # 尝试创建 DiscourseLoader 但是不给它任何配置信息
    with pytest.raises(ValueError, match="DiscourseLoader requires a config"):
        DiscourseLoader()

# 这个测试函数检查如果提供的配置里缺少网址会发生什么
def test_discourse_loader_init_with_missing_domain():
    # 设置一个错误的配置，没有包含网址
    config = {"another_key": "value"}
    # 尝试创建 DiscourseLoader 并检查是否会因为缺少网址而报错
    with pytest.raises(ValueError, match="DiscourseLoader requires a domain"):
        DiscourseLoader(config=config)

# 这个测试函数检查是否能正确验证查询字符串
def test_discourse_loader_check_query_with_valid_query(discourse_loader):
    # 使用一个有效的查询字符串调用 _check_query 方法
    discourse_loader._check_query("sample query")

# 这个测试函数检查如果没有提供查询字符串会发生什么
def test_discourse_loader_check_query_with_empty_query(discourse_loader):
    # 尝试使用空字符串作为查询字符串并检查是否会报错
    with pytest.raises(ValueError, match="DiscourseLoader requires a query"):
        discourse_loader._check_query("")

# 这个测试函数检查如果查询字符串不是字符串类型会发生什么
def test_discourse_loader_check_query_with_invalid_query_type(discourse_loader):
    # 尝试使用数字而不是字符串作为查询字符串并检查是否会报错
    with pytest.raises(ValueError, match="DiscourseLoader requires a query"):
        discourse_loader._check_query(123)

# 这个测试函数检查是否能正确加载帖子内容
def test_discourse_loader_load_post_with_valid_post_id(discourse_loader, monkeypatch):
    # 定义一个模拟函数，假装从网络获取数据
    def mock_get(*args, **kwargs):
        # 定义一个模拟的响应类
        class MockResponse:
            # 模拟返回 JSON 数据的方法
            def json(self):
                return {"raw": "Sample post content"}

            # 模拟检查响应状态的方法
            def raise_for_status(self):
                pass

        # 返回模拟的响应
        return MockResponse()

    # 使用 monkeypatch 来替换真实的网络请求函数
    monkeypatch.setattr(requests, "get", mock_get)

    # 调用 _load_post 方法并传入一个帖子 ID
    post_data = discourse_loader._load_post(123)

    # 检查返回的数据是否包含了正确的帖子内容
    assert post_data["content"] == "Sample post content"
    # 检查返回的数据是否包含元数据
    assert "meta_data" in post_data

# 这个测试函数检查是否能正确加载数据
def test_discourse_loader_load_data_with_valid_query(discourse_loader, monkeypatch):
    # 定义一个模拟函数，假装从网络获取帖子 ID 列表
    def mock_get(*args, **kwargs):
        # 定义一个模拟的响应类
        class MockResponse:
            # 模拟返回 JSON 数据的方法
            def json(self):
                return {"grouped_search_result": {"post_ids": [123, 456, 789]}}

            # 模拟检查响应状态的方法
            def raise_for_status(self):
                pass

        # 返回模拟的响应
        return MockResponse()

    # 使用 monkeypatch 来替换真实的网络请求函数
    monkeypatch.setattr(requests, "get", mock_get)

    # 定义一个模拟函数，假装加载单个帖子的内容
    def mock_load_post(*args, **kwargs):
        # 返回模拟的帖子数据
        return {
            "content": "Sample post content",
            "meta_data": {
                "url": "https://example.com/posts/123.json",
                "created_at": "2021-01-01",
                "username": "test_user",
                "topic_slug": "test_topic",
                "score": 10,
            },
        }

    # 使用 monkeypatch 来替换真正的 _load_post 函数
    monkeypatch.setattr(discourse_loader, "_load_post", mock_load_post)

    # 调用 load_data 方法并传入一个查询字符串
    data = discourse_loader.load_data("sample query")

    # 检查返回的数据是否包含了正确的帖子数量
    assert len(data["data"]) == 3
    # 检查第一个帖子的内容是否正确
    assert data["data"][0]["content"] == "Sample post content"
    # 检查第一个帖子的网址是否正确
    assert data["data"][0]["meta_data"]["url"] == "https://example.com/posts/123.json"
    # 检查第一个帖子的创建时间是否正确
    assert data["data"][0]["meta_data"]["created_at"] == "2021-01-01"
    # 检查第一个帖子的用户名是否正确
    assert data["data"][0]["meta_data"]["username"] == "test_user"
    # 检查第一个帖子的主题是否正确
    assert data["data"][0]["meta_data"]["topic_slug"] == "test_topic"
    # 检查第一个帖子的得分是否正确
    assert data["data"][0]["meta_data"]["score"] == 10

