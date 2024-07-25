# 引入日志模块，这个模块可以帮助我们记录程序运行时发生的事情。
import logging

# 引入Generator类，这是一个特殊的类，用于生成器，可以节省内存。
from collections.abc import Generator

# 引入Any和Optional类型提示，帮助我们更好地理解和使用变量。
from typing import Any, Optional

# 引入BaseMessage类，这是来自langchain库的一个类，用于处理对话中的消息。
from langchain.schema import BaseMessage as LCBaseMessage

# 引入BaseLlmConfig配置类，这是embedchain库中定义的，用于设置语言模型的基本配置。
from embedchain.config import BaseLlmConfig

# 引入base模块中的几个常量，这些是预设的文本模板，用于构建特定格式的提示信息。
from embedchain.config.llm.base import (
    # 这是默认的提示信息模板。
    DEFAULT_PROMPT,
    # 这是带有历史记录的提示信息模板。
    DEFAULT_PROMPT_WITH_HISTORY_TEMPLATE,
    # 这是带有记忆功能的提示信息模板。
    DEFAULT_PROMPT_WITH_MEM0_MEMORY_TEMPLATE,
    # 这是文档站点的提示信息模板。
    DOCS_SITE_PROMPT_TEMPLATE,
)

# 引入JSONSerializable类，这个类提供了将对象转换成JSON格式的方法，方便数据交换。
from embedchain.helpers.json_serializable import JSONSerializable

# 引入ChatHistory类，这个类用于处理聊天历史记录。
from embedchain.memory.base import ChatHistory

# 引入ChatMessage类，这个类用于表示一条聊天消息。
from embedchain.memory.message import ChatMessage

# 创建一个名为__name__的日志记录器，它会帮助我们记录这个模块中发生的事情。
logger = logging.getLogger(__name__)

