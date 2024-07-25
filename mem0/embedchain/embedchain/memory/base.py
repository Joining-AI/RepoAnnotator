# 导入一个叫做 json 的工具包，这个工具包可以帮助我们处理数据。
import json

# 导入一个叫做 logging 的工具包，这个工具包可以帮我们记录程序运行时发生了什么。
import logging

# 导入一个叫做 uuid 的工具包，这个工具包可以生成独一无二的编号。
import uuid

# 从 typing 这个工具包里导入两个东西：Any 和 Optional。它们可以帮助我们更好地描述代码里的数据类型。
from typing import Any, Optional

# 从 embedchain 这个项目的核心数据库模块里导入 get_session 这个函数，它能帮助我们连接到数据库。
from embedchain.core.db.database import get_session

# 从 embedchain 的核心数据库模块里导入 ChatHistoryModel 这个类，它是用来描述聊天记录在数据库中的表现形式的。
from embedchain.core.db.models import ChatHistory as ChatHistoryModel

# 从 embedchain 的记忆模块导入 ChatMessage 这个类，它可以用来表示一条聊天消息。
from embedchain.memory.message import ChatMessage

# 从 embedchain 的记忆模块导入 merge_metadata_dict 这个函数，它可以帮助我们合并一些关于消息的额外信息。
from embedchain.memory.utils import merge_metadata_dict

# 设置一个记录器（logger），当我们需要记录一些信息的时候就会用到它。
logger = logging.getLogger(__name__)

class ChatHistory:  # 定义一个叫做ChatHistory的类，就像一个工具箱，里面装着处理聊天记录的工具。
    def __init__(self) -> None:  # 初始化方法，当创建类的对象时会被调用。
        self.db_session = get_session()  # 获取数据库会话，就像打开一个数据库的门，准备存取数据。

    def add(self, app_id, session_id, chat_message: ChatMessage) -> Optional[str]:  # 添加聊天记录的方法。
        memory_id = str(uuid.uuid4())  # 生成一个唯一的ID，就像是给每条聊天记录贴上一个独一无二的标签。
        metadata_dict = merge_metadata_dict(chat_message.human_message.metadata, chat_message.ai_message.metadata)  # 合并元数据，就是把一些额外的信息整理在一起。
        if metadata_dict:  # 如果有元数据的话...
            metadata = self._serialize_json(metadata_dict)  # 把元数据转换成字符串形式，这样数据库才能保存它。
        self.db_session.add(  # 准备往数据库里添加一条聊天记录。
            ChatHistoryModel(  # 创建一个聊天记录模型对象。
                app_id=app_id,  # 设置应用ID，就像是聊天记录的来源。
                id=memory_id,  # 设置我们刚才生成的唯一ID。
                session_id=session_id,  # 设置会话ID，帮助我们追踪同一场对话的所有消息。
                question=chat_message.human_message.content,  # 记录人类用户发的消息内容。
                answer=chat_message.ai_message.content,  # 记录AI回复的内容。
                metadata=metadata if metadata_dict else "{}",  # 如果有元数据就用元数据，否则用空的字典字符串。
            )
        )
        try:  # 尝试执行下面的操作，如果出错就去except那里处理。
            self.db_session.commit()  # 提交更改到数据库，就像告诉数据库“这些是你要保存的数据”。
        except Exception as e:  # 如果上面的操作出错了...
            logger.error(f"Error adding chat memory to db: {e}")  # 打印错误信息，告诉我们哪里出了问题。
            self.db_session.rollback()  # 撤销刚才的更改，就像撤销了一次错误的修改。
            return None  # 返回None表示操作失败。

        logger.info(f"Added chat memory to db with id: {memory_id}")  # 如果一切顺利，打印成功信息。
        return memory_id  # 返回刚才生成的唯一ID。

    def delete(self, app_id: str, session_id: Optional[str] = None):  # 删除聊天记录的方法。
        """
        这个方法用于删除特定应用和会话的所有聊天记录。
        """
        params = {"app_id": app_id}  # 设置参数，至少需要应用ID。
        if session_id:  # 如果有会话ID的话...
            params["session_id"] = session_id  # 加入会话ID作为参数。
        self.db_session.query(ChatHistoryModel).filter_by(**params).delete()  # 查询符合参数的聊天记录并删除它们。
        try:  # 尝试执行下面的操作，如果出错就去except那里处理。
            self.db_session.commit()  # 提交更改到数据库，确认删除操作。
        except Exception as e:  # 如果上面的操作出错了...
            logger.error(f"Error deleting chat history: {e}")  # 打印错误信息，告诉我们哪里出了问题。
            self.db_session.rollback()  # 撤销刚才的更改，就像撤销了一次错误的修改。

    def get(self, app_id, session_id: str = "default", num_rounds=10, fetch_all: bool = False, display_format=False) -> list[ChatMessage]:  # 获取聊天记录的方法。
        """
        这个方法用于获取特定应用的聊天记录，可以指定会话ID、获取轮数、是否获取所有记录以及是否以展示格式返回。
        """
        params = {"app_id": app_id}  # 设置参数，至少需要应用ID。
        if not fetch_all:  # 如果不是获取所有记录的话...
            params["session_id"] = session_id  # 加入会话ID作为参数。
        results = (  # 查询符合条件的聊天记录。
            self.db_session.query(ChatHistoryModel).filter_by(**params).order_by(ChatHistoryModel.created_at.asc())
        )
        results = results.limit(num_rounds) if not fetch_all else results  # 如果不是获取所有记录，限制结果数量。
        history = []  # 创建一个空列表来存放聊天记录。
        for result in results:  # 遍历查询结果。
            metadata = self._deserialize_json(metadata=result.meta_data or "{}")  # 解析元数据，从字符串转回字典。
            if display_format:  # 如果要求以展示格式返回...
                history.append(  # 把聊天记录以字典形式加入列表。
                    {
                        "session_id": result.session_id,
                        "human": result.question,
                        "ai": result.answer,
                        "metadata": result.meta_data,
                        "timestamp": result.created_at,
                    }
                )
            else:  # 否则，创建一个聊天消息对象并加入列表。
                memory = ChatMessage()
                memory.add_user_message(result.question, metadata=metadata)
                memory.add_ai_message(result.answer, metadata=metadata)
                history.append(memory)
        return history  # 返回聊天记录列表。

    def count(self, app_id: str, session_id: Optional[str] = None):  # 计算聊天记录数量的方法。
        """
        这个方法用于计算特定应用和会话的聊天记录数量。
        """
        params = {"app_id": app_id}  # 设置参数，至少需要应用ID。
        if session_id:  # 如果有会话ID的话...
            params["session_id"] = session_id  # 加入会话ID作为参数。
        return self.db_session.query(ChatHistoryModel).filter_by(**params).count()  # 查询并返回记录数量。

    @staticmethod  # 静态方法，不需要访问类或实例的属性。
    def _serialize_json(metadata: dict[str, Any]):  # 把字典转换成JSON字符串。
        return json.dumps(metadata)

    @staticmethod  # 静态方法，不需要访问类或实例的属性。
    def _deserialize_json(metadata: str):  # 把JSON字符串转换成字典。
        return json.loads(metadata)

    def close_connection(self):  # 关闭数据库连接的方法。
        self.connection.close()  # 关闭数据库连接，就像关上门一样。

