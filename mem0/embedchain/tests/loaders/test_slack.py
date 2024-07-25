# 引入pytest库，这是一个用于编写测试代码的工具。
import pytest

# 导入SlackLoader类，这个类是用来从Slack（一个工作沟通平台）加载数据的。
from embedchain.loaders.slack import SlackLoader

# 使用pytest的fixture特性来设置一个SlackLoader实例。fixture可以理解为准备测试时需要的一些预设条件。
@pytest.fixture
def slack_loader(mocker, monkeypatch):
    # mocker和monkeypatch是pytest的插件，用来模拟或修改一些函数的行为。
    # 下面三行代码是在“假装”使用Slack的WebClient、SSL安全连接和证书验证，这样测试时不需要真的连接到网络。
    mocker.patch("slack_sdk.WebClient")
    mocker.patch("ssl.create_default_context")
    mocker.patch("certifi.where")

    # 设置环境变量，这是Slack用户的身份令牌，用于认证。
    monkeypatch.setenv("SLACK_USER_TOKEN", "slack_user_token")

    # 返回一个SlackLoader的实例，这个实例已经用我们设定的“假装”功能初始化好了。
    return SlackLoader()

# 这个测试函数检查SlackLoader实例是否正确初始化。
def test_slack_loader_initialization(slack_loader):
    # 断言，确保SlackLoader的client属性不是None，即已经成功创建。
    assert slack_loader.client is not None
    # 断言，检查SlackLoader的配置是否符合预期。
    assert slack_loader.config == {"base_url": "https://www.slack.com/api/"}

# 测试函数，检查SlackLoader的_setup_loader方法是否能更改基础URL。
def test_slack_loader_setup_loader(slack_loader):
    # 调用_setup_loader方法，传入自定义的基础URL。
    slack_loader._setup_loader({"base_url": "https://custom.slack.api/"})

    # 确认client仍然存在，即方法执行后没有破坏实例。
    assert slack_loader.client is not None

# 测试函数，检查SlackLoader的_check_query方法是否能识别有效的查询字符串。
def test_slack_loader_check_query(slack_loader):
    # 定义一个有效的查询字符串。
    valid_json_query = "test_query"
    # 定义一个无效的查询，这里是一个数字，而查询应该是字符串。
    invalid_query = 123

    # 调用_check_query方法，传入有效查询，应该正常运行。
    slack_loader._check_query(valid_json_query)

    # 使用pytest的raises上下文管理器来确认当传入无效查询时，会抛出ValueError异常。
    with pytest.raises(ValueError):
        slack_loader._check_query(invalid_query)

# 测试函数，检查SlackLoader的load_data方法是否能处理数据加载。
def test_slack_loader_load_data(slack_loader, mocker):
    # 定义一个有效的查询字符串，这里是"in:random"，它代表一种查询类型。
    valid_json_query = "in:random"

    # 模拟client的search_messages方法，让它返回一个空的消息字典，这样测试时不会真的去查找消息。
    mocker.patch.object(slack_loader.client, "search_messages", return_value={"messages": {}})

    # 调用load_data方法，传入有效查询，获取结果。
    result = slack_loader.load_data(valid_json_query)

    # 检查返回的结果中是否包含"doc_id"和"data"这两个键，这是期望的数据结构。
    assert "doc_id" in result
    assert "data" in result

