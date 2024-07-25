# 导入需要的库
import hashlib
# 导入模拟对象的功能，用于测试时假装有数据库连接
from unittest.mock import MagicMock
# 导入pytest库，这是一个常用的Python测试框架
import pytest

# 导入MySQLLoader类，这是用来从MySQL数据库加载数据的工具
from embedchain.loaders.mysql import MySQLLoader

# 这个函数是为了设置测试环境，它会创建一个假的MySQL连接
@pytest.fixture
def mysql_loader(mocker):
    # 使用mocker模拟MySQL连接，这样我们不用真的连接到数据库就能测试
    with mocker.patch("mysql.connector.connection.MySQLConnection"):
        # 这里定义了连接数据库需要的信息
        config = {
            "host": "localhost",  # 数据库服务器的位置
            "port": "3306",       # 连接数据库的端口
            "user": "your_username",  # 登录数据库的用户名
            "password": "your_password",  # 登录数据库的密码
            "database": "your_database",  # 要连接的数据库名字
        }
        # 创建MySQLLoader实例
        loader = MySQLLoader(config=config)
        # 返回这个实例给测试函数使用
        yield loader

# 测试函数，检查初始化是否成功
def test_mysql_loader_initialization(mysql_loader):
    # 确认配置信息不是空的
    assert mysql_loader.config is not None
    # 确认连接对象不是空的
    assert mysql_loader.connection is not None
    # 确认游标对象不是空的（游标是用来执行SQL语句的东西）
    assert mysql_loader.cursor is not None

# 测试函数，如果配置信息为空则应报错
def test_mysql_loader_invalid_config():
    # 尝试创建MySQLLoader实例时传入空配置
    with pytest.raises(ValueError, match="Invalid sql config: None"):
        MySQLLoader(config=None)

# 又一个测试函数，检查连接数据库是否成功
def test_mysql_loader_setup_loader_successful(mysql_loader):
    # 检查连接对象和游标对象都不为空
    assert mysql_loader.connection is not None
    assert mysql_loader.cursor is not None

# 测试函数，模拟连接失败的情况
def test_mysql_loader_setup_loader_connection_error(mysql_loader, mocker):
    # 使用mocker模拟连接失败
    mocker.patch("mysql.connector.connection.MySQLConnection", side_effect=IOError("Mocked connection error"))
    # 如果配置信息不对，则应该报错
    with pytest.raises(ValueError, match="Unable to connect with the given config:"):
        mysql_loader._setup_loader(config={})

# 测试函数，检查查询语句是否正确
def test_mysql_loader_check_query_successful(mysql_loader):
    # 正常的SQL查询语句
    query = "SELECT * FROM table"
    # 检查查询语句是否被正确处理
    mysql_loader._check_query(query=query)

# 测试函数，检查非法的查询语句是否会报错
def test_mysql_loader_check_query_invalid(mysql_loader):
    # 非法的查询语句（这里用数字123代替正常的SQL语句）
    with pytest.raises(ValueError, match="Invalid mysql query: 123"):
        mysql_loader._check_query(query=123)

# 测试函数，检查加载数据是否成功
def test_mysql_loader_load_data_successful(mysql_loader, mocker):
    # 模拟游标对象
    mock_cursor = MagicMock()
    # 把模拟的游标对象设置给mysql_loader
    mocker.patch.object(mysql_loader, "cursor", mock_cursor)
    # 模拟查询结果
    mock_cursor.fetchall.return_value = [(1, "data1"), (2, "data2")]
    
    # 正常的SQL查询语句
    query = "SELECT * FROM table"
    # 加载数据并检查结果
    result = mysql_loader.load_data(query)
    
    # 检查返回的数据格式是否正确
    assert "doc_id" in result
    assert "data" in result
    assert len(result["data"]) == 2
    assert result["data"][0]["meta_data"]["url"] == query
    assert result["data"][1]["meta_data"]["url"] == query
    
    # 生成文档ID
    doc_id = hashlib.sha256((query + ", ".join([d["content"] for d in result["data"]])).encode()).hexdigest()
    
    # 检查文档ID是否正确生成
    assert result["doc_id"] == doc_id
    # 检查查询语句是否被执行
    assert mock_cursor.execute.called_with(query)

# 测试函数，检查非法查询语句在加载数据时是否会报错
def test_mysql_loader_load_data_invalid_query(mysql_loader):
    # 非法的查询语句
    with pytest.raises(ValueError, match="Invalid mysql query: 123"):
        mysql_loader.load_data(query=123)

