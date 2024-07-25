# 导入一些库和模块，比如操作环境变量的库、发送HTTP请求的库、用来做单元测试的库等。
import os
import httpx
import pytest
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# 导入我们自己定义的一些配置类和具体的OpenAI模型实现。
from embedchain.config import BaseLlmConfig
from embedchain.llm.openai import OpenAILlm

# 定义一个测试用的fixture（可以看作是准备阶段），设置环境变量中的OpenAI API密钥和基础URL。
@pytest.fixture()
def env_config():
    # 设置环境变量，用于存放API密钥和基础URL。
    os.environ["OPENAI_API_KEY"] = "test_api_key"
    os.environ["OPENAI_API_BASE"] = "https://api.openai.com/v1/engines/"
    
    # 使用yield关键字表示这是一个fixture，在执行测试之前会先运行到这里。
    yield
    
    # 清理环境变量，避免影响其他测试。
    os.environ.pop("OPENAI_API_KEY")

# 另一个fixture，创建一个基本的配置对象，用于测试。
@pytest.fixture
def config(env_config):
    # 创建一个配置实例，包含温度（控制生成文本的随机性）、最大令牌数等参数。
    config = BaseLlmConfig(
        temperature=0.7,
        max_tokens=50,
        top_p=0.8,
        stream=False,
        system_prompt="System prompt",
        model="gpt-3.5-turbo",
        http_client_proxies=None,
        http_async_client_proxies=None,
    )
    
    # 使用yield关键字表示这是一个fixture，在执行测试之前会先运行到这里。
    yield config

# 定义一个测试函数，模拟获取模型回答的情况。
def test_get_llm_model_answer(config, mocker):
    # 使用mocker模拟OpenAILlm类中的_get_answer方法，让它直接返回"Test answer"。
    mocked_get_answer = mocker.patch("embedchain.llm.openai.OpenAILlm._get_answer", return_value="Test answer")
    
    # 创建一个OpenAILlm实例，并传入配置。
    llm = OpenAILlm(config)
    
    # 调用方法获取答案，并检查是否等于预期的"Test answer"。
    answer = llm.get_llm_model_answer("Test query")
    
    # 断言检查，确保答案正确。
    assert answer == "Test answer"
    
    # 检查模拟的方法是否被调用过一次。
    mocked_get_answer.assert_called_once_with("Test query", config)

# 类似的测试函数，这次是测试自定义系统提示的情况。
def test_get_llm_model_answer_with_system_prompt(config, mocker):
    # 更改配置中的系统提示。
    config.system_prompt = "Custom system prompt"
    
    # 使用mocker模拟OpenAILlm类中的_get_answer方法。
    mocked_get_answer = mocker.patch("embedchain.llm.openai.OpenAILlm._get_answer", return_value="Test answer")
    
    # 创建一个OpenAILlm实例，并传入配置。
    llm = OpenAILlm(config)
    
    # 调用方法获取答案，并检查是否等于预期的"Test answer"。
    answer = llm.get_llm_model_answer("Test query")
    
    # 断言检查，确保答案正确。
    assert answer == "Test answer"
    
    # 检查模拟的方法是否被调用过一次。
    mocked_get_answer.assert_called_once_with("Test query", config)

# 测试当输入为空字符串时的情况。
def test_get_llm_model_answer_empty_prompt(config, mocker):
    # 使用mocker模拟OpenAILlm类中的_get_answer方法。
    mocked_get_answer = mocker.patch("embedchain.llm.openai.OpenAILlm._get_answer", return_value="Test answer")
    
    # 创建一个OpenAILlm实例，并传入配置。
    llm = OpenAILlm(config)
    
    # 调用方法获取答案，并检查是否等于预期的"Test answer"。
    answer = llm.get_llm_model_answer("")
    
    # 断言检查，确保答案正确。
    assert answer == "Test answer"
    
    # 检查模拟的方法是否被调用过一次。
    mocked_get_answer.assert_called_once_with("", config)

