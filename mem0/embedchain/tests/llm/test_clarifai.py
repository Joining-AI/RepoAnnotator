# 导入pytest库，这是一个用来编写测试代码的库。
import pytest

# 从embedchain.config模块导入BaseLlmConfig类，这个类是用来配置语言模型的。
from embedchain.config import BaseLlmConfig

# 从embedchain.llm.clarifai模块导入ClarifaiLlm类，这是Clarifai语言模型的一个封装。
from embedchain.llm.clarifai import ClarifaiLlm

# 定义一个特殊的函数叫做“fixture”，它会在测试函数运行前被调用，用来准备一些测试需要用到的数据。
@pytest.fixture
def clarifai_llm_config(monkeypatch):
    # 使用monkeypatch工具来设置环境变量"CLARIFAI_PAT"为"test_api_key"。这就像假装我们有一个API密钥一样。
    monkeypatch.setenv("CLARIFAI_PAT","test_api_key")
    
    # 创建一个BaseLlmConfig实例，配置语言模型的一些参数，比如模型的URL和温度等。
    config = BaseLlmConfig(
        model="https://clarifai.com/openai/chat-completion/models/GPT-4",
        model_kwargs={"temperature": 0.7, "max_tokens": 100},
    )
    
    # 把配置好的config对象返回给测试函数使用。
    yield config
    
    # 测试结束后，清理环境变量"CLARIFAI_PAT"，确保不影响其他测试或程序部分。
    monkeypatch.delenv("CLARIFAI_PAT")

# 定义一个测试函数，用来测试ClarifaiLlm类的get_llm_model_answer方法是否能正确返回答案。
def test_clarifai__llm_get_llm_model_answer(clarifai_llm_config, mocker):
    # 使用mocker工具来模拟ClarifaiLlm类中的_get_answer方法，让它直接返回"Test answer"，而不是真的去获取答案。
    mocker.patch("embedchain.llm.clarifai.ClarifaiLlm._get_answer", return_value="Test answer")
    
    # 创建一个ClarifaiLlm实例，并传入之前准备好的配置信息。
    llm = ClarifaiLlm(clarifai_llm_config)
    
    # 调用get_llm_model_answer方法，并传入一个测试查询字符串"Test query"。
    answer = llm.get_llm_model_answer("Test query")
    
    # 检查返回的答案是否是我们模拟的那个"Test answer"，如果是，则测试通过。
    assert answer == "Test answer"

