# 这一行是从Flask-SQLAlchemy这个工具包里导入了一个叫SQLAlchemy的类。
from flask_sqlalchemy import SQLAlchemy

# 这一行是创建了一个SQLAlchemy类的对象，名字叫做db。这个对象可以帮助我们和数据库进行交流。
db = SQLAlchemy()

# 这一行开始定义了一个名为APIKey的新类，它继承了db.Model。这意味着这个类会成为一个数据库中的表。
class APIKey(db.Model):
    # 这一行是在APIKey这个类里面定义了一个名为id的列（字段），它是整数类型，并且是主键。
    # 主键的意思是这个列的值对于每一条记录来说都是唯一的，可以用来唯一标识一条记录。
    id = db.Column(db.Integer, primary_key=True)
    # 这一行定义了另一个名为key的列，它是字符串类型，长度最多255个字符，并且不允许为空。
    # 不允许为空的意思是这个字段必须要有值。
    key = db.Column(db.String(255), nullable=False)

# 这一行又定义了一个新的类，名字叫做BotList，同样继承了db.Model。
class BotList(db.Model):
    # 这一行定义了BotList类里的id列，它是整数类型，并且是主键。
    id = db.Column(db.Integer, primary_key=True)
    # 这一行定义了name列，它是字符串类型，最多255个字符，并且也不允许为空。
    name = db.Column(db.String(255), nullable=False)
    # 这一行定义了slug列，它是字符串类型，最多255个字符，不允许为空，并且要求每一项都必须是唯一的。
    # 唯一的意思是这个字段的值在所有记录中不能重复。
    slug = db.Column(db.String(255), nullable=False, unique=True)

