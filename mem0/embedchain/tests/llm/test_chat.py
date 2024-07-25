# 导入操作系统相关的功能，这里可能用到的是获取或设置环境变量等功能。
import os
# 导入 Python 自带的单元测试框架，用来编写和运行测试用例。
import unittest
# 导入模拟对象的功能，可以在测试时模拟某些函数或类的行为。
from unittest.mock import MagicMock, patch
# 从 embedchain 包里导入 App 类，这是我们要测试的主要应用。
from embedchain import App
# 从 embedchain.config 模块中导入 AppConfig 和 BaseLlmConfig 这两个配置类，它们定义了应用的配置信息。
from embedchain.config import AppConfig, BaseLlmConfig
# 从 embedchain.llm.base 模块中导入 BaseLlm 类，这是一个基础的语言模型接口。
from embedchain.llm.base import BaseLlm
# 从 embedchain.memory.base 模块中导入 ChatHistory 类，它用于记录聊天历史。
from embedchain.memory.base import ChatHistory
# 从 embedchain.memory.message 模块中导入 ChatMessage 类，它代表了一条具体的聊天消息。
from embedchain.memory.message import ChatMessage

# 定义了一个测试类，继承自 unittest.TestCase
class TestApp(unittest.TestCase):
    # setUp 方法会在每个测试方法之前被调用，用于设置测试前的准备工作
    def setUp(self):
        # 设置环境变量 OPENAI_API_KEY 为 "test_key"
        os.environ["OPENAI_API_KEY"] = "test_key"
        # 创建一个 App 实例，传入配置参数 collect_metrics 为 False
        self.app = App(config=AppConfig(collect_metrics=False))

    # 使用装饰器 patch.object 来模拟 App 类中的 _retrieve_from_database 方法
    # 和 BaseLlm 类中的 get_answer_from_llm 方法
    @patch.object(App, "_retrieve_from_database", return_value=["Test context"])
    @patch.object(BaseLlm, "get_answer_from_llm", return_value="Test answer")
    # 测试 chat_with_memory 方法
    def test_chat_with_memory(self, mock_get_answer, mock_retrieve):
        # 写一段说明文字，描述这个测试做了什么
        """
        这个测试主要检查 App 类中的 'chat' 方法是否能正确地处理聊天历史记录。
        我们会调用两次 'chat' 方法。第一次调用会初始化聊天历史记录。
        第二次调用时会使用第一次调用产生的聊天历史记录。

        主要测试点：
            确保方法被正确调用，并且添加了正确的聊天历史记录。
        - 第一次调用后，会添加用户消息和 AI 回答到历史记录中。
        - 第二次调用时，'chat' 方法会使用第一次调用的历史记录。
        """
        # 创建一个新的 AppConfig 对象，设置 collect_metrics 为 False
        config = AppConfig(collect_metrics=False)
        # 创建一个新的 App 实例
        app = App(config=config)
        # 使用装饰器 patch.object 来模拟 BaseLlm 类中的 add_history 方法
        with patch.object(BaseLlm, "add_history") as mock_history:
            # 第一次调用 'chat' 方法
            first_answer = app.chat("Test query 1")
            # 检查第一次的回答是否是 "Test answer"
            self.assertEqual(first_answer, "Test answer")
            # 检查 add_history 方法是否被正确调用
            mock_history.assert_called_with(app.config.id, "Test query 1", "Test answer", session_id="default")

            # 第二次调用 'chat' 方法
            second_answer = app.chat("Test query 2", session_id="test_session")
            # 检查第二次的回答是否也是 "Test answer"
            self.assertEqual(second_answer, "Test answer")
            # 再次检查 add_history 方法是否被正确调用
            mock_history.assert_called_with(app.config.id, "Test query 2", "Test answer", session_id="test_session")

    # 使用装饰器 patch.object 来模拟 App 类中的 _retrieve_from_database 方法
    # 和 BaseLlm 类中的 get_answer_from_llm 方法
    @patch.object(App, "_retrieve_from_database", return_value=["Test context"])
    @patch.object(BaseLlm, "get_answer_from_llm", return_value="Test answer")
    # 测试 template_replacement 方法
    def test_template_replacement(self, mock_get_answer, mock_retrieve):
        # 写一段说明文字，描述这个测试做了什么
        """
        这个测试确保如果使用默认模板并且模板中没有历史记录，
        那么会替换使用默认模板。

        同时测试 dry_run 不会改变历史记录。
        """
        # 使用装饰器 patch.object 来模拟 ChatHistory 类中的 get 方法
        with patch.object(ChatHistory, "get") as mock_memory:
            # 创建一个假的消息对象
            mock_message = ChatMessage()
            # 添加一条用户消息
            mock_message.add_user_message("Test query 1")
            # 添加一条 AI 的回答
            mock_message.add_ai_message("Test answer")
            # 让模拟的 get 方法返回这个消息对象
            mock_memory.return_value = [mock_message]

            # 创建一个新的 AppConfig 对象
            config = AppConfig(collect_metrics=False)
            # 创建一个新的 App 实例
            app = App(config=config)
            # 第一次调用 'chat' 方法
            first_answer = app.chat("Test query 1")
            # 检查第一次的回答是否是 "Test answer"
            self.assertEqual(first_answer, "Test answer")
            # 检查历史记录长度为 1
            self.assertEqual(len(app.llm.history), 1)
            # 获取当前的历史记录
            history = app.llm.history
            # 调用 'chat' 方法进行 dry_run
            dry_run = app.chat("Test query 2", dry_run=True)
            # 检查 dry_run 返回的结果包含 "Conversation history:"
            self.assertIn("Conversation history:", dry_run)
            # 确认历史记录没有变化
            self.assertEqual(history, app.llm.history)
            # 再次确认历史记录长度为 1
            self.assertEqual(len(app.llm.history), 1)

    # 使用装饰器 patch 来模拟 Collection 类中的 add 方法
    @patch("chromadb.api.models.Collection.Collection.add", MagicMock)
    # 测试 chat_with_where_in_params 方法
    def test_chat_with_where_in_params(self):
        # 写一段说明文字，描述这个测试做了什么
        """
        这个测试主要检查 'chat' 方法中 where 过滤器的功能。
        """
        # 使用装饰器 patch.object 来模拟 App 类中的 _retrieve_from_database 方法
        with patch.object(self.app, "_retrieve_from_database") as mock_retrieve:
            # 设置模拟方法的返回值
            mock_retrieve.return_value = ["Test context"]
            # 使用装饰器 patch.object 来模拟 App 实例中的 llm 属性的 get_llm_model_answer 方法
            with patch.object(self.app.llm, "get_llm_model_answer") as mock_answer:
                # 设置模拟方法的返回值
                mock_answer.return_value = "Test answer"
                # 调用 'chat' 方法并传递 where 参数
                answer = self.app.chat("Test query", where={"attribute": "value"})

        # 检查返回的答案是否是 "Test answer"
        self.assertEqual(answer, "Test answer")
        # 获取模拟方法的调用参数
        _args, kwargs = mock_retrieve.call_args
        # 检查调用参数 input_query 是否为 "Test query"
        self.assertEqual(kwargs.get("input_query"), "Test query")
        # 检查调用参数 where 是否为 {"attribute": "value"}
        self.assertEqual(kwargs.get("where"), {"attribute": "value"})
        # 检查 get_llm_model_answer 方法是否被调用了一次
        mock_answer.assert_called_once()

    # 使用装饰器 patch 来模拟 Collection 类中的 add 方法
    @patch("chromadb.api.models.Collection.Collection.add", MagicMock)
    # 测试 chat_with_where_in_chat_config 方法
    def test_chat_with_where_in_chat_config(self):
        # 写一段说明文字，描述这个测试做了什么
        """
        这个测试主要检查 'chat' 方法在 App 类中的功能。
        它模拟了一个场景，其中 _retrieve_from_database 方法根据 where 过滤器返回上下文列表，
        并且 get_llm_model_answer 返回预期的答案字符串。

        'chat' 方法应该调用 '_retrieve_from_database' 方法，并传入 where 过滤器指定的内容，
        以及正确调用 'get_llm_model_answer' 方法，并返回正确的答案。

        主要测试点：
        - '_retrieve_from_database' 方法只被调用了一次，并且传入参数 "Test query" 和 BaseLlmConfig 的实例。
        - 'get_llm_model_answer' 方法只被调用了一次，具体参数不在本测试中检查。
        - 'chat' 方法返回的内容与 'get_llm_model_answer' 返回的内容一致。

        通过模拟 '_retrieve_from_database' 和 'get_llm_model_answer' 方法来隔离 'chat' 方法的行为。
        """
        # 使用装饰器 patch.object 来模拟 App 实例中的 llm 属性的 get_llm_model_answer 方法
        with patch.object(self.app.llm, "get_llm_model_answer") as mock_answer:
            # 设置模拟方法的返回值
            mock_answer.return_value = "Test answer"
            # 使用装饰器 patch.object 来模拟 App 实例的 db 属性的 query 方法
            with patch.object(self.app.db, "query") as mock_database_query:
                # 设置模拟方法的返回值
                mock_database_query.return_value = ["Test context"]
                # 创建一个 BaseLlmConfig 对象，并设置 where 参数
                llm_config = BaseLlmConfig(where={"attribute": "value"})
                # 调用 'chat' 方法
                answer = self.app.chat("Test query", llm_config)

        # 检查返回的答案是否是 "Test answer"
        self.assertEqual(answer, "Test answer")
        # 获取模拟方法的调用参数
        _args, kwargs = mock_database_query.call_args
        # 检查调用参数 input_query 是否为 "Test query"
        self.assertEqual(kwargs.get("input_query"), "Test query")
        # 检查调用参数 where 中包含 "app_id" 和 "attribute"
        where = kwargs.get("where")
        assert "app_id" in where
        assert "attribute" in where
        # 检查 get_llm_model_answer 方法是否被调用了一次
        mock_answer.assert_called_once()

