# 导入操作系统相关的功能，这里可能会用来设置环境变量。
import os

# 导入pytest库，这是一个用于编写测试用例的框架。
import pytest

# 从一个名为`embedchain`的包中导入`llama2`模块下的`Llama2Llm`类。
from embedchain.llm.llama2 import Llama2Llm

# 定义了一个特殊的函数`fixture`叫做`llama2_llm`，这个函数会在运行测试之前被调用一次。
@pytest.fixture
def llama2_llm():
    # 设置一个环境变量`REPLICATE_API_TOKEN`，值为`test_api_token`。
    os.environ["REPLICATE_API_TOKEN"] = "test_api_token"
    # 创建一个`Llama2Llm`对象实例。
    llm = Llama2Llm()
    # 把创建的对象返回出去，这样其他测试函数可以使用它。
    return llm

# 定义一个测试函数，名字叫做`test_init_raises_value_error_without_api_key`。
def test_init_raises_value_error_without_api_key(mocker):
    # 使用`mocker`工具（模拟器）清除所有的环境变量。
    mocker.patch.dict(os.environ, clear=True)
    # 这段代码会尝试创建`Llama2Llm`对象，如果没有API密钥，应该会抛出`ValueError`异常。
    with pytest.raises(ValueError):
        Llama2Llm()

# 定义一个测试函数，名字叫做`test_get_llm_model_answer_raises_value_error_for_system_prompt`。
def test_get_llm_model_answer_raises_value_error_for_system_prompt(llama2_llm):
    # 给`llama2_llm`对象的`config.system_prompt`属性设置一个值`system_prompt`。
    llama2_llm.config.system_prompt = "system_prompt"
    # 当调用`get_llm_model_answer`方法并传入参数`prompt`时，应该会抛出`ValueError`异常。
    with pytest.raises(ValueError):
        llama2_llm.get_llm_model_answer("prompt")

# 定义一个测试函数，名字叫做`test_get_llm_model_answer`。
def test_get_llm_model_answer(llama2_llm, mocker):
    # 使用`mocker`工具（模拟器）来模拟`Replicate`类的行为。
    mocked_replicate = mocker.patch("embedchain.llm.llama2.Replicate")
    # 创建一个可以模拟任何方法或属性的模拟对象。
    mocked_replicate_instance = mocker.MagicMock()
    # 指定模拟`Replicate`类时返回的是`mocked_replicate_instance`。
    mocked_replicate.return_value = mocked_replicate_instance
    # 模拟`invoke`方法的返回值是`"Test answer"`。
    mocked_replicate_instance.invoke.return_value = "Test answer"

    # 给`llama2_llm`对象的配置属性设置一些值：模型名、最大令牌数、温度、top_p。
    llama2_llm.config.model = "test_model"
    llama2_llm.config.max_tokens = 50
    llama2_llm.config.temperature = 0.7
    llama2_llm.config.top_p = 0.8

    # 调用`get_llm_model_answer`方法并传入查询字符串`"Test query"`，把返回的结果存储在`answer`变量里。
    answer = llama2_llm.get_llm_model_answer("Test query")

    # 检查`answer`变量是否等于`"Test answer"`。
    assert answer == "Test answer"

