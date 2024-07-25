# 导入一个叫做 os 的库，这个库可以帮助我们和电脑的操作系统进行交流。
import os
# 导入一个叫做 pathlib 的库里的 Path 工具，它能帮助我们更方便地处理文件路径。
from pathlib import Path

# 这行代码获取了当前运行这个程序所在的文件夹的完整路径，并把它保存在一个叫 ABS_PATH 的变量里。
ABS_PATH = os.getcwd()
# 这行代码尝试从环境变量中获取一个叫 "EMBEDCHAIN_CONFIG_DIR" 的值，
# 如果没有找到，就用用户家目录作为默认值，并把这个结果保存在 HOME_DIR 变量里。
HOME_DIR = os.environ.get("EMBEDCHAIN_CONFIG_DIR", str(Path.home()))
# 这行代码把 HOME_DIR 和 ".embedchain" 连接起来，形成一个新的路径，用来保存配置文件夹的位置，并保存在 CONFIG_DIR 变量里。
CONFIG_DIR = os.path.join(HOME_DIR, ".embedchain")
# 这行代码把 CONFIG_DIR 和 "config.json" 连接起来，形成一个新的路径，用来保存配置文件的位置，并保存在 CONFIG_FILE 变量里。
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
# 这行代码把 CONFIG_DIR 和 "embedchain.db" 连接起来，形成一个新的路径，用来保存数据库文件的位置，并保存在 SQLITE_PATH 变量里。
SQLITE_PATH = os.path.join(CONFIG_DIR, "embedchain.db")

# 这行代码设置了环境变量 "EMBEDCHAIN_DB_URI"，如果之前没有设置的话，
# 它会自动设置为 "sqlite:///..." 加上刚刚保存的数据库文件路径，这样就知道数据库文件在哪里了。
os.environ.setdefault("EMBEDCHAIN_DB_URI", f"sqlite:///{SQLITE_PATH}")

