# 导入需要的库和模块
import os
# 导入pytest库，用于编写测试用例
import pytest
# 从embedchain.config导入BaseLlmConfig类，这是配置大语言模型的基本设置
from embedchain.config import BaseLlmConfig
# 从embedchain.llm.together导入TogetherLlm类，这是我们想要测试的大语言模型接口
from embedchain.llm.together import TogetherLlm

# 定义一个函数，用来创建测试时需要的配置对象
@pytest.fixture
def together_llm_config():
    # 设置环境变量，给大语言模型提供API密钥
    os.environ["TOGETHER_API_KEY"] = "test_api_key"
    # 创建一个BaseLlmConfig实例，指定一些模型参数
    config = BaseLlmConfig(model="together-ai-up-to-3b", max_tokens=50, temperature=0.7, top_p=0.8)
    # 使用yield关键字返回配置对象，测试结束后会自动清理环境变量
    yield config
    # 清除环境变量中的API密钥，保证测试环境的干净
    os.environ.pop("TOGETHER_API_KEY")

# 测试函数，验证如果没有提供API密钥是否会抛出错误
def test_init_raises_value_error_without_api_key(mocker):
    # 使用mocker清除所有环境变量
    mocker.patch.dict(os.environ, clear=True)
    # 使用pytest.raises来捕获期望的ValueError异常
    with pytest.raises(ValueError):
        # 尝试初始化TogetherLlm实例，没有API密钥应该抛出错误
        TogetherLlm()

# 测试函数，验证如果设置了系统提示(system_prompt)是否会抛出错误
def test_get_llm_model_answer_raises_value_error_for_system_prompt(together_llm_config):
    # 创建一个TogetherLlm实例，并使用上面定义的配置
    llm = TogetherLlm(together_llm_config)
    # 设置llm的系统提示，这在实际使用中不应该被设置
    llm.config.system_prompt = "system_prompt"
    # 检查当有系统提示时调用get_llm_model_answer方法是否会抛出错误
    with pytest.raises(ValueError):
        llm.get_llm_model_answer("prompt")

# 测试函数，验证get_llm_model_answer方法能否正确返回答案
def test_get_llm_model_answer(together_llm_config, mocker):
    # 使用mocker模拟TogetherLlm类中的_get_answer方法，让它直接返回预设的答案
    mocker.patch("embedchain.llm.together.TogetherLlm._get_answer", return_value="Test answer")
    # 创建一个TogetherLlm实例，并使用上面定义的配置
    llm = TogetherLlm(together_llm_config)
    # 调用get_llm_model_answer方法并传入测试查询
    answer = llm.get_llm_model_answer("Test query")
    # 检查返回的答案是否与预设的答案相同
    assert answer == "Test answer"

# 测试函数，验证get_llm_model_answer方法能否正确返回答案以及token使用信息
def test_get_llm_model_answer_with_token_usage(together_llm_config, mocker):
    # 创建一个新的BaseLlmConfig实例，并设置一些参数
    test_config = BaseLlmConfig(
        temperature=together_llm_config.temperature,
        max_tokens=together_llm_config.max_tokens,
        top_p=together_llm_config.top_p,
        model=together_llm_config.model,
        token_usage=True,
    )
    # 使用mocker模拟TogetherLlm类中的_get_answer方法，让它返回预设的答案和token使用情况
    mocker.patch(
        "embedchain.llm.together.TogetherLlm._get_answer",
        return_value=("Test answer", {"prompt_tokens": 1, "completion_tokens": 2}),
    )
    # 创建一个TogetherLlm实例，并使用上面定义的新配置
    llm = TogetherLlm(test_config)
    # 调用get_llm_model_answer方法并传入测试查询，同时获取答案和token使用信息
    answer, token_info = llm.get_llm_model_answer("Test query")
    # 检查返回的答案是否与预设的答案相同
    assert answer == "Test answer"
    # 检查返回的token使用信息是否与预设的信息一致
    assert token_info == {
        "prompt_tokens": 1,
        "completion_tokens": 2,
        "total_tokens": 3,
        "total_cost": 3e-07,
        "cost_currency": "USD",
    }

# 测试函数，验证get_llm_model_answer方法能否正确返回答案（这里使用mock来模拟实际情况）
def test_get_answer_mocked_together(together_llm_config, mocker):
    # 使用mocker模拟ChatTogether类，这个类是用来与大语言模型交互的
    mocked_together = mocker.patch("embedchain.llm.together.ChatTogether")
    # 获取模拟类的实例，并设置调用invoke方法后的返回值
    mock_instance = mocked_together.return_value
    mock_instance.invoke.return_value.content = "Mocked answer"
    # 创建一个TogetherLlm实例，并使用上面定义的配置
    llm = TogetherLlm(together_llm_config)
    # 调用get_llm_model_answer方法并传入测试查询
    prompt = "Test query"
    answer = llm.get_llm_model_answer(prompt)
    # 检查返回的答案是否与预设的答案相同
    assert answer == "Mocked answer"

