# 从string模块导入Template类，这个类用于处理字符串模板。
from string import Template

# 导入pytest库，这是一个用于编写测试的库。
import pytest

# 从embedchain的llm模块导入BaseLlm和BaseLlmConfig类，这些是我们要测试的类。
from embedchain.llm.base import BaseLlm, BaseLlmConfig

# 使用装饰器`@pytest.fixture`定义了一个测试用例，这个测试用例会创建一个BaseLlm实例。
@pytest.fixture
def base_llm():
    # 创建一个BaseLlmConfig配置实例。
    config = BaseLlmConfig()
    # 返回一个使用上面配置实例创建的BaseLlm对象。
    return BaseLlm(config=config)

# 定义一个测试函数，检查`get_llm_model_answer`方法是否实现了。
def test_is_get_llm_model_answer_not_implemented(base_llm):
    # 使用pytest的raises函数检查调用`get_llm_model_answer`方法是否会抛出NotImplementedError异常。
    with pytest.raises(NotImplementedError):
        base_llm.get_llm_model_answer()

# 定义一个测试函数，检查配置中的`stream`参数是否只能是布尔值。
def test_is_stream_bool():
    # 使用pytest的raises函数检查如果`stream`参数不是布尔值（这里用了字符串"test value"），是否会抛出ValueError异常。
    with pytest.raises(ValueError):
        config = BaseLlmConfig(stream="test value")
        BaseLlm(config=config)

# 定义一个测试函数，检查字符串模板是否能正确转换成Template实例。
def test_template_string_gets_converted_to_Template_instance():
    # 创建一个包含字符串模板的BaseLlmConfig配置实例。
    config = BaseLlmConfig(template="test value $query $context")
    # 使用配置实例创建BaseLlm对象。
    llm = BaseLlm(config=config)
    # 检查BaseLlm对象的prompt属性是否是Template类型的实例。
    assert isinstance(llm.config.prompt, Template)

# 定义一个测试函数，检查`get_llm_model_answer`方法是否可以被子类覆盖并实现。
def test_is_get_llm_model_answer_implemented():
    # 定义一个新的类TestLlm，继承自BaseLlm，并覆盖了`get_llm_model_answer`方法。
    class TestLlm(BaseLlm):
        def get_llm_model_answer(self):
            return "Implemented"
    # 创建一个BaseLlmConfig配置实例。
    config = BaseLlmConfig()
    # 使用配置实例创建TestLlm对象。
    llm = TestLlm(config=config)
    # 检查`get_llm_model_answer`方法返回的值是否是"Implemented"。
    assert llm.get_llm_model_answer() == "Implemented"

# 定义一个测试函数，检查`_stream_response`方法是否能正确处理分块响应。
def test_stream_response(base_llm):
    # 定义一个列表，作为模拟的分块响应。
    answer = ["Chunk1", "Chunk2", "Chunk3"]
    # 调用`_stream_response`方法，并将结果转换成列表。
    result = list(base_llm._stream_response(answer))
    # 检查结果是否与原始的分块响应相同。
    assert result == answer

# 定义一个测试函数，检查`_append_search_and_context`方法是否能正确拼接上下文和搜索结果。
def test_append_search_and_context(base_llm):
    # 定义上下文字符串。
    context = "Context"
    # 定义网络搜索结果字符串。
    web_search_result = "Web Search Result"
    # 调用`_append_search_and_context`方法。
    result = base_llm._append_search_and_context(context, web_search_result)
    # 定义期望的结果字符串。
    expected_result = "Context\nWeb Search Result: Web Search Result"
    # 检查结果是否与期望的结果相同。
    assert result == expected_result

# 定义一个测试函数，检查`access_search_and_get_results`方法是否能正确获取搜索结果。
def test_access_search_and_get_results(base_llm, mocker):
    # 使用mocker库的patch_object函数模拟`access_search_and_get_results`方法，并设置其返回值为"Search Results"。
    base_llm.access_search_and_get_results = mocker.patch.object(
        base_llm, "access_search_and_get_results", return_value="Search Results"
    )
    # 定义输入查询字符串。
    input_query = "Test query"
    # 调用模拟的方法。
    result = base_llm.access_search_and_get_results(input_query)
    # 检查返回的结果是否与预期的"Search Results"相同。
    assert result == "Search Results"

