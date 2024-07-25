# 我们从一个叫unittest.mock的库中导入了一个叫MagicMock的东西，
# 它可以帮助我们在测试时假装某些功能。
from unittest.mock import MagicMock

# 这是我们要连接的那个数据库的Python库。
import psycopg

# pytest是一个工具，它帮助我们测试代码。
import pytest

# 这是我们的PostgresLoader类，它能帮我们从PostgreSQL数据库加载数据。
from embedchain.loaders.postgres import PostgresLoader

# 下面是一个pytest的特殊函数，叫做fixture。它会在每个测试开始前运行，
# 并提供一些初始化的环境。这里我们创建了一个PostgresLoader实例，
# 但是我们假装psycopg.connect这个函数，这样我们不用真的连接到数据库，
# 只是为了测试。
@pytest.fixture
def postgres_loader(mocker):
    # 我们假装psycopg.connect这个函数，mocker是用来做这个的。
    with mocker.patch.object(psycopg, "connect"):
        # 这是我们连接数据库需要的配置信息，但因为我们只是在测试，
        # 所以这些信息是假的。
        config = {"url": "postgres://user:password@localhost:5432/database"}
        # 创建一个PostgresLoader实例，并把它返回给测试函数使用。
        loader = PostgresLoader(config=config)
        yield loader

# 这个测试函数检查PostgresLoader实例是否正确初始化了。
def test_postgres_loader_initialization(postgres_loader):
    # 确保连接和游标（用于执行SQL语句）不是None，也就是它们被正确创建了。
    assert postgres_loader.connection is not None
    assert postgres_loader.cursor is not None

# 这个测试函数检查如果配置信息没有给出，会怎样。
def test_postgres_loader_invalid_config():
    # 如果config参数是None，应该抛出一个ValueError异常，
    # 因为我们必须给正确的配置信息。
    with pytest.raises(ValueError, match="Must provide the valid config. Received: None"):
        PostgresLoader(config=None)

# 这个测试函数检查load_data方法是否能正确工作。
def test_load_data(postgres_loader, monkeypatch):
    # 我们创建一个假装的游标对象，因为真正的游标我们并不想用。
    mock_cursor = MagicMock()
    # 我们用monkeypatch来替换掉真实的游标对象，用我们创建的假装游标。
    monkeypatch.setattr(postgres_loader, "cursor", mock_cursor)

    # 这是我们想要从数据库获取数据的SQL查询语句。
    query = "SELECT * FROM table"
    # 我们假装当执行查询时，会得到两行数据。
    mock_cursor.fetchall.return_value = [(1, "data1"), (2, "data2")]

    # 调用load_data方法，并检查返回的数据是否正确。
    result = postgres_loader.load_data(query)

    # 确保返回的结果包含必要的键。
    assert "doc_id" in result
    assert "data" in result
    # 检查数据的数量是否正确。
    assert len(result["data"]) == 2
    # 检查元数据中的URL是否和查询语句一致。
    assert result["data"][0]["meta_data"]["url"] == query
    assert result["data"][1]["meta_data"]["url"] == query
    # 确认假装的游标确实被调用来执行查询。
    assert mock_cursor.execute.called_with(query)

# 这个测试函数检查当有异常发生时，load_data方法的反应。
def test_load_data_exception(postgres_loader, monkeypatch):
    # 同样，我们创建一个假装的游标对象。
    mock_cursor = MagicMock()
    # 用monkeypatch替换真实的游标。
    monkeypatch.setattr(postgres_loader, "cursor", mock_cursor)

    # 假装的查询语句。
    _ = "SELECT * FROM table"
    # 当假装的游标执行查询时，会抛出一个异常。
    mock_cursor.execute.side_effect = Exception("Mocked exception")

    # 确认当执行查询时，如果出现异常，会抛出ValueError异常。
    with pytest.raises(
        ValueError, match=r"Failed to load data using query=SELECT \* FROM table with: Mocked exception"
    ):
        postgres_loader.load_data("SELECT * FROM table")

# 这个测试函数检查关闭数据库连接的方法是否有效。
def test_close_connection(postgres_loader):
    # 调用关闭连接的方法。
    postgres_loader.close_connection()
    # 确认游标和连接都被设置成了None，也就是关闭了。
    assert postgres_loader.cursor is None
    assert postgres_loader.connection is None

