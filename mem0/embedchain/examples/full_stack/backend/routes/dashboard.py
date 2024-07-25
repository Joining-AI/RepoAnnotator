# 导入需要的模块
from flask import Blueprint, jsonify, make_response, request
# 导入数据库模型
from models import APIKey, BotList, db

# 创建一个蓝图，蓝图的名字是"dashboard"
dashboard_bp = Blueprint("dashboard", __name__)

# 定义一个路由，用来设置OpenAI的密钥，这个接口只允许POST请求
@dashboard_bp.route("/api/set_key", methods=["POST"])
def set_key():
    # 获取前端发来的JSON数据
    data = request.get_json()
    # 从数据中取出OpenAI密钥
    api_key = data["openAIKey"]
    # 查询数据库中是否已经有OpenAI密钥记录
    existing_key = APIKey.query.first()
    # 如果已经有记录，就更新密钥
    if existing_key:
        existing_key.key = api_key
    # 如果没有记录，就新建一条记录
    else:
        new_key = APIKey(key=api_key)
        db.session.add(new_key)
    # 提交更改到数据库
    db.session.commit()
    # 返回一个成功的响应给前端
    return make_response(jsonify(message="API key saved successfully"), 200)

# 定义一个路由，用来检查OpenAI的密钥是否存在，这个接口只允许GET请求
@dashboard_bp.route("/api/check_key", methods=["GET"])
def check_key():
    # 查询数据库中是否已经有OpenAI密钥记录
    existing_key = APIKey.query.first()
    # 如果有记录，则返回成功信息
    if existing_key:
        return make_response(jsonify(status="ok", message="OpenAI Key exists"), 200)
    # 如果没有记录，则返回失败信息
    else:
        return make_response(jsonify(status="fail", message="No OpenAI Key present"), 200)

# 定义一个路由，用来创建一个新的聊天机器人，这个接口只允许POST请求
@dashboard_bp.route("/api/create_bot", methods=["POST"])
def create_bot():
    # 获取前端发来的JSON数据
    data = request.get_json()
    # 从数据中取出机器人的名字
    name = data["name"]
    # 将名字转换成小写并用下划线替换空格作为唯一标识符
    slug = name.lower().replace(" ", "_")
    # 查询数据库中是否已经有这个名字的机器人
    existing_bot = BotList.query.filter_by(slug=slug).first()
    # 如果已经有了，则返回错误信息
    if existing_bot:
        return (make_response(jsonify(message="Bot already exists"), 400),)
    # 如果没有，则新建一个机器人记录
    new_bot = BotList(name=name, slug=slug)
    db.session.add(new_bot)
    db.session.commit()
    # 返回一个成功的响应给前端
    return make_response(jsonify(message="Bot created successfully"), 200)

# 定义一个路由，用来删除一个聊天机器人，这个接口只允许POST请求
@dashboard_bp.route("/api/delete_bot", methods=["POST"])
def delete_bot():
    # 获取前端发来的JSON数据
    data = request.get_json()
    # 从数据中取出机器人的唯一标识符
    slug = data.get("slug")
    # 根据标识符查询机器人
    bot = BotList.query.filter_by(slug=slug).first()
    # 如果找到了机器人，则删除它
    if bot:
        db.session.delete(bot)
        db.session.commit()
        # 返回一个成功的响应给前端
        return make_response(jsonify(message="Bot deleted successfully"), 200)
    # 如果没找到，则返回错误信息
    return make_response(jsonify(message="Bot not found"), 400)

# 定义一个路由，用来获取所有聊天机器人的列表，这个接口只允许GET请求
@dashboard_bp.route("/api/get_bots", methods=["GET"])
def get_bots():
    # 查询所有的机器人记录
    bots = BotList.query.all()
    # 创建一个空列表来存放机器人的信息
    bot_list = []
    # 遍历所有的机器人记录
    for bot in bots:
        # 将每个机器人的名字和标识符添加到列表中
        bot_list.append(
            {
                "name": bot.name,
                "slug": bot.slug,
            }
        )
    # 返回机器人列表给前端
    return jsonify(bot_list)

