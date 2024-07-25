# 首先，我们导入了一些工具箱里的工具，就像准备画画前要准备好颜料和画笔。
import hashlib   # 这是我们的“加密调色板”，用来生成独一无二的颜色（哈希值）。
import logging  # 这是我们的“日记本”，用来记录程序运行过程中的重要信息。
from typing import Any, Optional  # 这些是用来帮助我们描述变量类型的“说明书”。

# 接下来，我们从一个更大的“工具包”里拿出了一个特别的工具。
from embedchain.loaders.base_loader import BaseLoader

# 然后，我们创建了一个“日记本”的“一页”，用来写日志。
logger = logging.getLogger(__name__)

# 现在，我们要开始造我们的“小车”了，这辆“小车”叫做PostgresLoader，它专门用来从PostgreSQL数据库里搬东西。
class PostgresLoader(BaseLoader):
    # 这是我们的“小车”构造方法，就像组装一辆新自行车时看的说明书。
    def __init__(self, config: Optional[dict[str, Any]] = None):
        # 首先，我们调用了“父类”的构造方法，就像在组装自行车前先检查一下零件是否齐全。
        super().__init__()

        # 如果没有提供配置信息，我们会告诉用户这是必须的，就像骑车前必须检查轮胎气压一样。
        if not config:
            raise ValueError(f"Must provide the valid config. Received: {config}")

        # 我们还准备了两个“箱子”，一个用来装“小车”的连接，另一个用来装“小车”的“方向盘”。
        self.connection = None
        self.cursor = None

        # 现在，我们要设置我们的“小车”，让它知道怎么去数据库那里。
        self._setup_loader(config=config)

    # 这个方法就像是给“小车”加油，让它准备好出发。
    def _setup_loader(self, config: dict[str, Any]):
        # 首先，我们确保有必要的“燃料”——psycopg库，如果没有，我们会告诉用户如何获取。
        try:
            import psycopg
        except ImportError as e:
            # 提醒用户如果缺少“燃料”，需要怎样做才能继续。
            raise ImportError(
                "Unable to import required packages. \
                    Run `pip install --upgrade 'embedchain[postgres]'`"
            ) from e

        # 接下来，我们根据配置信息设置“小车”的路线。
        if "url" in config:
            config_info = config.get("url")
        else:
            # 如果没有直接给出“URL”，我们就把所有配置信息拼接成一个完整的“路线图”。
            conn_params = []
            for key, value in config.items():
                conn_params.append(f"{key}={value}")
            config_info = " ".join(conn_params)

        # 在日记本上记下我们即将前往的地方。
        logger.info(f"Connecting to postrgres sql: {config_info}")

        # 使用“路线图”启动“小车”，并与数据库建立连接。
        self.connection = psycopg.connect(conninfo=config_info)
        self.cursor = self.connection.cursor()

    # 这个静态方法像是一个检查站，确保我们的查询语句是正确的。
    @staticmethod
    def _check_query(query):
        # 如果查询不是字符串类型，我们会提醒用户并告诉他们正确的做法。
        if not isinstance(query, str):
            raise ValueError(
                f"Invalid postgres query: {query}. Provide the valid source to add from postgres, make sure you are following `https://docs.embedchain.ai/data-sources/postgres`",
            )

    # 这个方法是我们的“小车”真正开始工作的地方，它会根据查询语句从数据库中搬数据。
    def load_data(self, query):
        # 先通过检查站，确保一切正常。
        self._check_query(query)
        
        # 然后尝试执行查询，收集数据。
        try:
            data = []  # 这是我们用来装载数据的“篮子”。
            data_content = []  # 这是另一个“篮子”，用来装数据的内容部分。

            # 让“小车”的“方向盘”开始工作，执行查询。
            self.cursor.execute(query)
            results = self.cursor.fetchall()  # 收集所有结果。

            # 遍历所有的结果，把它们整理好，放进我们的“篮子”里。
            for result in results:
                doc_content = str(result)
                data.append({"content": doc_content, "meta_data": {"url": query}})
                data_content.append(doc_content)

            # 使用哈希函数生成一个独一无二的“车牌号”，以便识别这些数据。
            doc_id = hashlib.sha256((query + ", ".join(data_content)).encode()).hexdigest()

            # 最后，我们把“车牌号”和装满数据的“篮子”打包好，准备返回。
            return {
                "doc_id": doc_id,
                "data": data,
            }
        except Exception as e:
            # 如果在搬运过程中出错了，我们会告诉用户哪里出了问题。
            raise ValueError(f"Failed to load data using query={query} with: {e}")

    # 当我们不再需要“小车”时，这个方法会帮助我们安全地关闭它，释放资源。
    def close_connection(self):
        # 如果“方向盘”还在，我们就先把它关掉。
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        # 然后，如果“小车”的引擎还在运行，我们就关闭它。
        if self.connection:
            self.connection.close()
            self.connection = None

