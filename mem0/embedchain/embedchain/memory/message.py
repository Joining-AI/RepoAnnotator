# 导入日志模块，用来记录程序运行的信息。
import logging
# 导入类型提示相关的模块，帮助我们更好地理解变量和参数的类型。
from typing import Any, Optional

# 从 embedchain 的 helpers 模块中导入 JSONSerializable 类，
# 这个类可以帮助我们将数据转换成 JSON 格式，方便存储和传输。
from embedchain.helpers.json_serializable import JSONSerializable

# 创建一个名为 logger 的日志记录器，用来记录这个文件里的日志信息。
logger = logging.getLogger(__name__)

# 定义了一个叫做 BaseMessage 的类，它是所有消息的基础类。
class BaseMessage(JSONSerializable):
    """
    这是基础的消息类。
    消息是用来跟模型交流的东西。
    """

    # 消息的内容，比如文字。
    content: str

    # 谁创建了这条消息，比如是人还是 AI。
    created_by: str

    # 一些额外的信息，可以存放任何东西。
    metadata: dict[str, Any]

    # 初始化方法，当创建一个新的 BaseMessage 对象时会被调用。
    def __init__(self, content: str, created_by: str, metadata: Optional[dict[str, Any]] = None) -> None:
        # 调用父类的初始化方法。
        super().__init__()
        # 设置消息的内容。
        self.content = content
        # 设置谁创建了这条消息。
        self.created_by = created_by
        # 设置额外的信息。
        self.metadata = metadata

    # 一个属性方法，返回消息的类型，这里还没定义具体返回什么。
    @property
    def type(self) -> str:
        """返回消息的类型，用于序列化（就是把对象变成字符串之类的过程）。"""

    # 类方法，检查这个类是否可以被序列化。
    @classmethod
    def is_lc_serializable(cls) -> bool:
        """检查这个类是否可以被序列化。"""
        return True

    # 当我们需要将消息对象转换成字符串的时候会用到这个方法。
    def __str__(self) -> str:
        # 返回创建者是谁加上消息内容。
        return f"{self.created_by}: {self.content}"

# 定义了一个叫做 ChatMessage 的类，它是聊天消息的基础类。
class ChatMessage(JSONSerializable):
    """
    这是聊天消息的基础类。
    聊天消息是由人和模型之间的问答组成的对话。
    """

    # 人类发送的消息。
    human_message: Optional[BaseMessage] = None
    # AI 发送的消息。
    ai_message: Optional[BaseMessage] = None

    # 添加人类发送的消息的方法。
    def add_user_message(self, message: str, metadata: Optional[dict] = None):
        # 如果已经有了一条人类的消息，就打印一条日志信息，说明要覆盖之前的消息。
        if self.human_message:
            logger.info(
                "Human message already exists in the chat message,\ 
                overwriting it with new message."
            )
        # 创建一条人类发送的消息并保存在 human_message 属性里。
        self.human_message = BaseMessage(content=message, created_by="human", metadata=metadata)

    # 添加 AI 发送的消息的方法。
    def add_ai_message(self, message: str, metadata: Optional[dict] = None):
        # 如果已经有一条 AI 的消息，就打印一条日志信息，说明要覆盖之前的消息。
        if self.ai_message:
            logger.info(
                "AI message already exists in the chat message,\ 
                overwriting it with new message."
            )
        # 创建一条 AI 发送的消息并保存在 ai_message 属性里。
        self.ai_message = BaseMessage(content=message, created_by="ai", metadata=metadata)

    # 将聊天消息对象转换成字符串的方法。
    def __str__(self) -> str:
        # 返回人类消息和 AI 消息的内容。
        return f"{self.human_message}\n{self.ai_message}"

