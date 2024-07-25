# 这行代码是从一个叫 sqlalchemy 的大工具包里拿出一个叫 create_engine 的小工具。
from sqlalchemy import create_engine
# 这行代码是从同一个大工具包 sqlalchemy 里拿出一个叫 declarative_base 的小工具。
from sqlalchemy.ext.declarative import declarative_base
# 这行代码还是从同一个大工具包 sqlalchemy 里拿出一个叫 sessionmaker 的小工具。
from sqlalchemy.orm import sessionmaker

# 这行代码定义了一个数据库的地址，就像是告诉我们的程序数据库藏在哪里。
# 这里说的是一个 sqlite 数据库，它保存在和我们程序同一目录下的 app.db 文件里。
SQLALCHEMY_DATABASE_URI = "sqlite:///./app.db"

# 这行代码是使用上面提到的 create_engine 小工具，根据数据库地址创建一个数据库引擎。
# 这个引擎就像是开车需要的发动机一样，有了它我们才能连接到数据库。
# 连接参数里的 "check_same_thread": False 告诉这个引擎不需要检查线程，这样不同地方可以同时访问数据库。
engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})

# 这行代码是使用 sessionmaker 工具根据前面创建的引擎创建一个 SessionLocal 类。
# SessionLocal 类就像是一个门，通过它可以进入数据库操作数据。
# autocommit=False 和 autoflush=False 这两个参数告诉它不要自动提交更改和刷新数据，我们需要手动控制这些操作。
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 这行代码是使用 declarative_base 工具创建一个 Base 类。
# Base 类就像是一个蓝图，我们可以基于它来定义数据库里面的各种表格（模型）。
Base = declarative_base()

