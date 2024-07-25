import copy
# 这行代码引入了一个叫“copy”的库，它可以让程序复制对象，就像你在画画时复印一张画一样。

import os
# 引入了一个叫“os”的库，这个库可以让我们跟电脑的操作系统进行交流，比如读取文件或获取环境变量等。

from typing import Optional, Union
# 这行代码是从一个叫做“typing”的库中引入了两个东西：Optional 和 Union。
# Optional 可以用来表示某个值可能不存在（None），Union 表示一个变量可以是几种类型中的任意一种。

try:
    import weaviate
# 这里尝试从一个叫做“weaviate”的库导入一些功能，这个库就是用来连接和操作 Weaviate 数据库的。

except ImportError:
# 如果上面那行代码运行出错，也就是找不到 “weaviate” 库，就会执行下面的代码。

    raise ImportError(
# 抛出一个错误信息，告诉用户需要安装额外的依赖项（也就是“weaviate”库）。
# 这个错误信息还告诉用户怎么去安装这个库，就是用 pip 命令。

        "Weaviate requires extra dependencies. Install with `pip install --upgrade 'embedchain[weaviate]'`"
    ) from None

from embedchain.config.vector_db.weaviate import WeaviateDBConfig
# 这行代码是从一个叫做 “embedchain” 的项目中找到一个特定的配置文件 “WeaviateDBConfig”，这个配置文件包含了一些设置，让我们的程序知道如何跟 Weaviate 数据库交流。

from embedchain.helpers.json_serializable import register_deserializable
# 这行代码是从 “embedchain” 项目中找到一个工具，这个工具可以帮助我们把某些对象转换成 JSON 格式，这样就可以更容易地保存到数据库里，或者在网络上发送给别人。

from embedchain.vectordb.base import BaseVectorDB
# 这行代码是从 “embedchain” 项目中找到一个基础类 “BaseVectorDB”。这个类定义了一些基本的行为，所有跟向量数据库相关的类都会继承这个类的功能。

@register_deserializable
# 这个装饰器标记了下面的类，意味着这个类可以被序列化成 JSON 格式，也可以从 JSON 格式反序列化回来。

class WeaviateDB(BaseVectorDB):

