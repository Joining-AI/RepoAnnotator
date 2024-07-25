# 导入我们需要的一些工具包
import importlib
import os

import pytest

# 从一个叫embedchain的包里导入配置类和HuggingFaceLlm这个模型类
from embedchain.config import BaseLlmConfig
from embedchain.llm.huggingface import HuggingFaceLlm

# 这个函数是为了测试准备环境的，它会设置一个环境变量，然后创建一个配置对象，最后清理环境变量
@pytest.fixture
def huggingface_llm_config():
    # 设置环境变量，这像是告诉电脑我们要用哪个钥匙开门
    os.environ["HUGGINGFACE_ACCESS_TOKEN"] = "test_access_token"
    # 创建配置对象，告诉模型我们要用哪个模型，以及一些参数
    config = BaseLlmConfig(model="google/flan-t5-xxl", max_tokens=50, temperature=0.7, top_p=0.8)
    # 使用yield关键字，这就像说“现在你可以用这个配置了”
    yield config
    # 清理工作，测试完后把设置的环境变量拿掉，保持干净
    os.environ.pop("HUGGINGFACE_ACCESS_TOKEN")

# 另一个准备环境的函数，但这次是为测试自定义端点（就像是自定义的大门）
@pytest.fixture
def huggingface_endpoint_config():
    # 同样的，设置环境变量
    os.environ["HUGGINGFACE_ACCESS_TOKEN"] = "test_access_token"
    # 创建配置对象，但这次指定的是一个网络地址
    config = BaseLlmConfig(endpoint="https://api-inference.huggingface.co/models/gpt2", model_kwargs={"device": "cpu"})
    yield config
    # 清理工作
    os.environ.pop("HUGGINGFACE_ACCESS_TOKEN")

# 测试如果没有API密钥就初始化模型，应该会出错
def test_init_raises_value_error_without_api_key(mocker):
    # 清除所有环境变量，就像清理房间一样
    mocker.patch.dict(os.environ, clear=True)
    # 尝试没有密钥的情况下初始化模型，如果不出错，那么测试失败
    with pytest.raises(ValueError):
        HuggingFaceLlm()

# 测试如果系统提示（system_prompt）被设置了，应该会出错
def test_get_llm_model_answer_raises_value_error_for_system_prompt(huggingface_llm_config):
    # 初始化模型并设置系统提示
    llm = HuggingFaceLlm(huggingface_llm_config)
    llm.config.system_prompt = "system_prompt"
    # 如果不报错，测试失败
    with pytest.raises(ValueError):
        llm.get_llm_model_answer("prompt")

# 测试top_p参数是否在合理范围内，如果不在，应该会出错
def test_top_p_value_within_range():
    # 创建配置对象，设置top_p为1.0
    config = BaseLlmConfig(top_p=1.0)
    # 尝试使用这个配置，如果top_p超出范围，应该出错
    with pytest.raises(ValueError):
        HuggingFaceLlm._get_answer("test_prompt", config)

# 检查依赖库是否已经安装
def test_dependency_is_imported():
    # 假设库已经安装
    importlib_installed = True
    # 尝试导入库，如果导入失败，改变标志
    try:
        importlib.import_module("huggingface_hub")
    except ImportError:
        importlib_installed = False
    # 确认库是否真的安装了
    assert importlib_installed

# 测试获取模型答案的函数
def test_get_llm_model_answer(huggingface_llm_config, mocker):
    # 模拟返回答案的行为
    mocker.patch("embedchain.llm.huggingface.HuggingFaceLlm._get_answer", return_value="Test answer")
    # 初始化模型并获取答案，检查答案是否正确
    llm = HuggingFaceLlm(huggingface_llm_config)
    answer = llm.get_llm_model_answer("Test query")
    assert answer == "Test answer"

# 测试模拟HuggingFace模型实例
def test_hugging_face_mock(huggingface_llm_config, mocker):
    # 模拟HuggingFace模型实例的回答
    mock_llm_instance = mocker.Mock(return_value="Test answer")
    # 模拟HuggingFaceHub的调用
    mock_hf_hub = mocker.patch("embedchain.llm.huggingface.HuggingFaceHub")
    mock_hf_hub.return_value.invoke = mock_llm_instance
    # 初始化模型并获取答案，确保调用正确
    llm = HuggingFaceLlm(huggingface_llm_config)
    answer = llm.get_llm_model_answer("Test query")
    assert answer == "Test answer"
    mock_llm_instance.assert_called_once_with("Test query")

# 测试自定义端点的功能
def test_custom_endpoint(huggingface_endpoint_config, mocker):
    # 模拟自定义端点的回答
    mock_llm_instance = mocker.Mock(return_value="Test answer")
    # 模拟HuggingFaceEndpoint的调用
    mock_hf_endpoint = mocker.patch("embedchain.llm.huggingface.HuggingFaceEndpoint")
    mock_hf_endpoint.return_value.invoke = mock_llm_instance
    # 初始化模型并获取答案，确保调用正确
    llm = HuggingFaceLlm(huggingface_endpoint_config)
    answer = llm.get_llm_model_answer("Test query")
    assert answer == "Test answer"
    mock_llm_instance.assert_called_once_with("Test query")

