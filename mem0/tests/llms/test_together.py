# 导入测试相关的库。
import pytest
# 导入模拟对象和补丁工具，用来模拟外部的行为。
from unittest.mock import Mock, patch
# 导入自定义的聊天机器人模型类。
from mem0.llms.together import TogetherLLM
# 导入基础配置类。
from mem0.configs.llms.base import BaseLlmConfig

# 定义一个特殊的函数，用于在测试中模拟“Together”客户端。
@pytest.fixture
def mock_together_client():
    # 使用补丁工具模拟“Together”类。
    with patch('mem0.llms.together.Together') as mock_together:
        # 创建一个模拟的客户端对象。
        mock_client = Mock()
        # 设置模拟返回值为我们创建的模拟客户端。
        mock_together.return_value = mock_client
        # 让测试函数可以使用这个模拟客户端。
        yield mock_client

