# 导入pytest库，这是一个用于编写测试的库。
import pytest

# 从embedchain.config模块导入BaseLlmConfig类，这个类是用来配置语言模型的一些参数的。
from embedchain.config import BaseLlmConfig
# 从embedchain.llm.ollama模块导入OllamaLlm类，这是一个具体的语言模型实现。
from embedchain.llm.ollama import OllamaLlm
# 从langchain.callbacks.streaming_stdout模块导入StreamingStdOutCallbackHandler类，这是一个处理流式输出的回调处理器。
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# 定义一个pytest的fixture（固定装置），名字叫`ollama_llm_config`。它创建了一个BaseLlmConfig实例，并设置了一些参数，比如模型名、温度值等。
@pytest.fixture
def ollama_llm_config():
    # 创建BaseLlmConfig实例，并给它一些参数。
    config = BaseLlmConfig(model="llama2", temperature=0.7, top_p=0.8, stream=True, system_prompt=None)
    # 使用yield关键字告诉pytest这是一个fixture，并把配置对象传出去。
    yield config

# 这个函数用来测试获取语言模型答案的功能。它使用了mock（模拟）技术来假装某些功能，这样就可以在不需要真实环境的情况下进行测试。
def test_get_llm_model_answer(ollama_llm_config, mocker):
    # 模拟OllamaLlm中的Client.list方法，让它返回一个包含模型名称的字典。
    mocker.patch("embedchain.llm.ollama.Client.list", return_value={"models": [{"name": "llama2"}]})
    # 模拟OllamaLlm中的_get_answer方法，让它返回一个测试答案。
    mocker.patch("embedchain.llm.ollama.OllamaLlm._get_answer", return_value="Test answer")
    
    # 创建一个OllamaLlm实例，并传入前面定义好的配置。
    llm = OllamaLlm(ollama_llm_config)
    # 调用get_llm_model_answer方法，传入一个测试问题，获取答案。
    answer = llm.get_llm_model_answer("Test query")
    
    # 断言（检查）得到的答案是否是预期的“Test answer”。
    assert answer == "Test answer"

# 这个函数也是用来测试获取语言模型答案的功能，但是这次是通过模拟Ollama类的方法。
def test_get_answer_mocked_ollama(ollama_llm_config, mocker):
    # 模拟OllamaLlm中的Client.list方法，让它返回一个包含模型名称的字典。
    mocker.patch("embedchain.llm.ollama.Client.list", return_value={"models": [{"name": "llama2"}]})
    # 模拟Ollama类，让它在被调用时返回一个模拟的对象。
    mocked_ollama = mocker.patch("embedchain.llm.ollama.Ollama")
    # 获取模拟对象的一个实例。
    mock_instance = mocked_ollama.return_value
    # 设置模拟对象的invoke方法返回一个模拟答案。
    mock_instance.invoke.return_value = "Mocked answer"
    
    # 创建一个OllamaLlm实例，并传入前面定义好的配置。
    llm = OllamaLlm(ollama_llm_config)
    # 定义一个测试问题。
    prompt = "Test query"
    # 调用get_llm_model_answer方法，传入测试问题，获取答案。
    answer = llm.get_llm_model_answer(prompt)
    
    # 断言（检查）得到的答案是否是预期的“Mocked answer”。
    assert answer == "Mocked answer"

# 这个函数测试带有流式输出的语言模型答案获取功能。
def test_get_llm_model_answer_with_streaming(ollama_llm_config, mocker):
    # 把配置中的stream属性设为True，表示要启用流式输出。
    ollama_llm_config.stream = True
    # 设置配置中的callbacks属性为一个包含StreamingStdOutCallbackHandler实例的列表，这表示我们要用到流式输出的回调处理器。
    ollama_llm_config.callbacks = [StreamingStdOutCallbackHandler()]
    # 模拟OllamaLlm中的Client.list方法，让它返回一个包含模型名称的字典。
    mocker.patch("embedchain.llm.ollama.Client.list", return_value={"models": [{"name": "llama2"}]})
    # 模拟OllamaLlm中的_get_answer方法，让它返回一个测试答案。
    mocked_ollama_chat = mocker.patch("embedchain.llm.ollama.OllamaLlm._get_answer", return_value="Test answer")
    
    # 创建一个OllamaLlm实例，并传入前面定义好的配置。
    llm = OllamaLlm(ollama_llm_config)
    # 调用get_llm_model_answer方法，传入一个测试问题。
    llm.get_llm_model_answer("Test query")
    
    # 检查模拟的_get_answer方法是否只被调用了一次。
    mocked_ollama_chat.assert_called_once()
    # 获取模拟方法被调用时的参数。
    call_args = mocked_ollama_chat.call_args
    # 从参数中提取出配置对象。
    config_arg = call_args[1]["config"]
    # 从配置对象中提取出回调处理器列表。
    callbacks = config_arg.callbacks
    
    # 断言（检查）回调处理器列表长度是否为1。
    assert len(callbacks) == 1
    # 断言（检查）列表中的第一个元素是否是StreamingStdOutCallbackHandler类型的实例。
    assert isinstance(callbacks[0], StreamingStdOutCallbackHandler)

