# 这里使用了一个工具来忽略某些代码风格检查规则

# 导入文本分块器类
from embedchain.chunkers.text import TextChunker
# 导入配置类，用于设置分块参数
from embedchain.config import ChunkerConfig
# 导入数据类型枚举类，用于指定处理的数据类型
from embedchain.models.data_type import DataType


# 定义一个测试类，用于测试文本分块器的功能
class TestTextChunker:
    # 测试没有应用ID时的分块功能
    def test_chunks_without_app_id(self):
        """
        检查TextChunker生成的分块是否正确。
        """
        # 创建一个配置对象，设置分块大小、重叠量和最小分块大小
        chunker_config = ChunkerConfig(chunk_size=10, chunk_overlap=0, length_function=len, min_chunk_size=0)
        # 使用上述配置创建一个文本分块器实例
        chunker = TextChunker(config=chunker_config)
        # 设置一段测试文本
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        # 手动设置数据类型为文本
        chunker.set_data_type(DataType.TEXT)
        # 调用分块器的create_chunks方法，传入模拟加载器、文本和配置
        result = chunker.create_chunks(MockLoader(), text, chunker_config)
        # 获取结果中的文档列表
        documents = result["documents"]
        # 断言文档数量大于5，验证分块效果
        assert len(documents) > 5

    # 测试有应用ID时的分块功能，实际上这里的实现与上个测试方法相同
    def test_chunks_with_app_id(self):
        """
        检查带有app_id的TextChunker生成的分块是否正确。
        """
        # 创建配置、实例化分块器、设置文本和数据类型等步骤与上个方法一样
        chunker_config = ChunkerConfig(chunk_size=10, chunk_overlap=0, length_function=len, min_chunk_size=0)
        chunker = TextChunker(config=chunker_config)
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        chunker.set_data_type(DataType.TEXT)
        # 调用分块方法并获取结果
        result = chunker.create_chunks(MockLoader(), text, chunker_config)
        documents = result["documents"]
        # 断言文档数量大于5
        assert len(documents) > 5

    # 测试非常大的分块大小情况
    def test_big_chunksize(self):
        """
        当使用无限大的分块大小时，应该只返回一个分块。
        """
        # 设置分块大小为一个极大的数，意味着整个文本作为一个分块
        chunker_config = ChunkerConfig(chunk_size=9999999999, chunk_overlap=0, length_function=len, min_chunk_size=0)
        chunker = TextChunker(config=chunker_config)
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        chunker.set_data_type(DataType.TEXT)
        # 调用分块方法并获取结果
        result = chunker.create_chunks(MockLoader(), text, chunker_config)
        documents = result["documents"]
        # 断言文档列表长度为1，即只有一个分块
        assert len(documents) == 1

    # 测试极小的分块大小情况
    def test_small_chunksize(self):
        """
        当分块大小设为1时，每个字符应该成为一个独立的分块。
        """
        # 设置分块大小为1
        chunker_config = ChunkerConfig(chunk_size=1, chunk_overlap=0, length_function=len, min_chunk_size=0)
        chunker = TextChunker(config=chunker_config)
        # 使用一个包含各种字符的长字符串作为测试文本
        text = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c"""
        chunker.set_data_type(DataType.TEXT)
        # 调用分块方法并获取结果
        result = chunker.create_chunks(MockLoader(), text, chunker_config)
        documents = result["documents"]
        # 断言文档列表长度等于原始文本长度，确保每个字符都被分块
        assert len(documents) == len(text)

    # 测试单词计数功能
    def test_word_count(self):
        # 创建配置、实例化分块器、设置数据类型等步骤与之前相同
        chunker_config = ChunkerConfig(chunk_size=1, chunk_overlap=0, length_function=len, min_chunk_size=0)
        chunker = TextChunker(config=chunker_config)
        chunker.set_data_type(DataType.TEXT)

        # 定义一个文档列表，包含两个字符串元素
        document = ["ab cd", "ef gh"]
        # 调用get_word_count方法计算文档中单词总数
        result = chunker.get_word_count(document)
        # 断言结果等于4，因为总共有4个单词
        assert result == 4


# 定义一个模拟加载器类，用于在测试中模拟数据加载过程
class MockLoader:
    # 定义静态方法load_data，用于返回一个字典，其中包含文档ID和数据内容
    @staticmethod
    def load_data(src) -> dict:
        """
        这个模拟加载器会返回一个包含数据字典的列表。你可以调整这个方法以返回不同的数据用于测试。
        """
        return {
            "doc_id": "123",
            "data": [
                {
                    "content": src,
                    "meta_data": {"url": "none"},
                }
            ],
        }

