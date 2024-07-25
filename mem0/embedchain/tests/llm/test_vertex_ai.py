# 导入需要的模拟工具
from unittest.mock import MagicMock, patch

# 导入测试框架
import pytest

# 导入一些聊天模型的消息类型
from langchain.schema import HumanMessage, SystemMessage

# 导入配置类
from embedchain.config import BaseLlmConfig

# 导入数据库管理器
from embedchain.core.db.database import database_manager

# 导入我们想要测试的类
from embedchain.llm.vertex_ai import VertexAILlm

# 定义一个测试用例，自动运行，用于设置数据库环境
@pytest.fixture(autouse=True)  # 这个装饰器表示这是一个特殊的测试用例，会在其他测试前自动运行
def setup_database():  # 这个函数用来设置数据库引擎
    database_manager.setup_engine()  # 设置数据库引擎

# 定义一个测试用例，用于创建 `VertexAILlm` 实例
@pytest.fixture  # 这个装饰器表示这是一个测试用例
def vertexai_llm():  # 创建一个 `VertexAILlm` 实例
    config = BaseLlmConfig(temperature=0.6, model="chat-bison")  # 创建配置对象
    return VertexAILlm(config)  # 返回实例

# 定义一个测试用例，测试获取答案的方法
def test_get_llm_model_answer(vertexai_llm):  # 测试 `get_llm_model_answer` 方法
    with patch.object(VertexAILlm, "_get_answer", return_value="Test Response"):  # 模拟 `_get_answer` 方法返回 "Test Response"
        prompt = "Test Prompt"  # 设置测试提示语
        response = vertexai_llm.get_llm_model_answer(prompt)  # 调用方法并获取响应
        assert response == "Test Response"  # 确认响应正确
        mock_method.assert_called_once_with(prompt, vertexai_llm.config)  # 确认 `_get_answer` 被调用了一次

# 定义一个测试用例，测试带有令牌计数功能的答案获取
def test_get_llm_model_answer_with_token_usage(vertexai_llm):  # 测试 `get_llm_model_answer` 方法，这次关注令牌计数
    test_config = BaseLlmConfig(  # 创建一个新的配置对象
        temperature=vertexai_llm.config.temperature,  # 设置温度
        max_tokens=vertexai_llm.config.max_tokens,  # 设置最大令牌数
        top_p=vertexai_llm.config.top_p,  # 设置 top_p
        model=vertexai_llm.config.model,  # 设置模型
        token_usage=True,  # 启用令牌计数
    )
    vertexai_llm.config = test_config  # 更新配置
    with patch.object(  # 模拟 `_get_answer` 方法返回值
        VertexAILlm,
        "_get_answer",
        return_value=("Test Response", {"prompt_token_count": 1, "candidates_token_count": 2}),
    ):
        response, token_info = vertexai_llm.get_llm_model_answer("Test Query")  # 获取响应和令牌信息
        assert response == "Test Response"  # 确认响应正确
        assert token_info == {  # 确认令牌信息正确
            "prompt_tokens": 1,
            "completion_tokens": 2,
            "total_tokens": 3,
            "total_cost": 3.75e-07,  # 总成本
            "cost_currency": "USD",  # 成本货币单位
        }

# 定义一个测试用例，测试获取答案的内部方法
@patch("embedchain.llm.vertex_ai.ChatVertexAI")  # 使用模拟对象替换 `ChatVertexAI`
def test_get_answer(mock_chat_vertexai, vertexai_llm, caplog):  # 测试 `_get_answer` 方法
    mock_chat_vertexai.return_value.invoke.return_value = MagicMock(content="Test Response")  # 设置模拟对象的返回值
    config = vertexai_llm.config  # 获取配置
    prompt = "Test Prompt"  # 设置测试提示语
    messages = vertexai_llm._get_messages(prompt)  # 获取消息列表
    response = vertexai_llm._get_answer(prompt, config)  # 获取答案
    mock_chat_vertexai.return_value.invoke.assert_called_once_with(messages)  # 确认 `invoke` 被调用了一次
    assert response == "Test Response"  # 确认响应正确
    assert "Config option `top_p` is not supported by this model." not in caplog.text  # 确认日志中没有特定警告信息

# 定义一个测试用例，测试构建消息的方法
def test_get_messages(vertexai_llm):  # 测试 `_get_messages` 方法
    prompt = "Test Prompt"  # 设置测试提示语
    system_prompt = "Test System Prompt"  # 设置系统提示语
    messages = vertexai_llm._get_messages(prompt, system_prompt)  # 获取消息列表
    assert messages == [  # 确认消息列表正确
        SystemMessage(content="Test System Prompt", additional_kwargs={}),  # 系统消息
        HumanMessage(content="Test Prompt", additional_kwargs={}, example=False),  # 人类消息
    ]

