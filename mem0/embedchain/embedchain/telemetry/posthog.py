# 导入需要的模块
import json
import logging
import os
import uuid

# 导入Posthog这个工具，用来发送匿名数据
from posthog import Posthog

# 导入我们项目的一些模块和常量
import embedchain
from embedchain.constants import CONFIG_DIR, CONFIG_FILE

