import os  # 这行代码是引入了一个叫做“os”的工具包，它可以帮助我们和电脑的操作系统进行交流。
from typing import Optional, Union  # 引入了两个工具，Optional 和 Union，它们用来帮助我们更好地描述变量可以是什么类型。

from embedchain.config.vector_db.base import BaseVectorDbConfig  # 引入了一个叫做 BaseVectorDbConfig 的类，这个类是用来配置数据库的。
from embedchain.helpers.json_serializable import register_deserializable  # 引入了一个装饰器，叫做 register_deserializable，它可以帮我们把类变成可以被保存成 JSON 格式的东西。

@register_deserializable  # 这个装饰器用在这里，意味着我们下面定义的类可以被保存成 JSON。
class ElasticsearchDBConfig(BaseVectorDbConfig):  # 定义了一个新的类，叫 ElasticsearchDBConfig，它是从 BaseVectorDbConfig 类继承来的。
    def __init__(self,  # 这是类的初始化方法，当创建这个类的一个实例时，这些代码就会执行。
                 collection_name: Optional[str] = None,  # 这个参数是可选的，用于设置默认的集合名字。
                 dir: Optional[str] = None,  # 可选参数，用于指定数据库存储的目录路径。
                 es_url: Union[str, list[str]] = None,  # 可以是一个字符串或字符串列表，代表 Elasticsearch 的地址。
                 cloud_id: Optional[str] = None,  # 可选参数，用于连接到云上的 Elasticsearch 集群。
                 batch_size: Optional[int] = 100,  # 插入数据时一次处理的数据量，默认是100。
                 **ES_EXTRA_PARAMS: dict[str, any],  # 这是一个字典，可以接受额外的参数，用于配置 Elasticsearch。
                ):
        if es_url and cloud_id:  # 如果同时设置了 es_url 和 cloud_id，这是不允许的，会抛出错误。
            raise ValueError("Only one of `es_url` and `cloud_id` can be set.")

        self.ES_URL = es_url or os.environ.get("ELASTICSEARCH_URL")  # 设置 ES_URL，如果没有传入，就尝试从环境变量中获取。
        self.CLOUD_ID = cloud_id or os.environ.get("ELASTICSEARCH_CLOUD_ID")  # 设置 CLOUD_ID，如果没有传入，也从环境变量中获取。

        if not self.ES_URL and not self.CLOUD_ID:  # 如果 ES_URL 和 CLOUD_ID 都没有设置，程序会报错。
            raise AttributeError(  # 报错信息，告诉我们需要设置 ES_URL 或者 CLOUD_ID。
                "Elasticsearch needs a URL or CLOUD_ID attribute, "
                "this can either be passed to `ElasticsearchDBConfig` or as `ELASTICSEARCH_URL` or `ELASTICSEARCH_CLOUD_ID` in `.env`"
            )

        self.ES_EXTRA_PARAMS = ES_EXTRA_PARAMS  # 设置额外的参数。

        # 如果额外参数中没有 api_key、basic_auth 和 bearer_auth，就尝试从环境变量中获取 api_key。
        if (
            not self.ES_EXTRA_PARAMS.get("api_key")
            and not self.ES_EXTRA_PARAMS.get("basic_auth")
            and not self.ES_EXTRA_PARAMS.get("bearer_auth")
        ):
            self.ES_EXTRA_PARAMS["api_key"] = os.environ.get("ELASTICSEARCH_API_KEY")

        self.batch_size = batch_size  # 设置 batch_size。
        super().__init__(collection_name=collection_name, dir=dir)  # 调用父类的初始化方法，传递集合名字和目录路径。

