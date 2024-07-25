# 首先，我们导入了一个叫做pytest的工具，它帮助我们测试代码。
import pytest

# 然后从embedchain.config这个包里拿出了BaseLlmConfig这个类，
# 这个类是用来设置语言模型的一些参数的。
from embedchain.config import BaseLlmConfig

# 接下来，我们从embedchain.llm.google这个包里拿到了GoogleLlm这个类，
# 这个类是跟谷歌的语言模型交互的工具。
from embedchain.llm.google import GoogleLlm

# 下面我们定义了一个函数，它创建了一个GoogleLlm需要的配置对象。
# 这个配置告诉模型要用什么模型（这里是gemini-pro），最大生成多少词，
# 温度（控制随机性）、top_p（另一个控制随机性的参数）以及是否流式输出。
@pytest.fixture
def google_llm_config():
    return BaseLlmConfig(model="gemini-pro", max_tokens=100, temperature=0.7, top_p=0.5, stream=False)

# 这个测试函数检查如果没设置API密钥会发生什么。
# 我们用monkeypatch来假装删除了环境变量GOOGLE_API_KEY，
# 然后尝试创建GoogleLlm实例，期望它会抛出一个错误，告诉我们缺少API密钥。
def test_google_llm_init_missing_api_key(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    with pytest.raises(ValueError, match="Please set the GOOGLE_API_KEY environment variable."):
        GoogleLlm()

# 这个测试函数检查当有API密钥时，GoogleLlm实例能否正常创建。
# 我们设置了一个假的API密钥，然后创建GoogleLlm实例，确保它不是None。
def test_google_llm_init(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "fake_api_key")
    with monkeypatch.context() as m:
        m.setattr("importlib.import_module", lambda x: None)
        google_llm = GoogleLlm()
    assert google_llm is not None

# 这个测试函数检查如果在初始化GoogleLlm时传入系统提示（system_prompt）会发生什么。
# 我们设置了一个假的API密钥，创建GoogleLlm实例并传入system_prompt，
# 但因为GoogleLlm不支持这个参数，所以它应该抛出一个错误。
def test_google_llm_get_llm_model_answer_with_system_prompt(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "fake_api_key")
    monkeypatch.setattr("importlib.import_module", lambda x: None)
    google_llm = GoogleLlm(config=BaseLlmConfig(system_prompt="system prompt"))
    with pytest.raises(ValueError, match="GoogleLlm does not support `system_prompt`"):
        google_llm.get_llm_model_answer("test prompt")

# 最后，这个测试函数检查GoogleLlm能否正确地从模型获取答案。
# 我们再次设置了假的API密钥，还做了一些模拟，让`_get_answer`方法直接返回“Generated Text”。
# 然后我们创建了GoogleLlm实例，调用它的`get_llm_model_answer`方法，
# 并检查返回的结果是否是我们模拟的那个答案。
def test_google_llm_get_llm_model_answer(monkeypatch, google_llm_config):
    def mock_get_answer(prompt, config):
        return "Generated Text"

    monkeypatch.setenv("GOOGLE_API_KEY", "fake_api_key")
    monkeypatch.setattr(GoogleLlm, "_get_answer", mock_get_answer)
    google_llm = GoogleLlm(config=google_llm_config)
    result = google_llm.get_llm_model_answer("test prompt")

    assert result == "Generated Text"

