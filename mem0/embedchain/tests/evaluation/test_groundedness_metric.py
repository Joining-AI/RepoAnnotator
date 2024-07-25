# 导入所需的库和模块
import numpy as np
# 导入用于测试的库
import pytest

# 从相应的模块中导入配置类、评估指标、以及一些实用工具
from embedchain.config.evaluation.base import GroundednessConfig
from embedchain.evaluation.metrics import Groundedness
from embedchain.utils.evaluation import EvalData, EvalMetric

# 定义一个测试用例生成器，用来创建模拟的数据集
@pytest.fixture
def mock_data():
    # 返回一个包含两个示例数据点的列表
    return [
        # 第一个数据点：包含一个上下文、一个问题、以及一个答案
        EvalData(
            contexts=[
                "这是一个测试上下文 1。",
            ],
            question="这是一个测试问题 1。",
            answer="这是一个测试答案 1。",
        ),
        # 第二个数据点：包含两个上下文、一个问题、以及一个答案
        EvalData(
            contexts=[
                "这是一个测试上下文 2-1。",
                "这是一个测试上下文 2-2。",
            ],
            question="这是一个测试问题 2。",
            answer="这是一个测试答案 2。",
        ),
    ]

# 定义一个测试用例生成器，用来创建模拟的评估指标对象
@pytest.fixture
def mock_groundedness_metric(monkeypatch):
    # 设置一个环境变量用于测试API密钥
    monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")
    # 创建并返回一个Groundedness实例
    metric = Groundedness()
    return metric

# 测试Groundedness初始化方法
def test_groundedness_init(monkeypatch):
    # 设置一个环境变量用于测试API密钥
    monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")
    # 创建一个Groundedness实例
    metric = Groundedness()
    # 检查名称是否正确
    assert metric.name == EvalMetric.GROUNDEDNESS.value
    # 检查默认使用的模型是否是gpt-4
    assert metric.config.model == "gpt-4"
    # 检查API密钥是否为空（这里应该为空，因为我们设置了环境变量）
    assert metric.config.api_key is None
    # 删除设置的环境变量
    monkeypatch.delenv("OPENAI_API_KEY")

# 测试Groundedness初始化时传入配置选项
def test_groundedness_init_with_config():
    # 创建一个Groundedness实例并传入配置选项
    metric = Groundedness(config=GroundednessConfig(api_key="test_api_key"))
    # 检查名称是否正确
    assert metric.name == EvalMetric.GROUNDEDNESS.value
    # 检查默认使用的模型是否是gpt-4
    assert metric.config.model == "gpt-4"
    # 检查传入的API密钥是否被正确设置
    assert metric.config.api_key == "test_api_key"

# 测试当没有提供API密钥时初始化Groundedness会抛出异常
def test_groundedness_init_without_api_key(monkeypatch):
    # 删除环境中的API密钥变量
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    # 尝试创建Groundedness实例，期望抛出ValueError异常
    with pytest.raises(ValueError):
        Groundedness()

# 测试生成答案声明提示的方法
def test_generate_answer_claim_prompt(mock_groundedness_metric, mock_data):
    # 生成第一个数据点的答案声明提示
    prompt = mock_groundedness_metric._generate_answer_claim_prompt(data=mock_data[0])
    # 检查提示中是否包含了问题和答案
    assert "这是一个测试问题 1." in prompt
    assert "这是一个测试答案 1." in prompt

# 测试获取声明语句的方法
def test_get_claim_statements(mock_groundedness_metric, mock_data, monkeypatch):
    # 假装调用OpenAI API返回了一些测试数据
    monkeypatch.setattr(
        mock_groundedness_metric.client.chat.completions,
        "create",
        lambda *args, **kwargs: type(
            "obj",
            (object,),
            {
                "choices": [
                    type(
                        "obj",
                        (object,),
                        {
                            "message": type(
                                "obj",
                                (object,),
                                {
                                    "content": """这是一个测试答案 1。
                                                                                        这是一个测试答案 2。
                                                                                        这是一个测试答案 3."""
                                },
                            )
                        },
                    )
                ]
            },
        )(),
    )
    # 生成第一个数据点的答案声明提示
    prompt = mock_groundedness_metric._generate_answer_claim_prompt(data=mock_data[0])
    # 获取声明语句
    claim_statements = mock_groundedness_metric._get_claim_statements(prompt=prompt)
    # 检查返回了三个声明语句
    assert len(claim_statements) == 3
    # 检查其中是否包含测试答案1
    assert "这是一个测试答案 1." in claim_statements

# 测试生成声明推断提示的方法
def test_generate_claim_inference_prompt(mock_groundedness_metric, mock_data):
    # 生成第一个数据点的答案声明提示
    prompt = mock_groundedness_metric._generate_answer_claim_prompt(data=mock_data[0])
    # 准备一些测试的声明语句
    claim_statements = [
        "这是一个测试声明 1。",
        "这是一个测试声明 2。",
    ]
    # 生成声明推断提示
    prompt = mock_groundedness_metric._generate_claim_inference_prompt(
        data=mock_data[0], claim_statements=claim_statements
    )
    # 检查提示中是否包含了上下文和声明语句
    assert "这是一个测试上下文 1." in prompt
    assert "这是一个测试声明 1." in prompt

# 这个函数是用来测试获取判断得分的方法是否正确的。
def test_get_claim_verdict_scores(mock_groundedness_metric, mock_data, monkeypatch):
    # 使用monkeypatch来模拟`client.chat.completions.create`这个方法的行为，
    # 当这个方法被调用时，它会返回一个模拟的对象，对象里面包含了一个得分信息。
    monkeypatch.setattr(
        mock_groundedness_metric.client.chat.completions,
        "create",
        lambda *args, **kwargs: type(
            "obj",
            (object,),
            {"choices": [type("obj", (object,), {"message": type("obj", (object,), {"content": "1\n0\n-1"})})]},
        )(),
    )
    # 生成一条用于询问的回答提示语。
    prompt = mock_groundedness_metric._generate_answer_claim_prompt(data=mock_data[0])
    # 根据上面生成的提示语，得到一些待验证的陈述。
    claim_statements = mock_groundedness_metric._get_claim_statements(prompt=prompt)
    # 再次根据提示语和得到的陈述，生成一个新的提示语。
    prompt = mock_groundedness_metric._generate_claim_inference_prompt(
        data=mock_data[0], claim_statements=claim_statements
    )
    # 根据新的提示语，获取判断得分。
    claim_verdict_scores = mock_groundedness_metric._get_claim_verdict_scores(prompt=prompt)
    # 确认得分列表的长度应该是3。
    assert len(claim_verdict_scores) == 3
    # 确认第一个得分是1。
    assert claim_verdict_scores[0] == 1
    # 确认第二个得分是0。
    assert claim_verdict_scores[1] == 0

