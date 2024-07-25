import numpy as np

# 这个函数用于测试生成问题嵌入的功能。
def test_generate_embedding(mock_answer_relevance_metric, mock_data, monkeypatch):
    # 这里我们告诉程序当它需要创建一个嵌入时，就返回一个有三个数字（1, 2, 3）的列表。
    monkeypatch.setattr(
        mock_answer_relevance_metric.client.embeddings,
        "create",
        lambda input, model: type("obj", (object,), {"data": [type("obj", (object,), {"embedding": [1, 2, 3]})]})(),
    )
    # 现在我们调用这个功能，传入一个问题作为测试。
    embedding = mock_answer_relevance_metric._generate_embedding("This is a test question.")
    # 我们检查返回的嵌入是否由三个数字组成。
    assert len(embedding) == 3

