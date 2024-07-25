# 引入了hashlib库，它用于生成加密的哈希值。
import hashlib

# 引入pytest库，这是一个用于编写测试代码的框架。
import pytest

# 从embedchain这个程序中，引入了一个叫做LocalQnaPairLoader的类，这个类能帮助我们加载本地的问答对数据。
from embedchain.loaders.local_qna_pair import LocalQnaPairLoader

# 使用pytest的一个特殊装饰器@fixture，创建了一个叫qna_pair_loader的测试资源。
# 这个资源会返回一个LocalQnaPairLoader类的实例，这样在测试函数中就可以直接使用这个实例了。
@pytest.fixture
def qna_pair_loader():
    return LocalQnaPairLoader()

# 定义了一个名为test_load_data的测试函数，它接受一个参数qna_pair_loader。
# 这个参数就是上面定义的测试资源，已经是一个LocalQnaPairLoader的实例了。
def test_load_data(qna_pair_loader):
    # 定义了一个问题字符串，问题是“法国的首都是什么？”
    question = "What is the capital of France?"
    # 定义了一个答案字符串，答案是“法国的首都是巴黎。”
    answer = "The capital of France is Paris."

    # 将问题和答案组合成一个元组，叫做content。
    content = (question, answer)
    # 使用qna_pair_loader实例的load_data方法处理content，得到结果，存储在result变量里。
    result = qna_pair_loader.load_data(content)

    # 检查result字典里是否包含键"doc_id"，确保有文档ID信息。
    assert "doc_id" in result
    # 检查result字典里是否包含键"data"，确保有数据信息。
    assert "data" in result
    # 设定一个字符串变量url，这里设为"local"，表示数据来源是本地的。
    url = "local"

    # 把问题和答案格式化成期望的内容格式，问题后面跟着答案，用换行符隔开。
    expected_content = f"Q: {question}\nA: {answer}"
    # 检查result字典里的"data"键下的第一个元素的"content"是否与expected_content相等。
    assert result["data"][0]["content"] == expected_content

    # 检查result字典里的"data"键下的第一个元素的"meta_data"键下的"url"是否等于设定的url。
    assert result["data"][0]["meta_data"]["url"] == url

    # 检查result字典里的"data"键下的第一个元素的"meta_data"键下的"question"是否等于问题字符串。
    assert result["data"][0]["meta_data"]["question"] == question

    # 使用hashlib库中的sha256算法，将expected_content和url组合并编码后生成一个哈希值。
    expected_doc_id = hashlib.sha256((expected_content + url).encode()).hexdigest()
    # 最后，检查result字典里的"doc_id"是否等于预期的哈希值expected_doc_id。
    assert result["doc_id"] == expected_doc_id