# 测试带有令牌计数功能的情况。
def test_get_llm_model_answer_with_token_usage(config, mocker):
    # 创建一个新的配置实例，开启令牌计数功能。
    test_config = BaseLlmConfig(
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        top_p=config.top_p,
        stream=config.stream,
        system_prompt=config.system_prompt,
        model=config.model,
        token_usage=True,
    )
    
    # 使用mocker模拟OpenAILlm类中的_get_answer方法，返回答案以及令牌信息。
    mocked_get_answer = mocker.patch(
        "embedchain.llm.openai.OpenAILlm._get_answer",
        return_value=("Test answer", {"prompt_tokens": 1, "completion_tokens": 2}),
    )
    
    # 创建一个OpenAILlm实例，并传入新的配置。
    llm = OpenAILlm(test_config)
    
    # 调用方法获取答案和令牌信息。
    answer, token_info = llm.get_llm_model_answer("Test query")
    
    # 断言检查，确保答案正确。
    assert answer == "Test answer"
    
    # 确认令牌信息是否正确。
    assert token_info == {
        "prompt_tokens": 1,
        "completion_tokens": 2,
        "total_tokens": 3,
        "total_cost": 5.5e-06,
        "cost_currency": "USD",
    }
    
    # 检查模拟的方法是否被调用过一次。
    mocked_get_answer.assert_called_once_with("Test query", test_config)

# 测试带有流式输出功能的情况。
def test_get_llm_model_answer_with_streaming(config, mocker):
    # 在配置中启用流式输出。
    config.stream = True
    
    # 使用mocker模拟ChatOpenAI类。
    mocked_openai_chat = mocker.patch("embedchain.llm.openai.ChatOpenAI")
    
    # 创建一个OpenAILlm实例，并传入配置。
    llm = OpenAILlm(config)
    
    # 调用方法获取答案。
    llm.get_llm_model_answer("Test query")
    
    # 检查ChatOpenAI是否被正确调用。
    mocked_openai_chat.assert_called_once()
    
    # 检查回调函数中是否包含了StreamingStdOutCallbackHandler。
    callbacks = [callback[1]["callbacks"] for callback in mocked_openai_chat.call_args_list]
    assert any(isinstance(callback[0], StreamingStdOutCallbackHandler) for callback in callbacks)

# 最后一个测试函数，测试没有系统提示的情况。
def test_get_llm_model_answer_without_system_prompt(config, mocker):
    # 将配置中的系统提示设为None。
    config.system_prompt = None
    
    # 使用mocker模拟ChatOpenAI类。
    mocked_openai_chat = mocker.patch("embedchain.llm.openai.ChatOpenAI")
    
    # 创建一个OpenAILlm实例，并传入配置。
    llm = OpenAILlm(config)
    
    # 调用方法获取答案。
    llm.get_llm_model_answer("Test query")
    
    # 检查ChatOpenAI是否被正确调用，并传入了正确的参数。
    mocked_openai_chat.assert_called_once_with(
        model=config.model,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        model_kwargs={"top_p": config.top_p},
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ["OPENAI_API_BASE"],
        http_client=None,
        http_async_client=None,
    )

# 这个测试函数检查当有特殊头部信息时，函数的行为。
def test_get_llm_model_answer_with_special_headers(config, mocker):
    # 首先，设置一些测试用的头部信息（就像信封上的地址标签）。
    config.default_headers = {"test": "test"}

    # 接下来，我们假装`ChatOpenAI`这个类已经被调用过，这样我们就能控制它的行为。
    mocked_openai_chat = mocker.patch("embedchain.llm.openai.ChatOpenAI")

    # 创建一个`OpenAILlm`实例，传入配置信息。
    llm = OpenAILlm(config)

    # 调用`get_llm_model_answer`函数，传入一个测试查询。
    llm.get_llm_model_answer("Test query")

    # 然后，我们检查`ChatOpenAI`是否被正确地调用了一次，确保所有的参数都符合预期。
    mocked_openai_chat.assert_called_once_with(
        model=config.model,  # 使用配置里的模型类型
        temperature=config.temperature,  # 使用配置里的温度值
        max_tokens=config.max_tokens,  # 使用配置里的最大令牌数
        model_kwargs={"top_p": config.top_p},  # 设置额外的模型参数
        api_key=os.environ["OPENAI_API_KEY"],  # 获取环境变量中的API密钥
        base_url=os.environ["OPENAI_API_BASE"],  # 获取环境变量中的API基础URL
        default_headers={"test": "test"},  # 使用之前设置的头部信息
        http_client=None,  # 不使用自定义的HTTP客户端
        http_async_client=None,  # 不使用自定义的异步HTTP客户端
    )

# 定义一个函数叫做 test_get_llm_model_answer_with_http_async_client_proxies，
# 这个函数接受两个参数：env_config 和 mocker。
def test_get_llm_model_answer_with_http_async_client_proxies(env_config, mocker):