# 定义一个名为BaseLlm的类，继承自JSONSerializable（假设这是一个可以序列化为JSON的对象）
class BaseLlm(JSONSerializable):
    # 初始化方法，创建这个类的实例时会被调用
    def __init__(self, config: Optional[BaseLlmConfig] = None):
        """初始化一个基础的语言模型类

        :param config: 语言模型的配置选项类，默认为None
        :type config: Optional[BaseLlmConfig], 可选参数
        """
        # 如果没有提供配置，则创建一个默认的配置实例
        if config is None:
            self.config = BaseLlmConfig()
        else:
            self.config = config

        # 创建一个聊天历史记录对象
        self.memory = ChatHistory()
        # 标记是否是文档站点实例
        self.is_docs_site_instance = False
        # 历史记录属性，类型为任意，可能是用于存储对话历史的
        self.history: Any = None

    # 方法用于获取语言模型的回答，但在这个基础类中没有实现，需要子类去实现
    def get_llm_model_answer(self):
        """
        通常由子类实现的方法
        """
        raise NotImplementedError

    # 设置历史记录的方法
    def set_history(self, history: Any):
        """
        提供你自己的历史记录。
        特别适用于查询方法，该方法内部不管理会话历史。

        :param history: 要设置的历史记录
        :type history: Any
        """
        self.history = history

    # 更新历史记录的方法，从内存中获取并更新类的history属性
    def update_history(self, app_id: str, session_id: str = "default"):
        """根据应用ID和会话ID更新类中的历史记录属性"""
        # 从memory中获取历史记录，限制为最近10轮对话
        chat_history = self.memory.get(app_id=app_id, session_id=session_id, num_rounds=10)
        # 将历史记录转换为字符串列表并设置为当前实例的history属性
        self.set_history([str(history) for history in chat_history])

    # 添加历史记录的方法
    def add_history(
        self,
        app_id: str,
        question: str,
        answer: str,
        metadata: Optional[dict[str, Any]] = None,
        session_id: str = "default",
    ):
        # 创建一个聊天消息对象
        chat_message = ChatMessage()
        # 添加用户消息到聊天消息对象中
        chat_message.add_user_message(question, metadata=metadata)
        # 添加AI消息到聊天消息对象中
        chat_message.add_ai_message(answer, metadata=metadata)
        # 将聊天消息添加到memory中
        self.memory.add(app_id=app_id, chat_message=chat_message, session_id=session_id)
        # 更新历史记录
        self.update_history(app_id=app_id, session_id=session_id)

    # 格式化历史记录的方法，将历史记录转换为字符串格式
    def _format_history(self) -> str:
        """将历史记录格式化为字符串，用于提示（prompt）中

        :return: 格式化后的历史记录字符串
        :rtype: str
        """
        return "\n".join(self.history)

    # 格式化记忆的方法，将记忆列表转换为字符串格式
    def _format_memories(self, memories: list[dict]) -> str:
        """将记忆列表格式化为字符串，用于提示（prompt）中

        :param memories: 需要格式化的记忆列表
        :type memories: list[dict]
        :return: 格式化后的记忆字符串
        :rtype: str
        """
        return "\n".join([memory["text"] for memory in memories])

    # 生成提示（prompt）的方法
    def generate_prompt(self, input_query: str, contexts: list[str], **kwargs: dict[str, Any]) -> str:
        """
        根据给定的查询和上下文生成一个提示（prompt），准备好传递给语言模型

        :param input_query: 查询内容
        :type input_query: str
        :param contexts: 与查询相关的上下文文档列表
        :type contexts: list[str]
        :return: 生成的提示
        :rtype: str
        """
        # 将上下文文档列表转换为字符串
        context_string = " | ".join(contexts)
        # 获取网络搜索结果，如果没有则为空字符串
        web_search_result = kwargs.get("web_search_result", "")
        # 获取记忆数据，如果没有则为None
        memories = kwargs.get("memories", None)
        # 如果有网络搜索结果，将其附加到上下文中
        if web_search_result:
            context_string = self._append_search_and_context(context_string, web_search_result)

        # 检查配置中的提示是否包含历史记录
        prompt_contains_history = self.config._validate_prompt_history(self.config.prompt)
        # 如果提示包含历史记录，进行替换操作
        if prompt_contains_history:
            prompt = self.config.prompt.substitute(
                context=context_string, query=input_query, history=self._format_history() or "No history"
            )
        # 如果有历史记录但是提示中没有包含，检查是否是默认提示，如果是则替换模板
        elif self.history and not prompt_contains_history:
            if (
                not self.config._validate_prompt_history(self.config.prompt)
                and self.config.prompt.template == DEFAULT_PROMPT
            ):
                if memories:
                    # 如果有记忆数据，使用包含记忆的模板
                    prompt = DEFAULT_PROMPT_WITH_MEM0_MEMORY_TEMPLATE.substitute(
                        context=context_string,
                        query=input_query,
                        history=self._format_history(),
                        memories=self._format_memories(memories),
                    )
                else:
                    # 如果没有记忆数据，使用包含历史的模板
                    prompt = DEFAULT_PROMPT_WITH_HISTORY_TEMPLATE.substitute(
                        context=context_string, query=input_query, history=self._format_history()
                    )
            else:
                # 如果不能替换默认模板，警告用户历史记录将被忽略
                logger.warning(
                    "你的机器人包含历史记录，但提示中没有包括`$history`关键字。历史记录被忽略。"
                )
                prompt = self.config.prompt.substitute(context=context_string, query=input_query)
        # 如果没有历史记录，直接生成基本的提示
        else:
            prompt = self.config.prompt.substitute(context=context_string, query=input_query)
        # 返回生成的提示
        return prompt

    # 静态方法，用于将网络搜索结果附加到现有上下文中
    @staticmethod
    def _append_search_and_context(context: str, web_search_result: str) -> str:
        """将网络搜索结果附加到现有的上下文中

        :param context: 现有的上下文
        :type context: str
        :param web_search_result: 网络搜索结果
        :type web_search_result: str
        :return: 合并后的上下文和网络搜索结果字符串
        :rtype: str
        """
        return f"{context}\n网络搜索结果: {web_search_result}"

    # 从语言模型获取回答的方法
    def get_answer_from_llm(self, prompt: str):
        """
        根据给定的查询和上下文，通过传递给语言模型来获取答案

        :param prompt: 传递给语言模型的提示
        :type prompt: str
        :return: 从语言模型得到的答案
        :rtype: _type_
        """
        return self.get_llm_model_answer(prompt)

    # 静态方法，用于在网络上搜索信息
    @staticmethod
    def access_search_and_get_results(input_query: str):
        """
        在互联网上搜索额外的信息

        :param input_query: 搜索查询
        :type input_query: str
        :return: 搜索结果
        :rtype: 未知类型
        """
        try:
            # 导入搜索引擎工具
            from langchain.tools import DuckDuckGoSearchRun
        except ImportError:
            # 如果导入失败，提示需要安装额外的依赖包
            raise ImportError(
                "搜索功能需要额外的依赖包。请使用`pip install duckduckgo-search==6.1.5`安装。"
            ) from None
        # 创建搜索引擎运行实例
        search = DuckDuckGoSearchRun()
        # 打印日志信息，说明正在搜索什么
        logger.info(f"访问搜索引擎获取{input_query}的答案")
        # 运行搜索并返回结果
        return search.run(input_query)

    # 流式响应生成器方法
    @staticmethod
    def _stream_response(answer: Any, token_info: Optional[dict[str, Any]] = None) -> Generator[Any, Any, None]:
        """生成器，用于流式响应

        :param answer: 来自语言模型的回答片段
        :type answer: Any
        :yield: 来自语言模型的回答片段
        :rtype: Generator[Any, Any, None]
        """
        # 初始化流式回答字符串
        streamed_answer = ""
        # 遍历回答片段
        for chunk in answer:
            # 将片段追加到流式回答字符串中
            streamed_answer = streamed_answer + chunk
            # 产出回答片段
            yield chunk
        # 打印最终的回答和令牌信息（如果有的话）
        logger.info(f"回答: {streamed_answer}")
        if token_info:
            logger.info(f"令牌信息: {token_info}")

    # 查询方法，基于输入查询查询向量数据库
    def query(self, input_query: str, contexts: list[str], config: BaseLlmConfig = None, dry_run=False, memories=None):
        """
        根据给定的输入查询，查询向量数据库。
        获取与查询相关联的文档，然后将其作为上下文传递给语言模型以获取答案。

        :param input_query: 查询内容
        :type input_query: str
        :param contexts: 从数据库检索出的嵌入数据，用作上下文
        :type contexts: list[str]
        :param config: 作为配置选项使用的`BaseLlmConfig`实例。这用于单次方法调用。
        要持久地使用配置，请在应用程序初始化期间声明它。默认为None
        :type config: Optional[BaseLlmConfig], 可选参数
        :param dry_run: 干运行模式，除了将结果提示发送给语言模型外，其他都执行。
        目的是测试提示，而不是响应。默认为False
        :type dry_run: bool, 可选参数
        :return: 查询的答案或干运行的结果
        :rtype: str
        """
        try:
            # 如果提供了配置实例，保存当前配置并在方法执行后恢复
            if config:
                prev_config = self.config.serialize()
                self.config = config

            # 如果是文档站点实例，更新配置
            if self.is_docs_site_instance:
                self.config.prompt = DOCS_SITE_PROMPT_TEMPLATE
                self.config.number_documents = 5
            # 初始化字典k
            k = {}
            # 如果配置了在线搜索，获取网络搜索结果
            if self.config.online:
                k["web_search_result"] = self.access_search_and_get_results(input_query)
            # 添加记忆数据到字典k中
            k["memories"] = memories
            # 生成提示
            prompt = self.generate_prompt(input_query, contexts, **k)
            # 打印日志信息，显示生成的提示
            logger.info(f"提示: {prompt}")
            # 如果是干运行模式，直接返回提示
            if dry_run:
                return prompt

            # 如果配置了令牌使用，获取答案和令牌信息
            if self.config.token_usage:
                answer, token_info = self.get_answer_from_llm(prompt)
            else:
                answer = self.get_answer_from_llm(prompt)
            # 如果答案是字符串类型
            if isinstance(answer, str):
                # 打印日志信息，显示答案
                logger.info(f"回答: {answer}")
                # 如果配置了令牌使用，返回答案和令牌信息
                if self.config.token_usage:
                    return answer, token_info
                return answer
            # 如果答案不是字符串类型，处理流式响应
            else:
                if self.config.token_usage:
                    return self._stream_response(answer, token_info)
                return self._stream_response(answer)
        finally:
            # 如果提供了配置实例，恢复之前的配置
            if config:
                self.config: BaseLlmConfig = BaseLlmConfig.deserialize(prev_config)

    # 聊天方法，类似于query方法，但是维护整个对话的历史记录
    def chat(
        self, input_query: str, contexts: list[str], config: BaseLlmConfig = None, dry_run=False, session_id: str = None
    ):
        """
        根据给定的输入查询，查询向量数据库。
        获取与查询相关联的文档，然后将其作为上下文传递给语言模型以获取答案。

        维护对话的完整历史记录在内存中。

        :param input_query: 查询内容
        :type input_query: str
        :param contexts: 从数据库检索出的嵌入数据，用作上下文
        :type contexts: list[str]
        :param config: 作为配置选项使用的`BaseLlmConfig`实例。这用于单次方法调用。
        要持久地使用配置，请在应用程序初始化期间声明它。默认为None
        :type config: Optional[BaseLlmConfig], 可选参数
        :param dry_run: 干运行模式，除了将结果提示发送给语言模型外，其他都执行。
        目的是测试提示，而不是响应。默认为False
        :type dry_run: bool, 可选参数
        :param session_id: 对话的会话ID，默认为None
        :type session_id: str, 可选参数
        :return: 查询的答案或干运行的结果
        :rtype: str
        """
        try:
            # 如果提供了配置实例，保存当前配置并在方法执行后恢复
            if config:
                prev_config = self.config.serialize()
                self.config = config

            # 如果是文档站点实例，更新配置
            if self.is_docs_site_instance:
                self.config.prompt = DOCS_SITE_PROMPT_TEMPLATE
                self.config.number_documents = 5
            # 初始化字典k
            k = {}
            # 如果配置了在线搜索，获取网络搜索结果
            if self.config.online:
                k["web_search_result"] = self.access_search_and_get_results(input_query)

            # 生成提示
            prompt = self.generate_prompt(input_query, contexts, **k)
            # 打印日志信息，显示生成的提示
            logger.info(f"提示: {prompt}")

            # 如果是干运行模式，直接返回提示
            if dry_run:
                return prompt

            # 获取答案和令牌信息
            answer, token_info = self.get_answer_from_llm(prompt)
            # 如果答案是字符串类型
            if isinstance(answer, str):
                # 打印日志信息，显示答案
                logger.info(f"回答: {answer}")
                # 返回答案和令牌信息
                return answer, token_info
            # 如果答案不是字符串类型，处理流式响应
            else:
                # 返回流式响应生成器
                return self._stream_response(answer, token_info)
        finally:
            # 如果提供了配置实例，恢复之前的配置
            if config:
                self.config: BaseLlmConfig = BaseLlmConfig.deserialize(prev_config)

    # 静态方法，用于构造langchain消息列表
    @staticmethod
    def _get_messages(prompt: str, system_prompt: Optional[str] = None) -> list[LCBaseMessage]:
        """
        构建langchain消息列表

        :param prompt: 用户的提示
        :type prompt: str
        :param system_prompt: 系统的提示，默认为None
        :type system_prompt: Optional[str], 可选参数
        :return: 消息列表
        :rtype: list[LCBaseMessage]
        """
        # 导入langchain的消息类
        from langchain.schema import HumanMessage, SystemMessage

        # 初始化消息列表
        messages = []
        # 如果有系统提示，添加到消息列表中
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        # 添加用户的提示到消息列表中
        messages.append(HumanMessage(content=prompt))
        # 返回消息列表
        return messages

