# 导入一些必要的库和模块，这些库和模块帮助我们进行测试和使用特定的AI模型。
import os
from unittest.mock import patch

import pytest
from langchain.schema import HumanMessage, SystemMessage

from embedchain.config import BaseLlmConfig
from embedchain.llm.anthropic import AnthropicLlm

# 下面的代码块是为了准备一个AI模型的实例，这个模型是来自Anthropic的Claude模型。
@pytest.fixture
def anthropic_llm():
    # 设置环境变量，这里像是告诉电脑我们要用的API密钥是什么。
    os.environ["ANTHROPIC_API_KEY"] = "test_api_key"
    # 创建一个配置对象，设置模型的温度（随机性）和模型类型。
    config = BaseLlmConfig(temperature=0.5, model="claude-instant-1", token_usage=False)
    # 返回一个根据配置创建的AI模型实例。
    return AnthropicLlm(config)

# 这个函数用于测试AI模型的回答是否正确。
def test_get_llm_model_answer(anthropic_llm):
    # 使用“补丁”来假装AI模型的回答，这样我们就可以控制它返回什么。
    with patch.object(AnthropicLlm, "_get_answer", return_value="Test Response") as mock_method:
        # 定义一个测试用的提示语。
        prompt = "Test Prompt"
        # 调用模型获取回答，并检查回答是否是我们预设的那个。
        response = anthropic_llm.get_llm_model_answer(prompt)
        assert response == "Test Response"
        # 确保我们的“补丁”方法只被调用了一次。
        mock_method.assert_called_once_with(prompt, anthropic_llm.config)

# 这个函数测试AI模型如何处理系统提示和用户输入。
def test_get_messages(anthropic_llm):
    # 定义一个测试用的提示语和系统提示。
    prompt = "Test Prompt"
    system_prompt = "Test System Prompt"
    # 获取模型处理后的消息列表，并检查它们是否正确。
    messages = anthropic_llm._get_messages(prompt, system_prompt)
    assert messages == [
        SystemMessage(content="Test System Prompt", additional_kwargs={}),
        HumanMessage(content="Test Prompt", additional_kwargs={}, example=False),
    ]

# 这个函数测试AI模型在考虑令牌使用情况下的回答。
def test_get_llm_model_answer_with_token_usage(anthropic_llm):
    # 创建一个新的配置，这次要计算令牌使用情况。
    test_config = BaseLlmConfig(
        temperature=anthropic_llm.config.temperature, model=anthropic_llm.config.model, token_usage=True
    )
    # 更新AI模型的配置。
    anthropic_llm.config = test_config
    # 再次使用“补丁”，这次还假装返回令牌使用信息。
    with patch.object(
        AnthropicLlm, "_get_answer", return_value=("Test Response", {"input_tokens": 1, "output_tokens": 2})
    ) as mock_method:
        # 同样定义一个测试用的提示语。
        prompt = "Test Prompt"
        # 调用模型获取回答和令牌信息，并检查它们是否正确。
        response, token_info = anthropic_llm.get_llm_model_answer(prompt)
        assert response == "Test Response"
        # 检查令牌信息是否正确。
        assert token_info == {
            "prompt_tokens": 1,
            "completion_tokens": 2,
            "total_tokens": 3,
            "total_cost": 1.265e-05,
            "cost_currency": "USD",
        }
        # 确保“补丁”方法只被调用了一次。
        mock_method.assert_called_once_with(prompt, anthropic_llm.config)

