# 导入需要的库
import hashlib  # 用于生成哈希值
from unittest.mock import MagicMock, Mock, patch  # 用于模拟对象和方法
import pytest  # 测试框架

# 导入自定义的YouTube视频加载器
from embedchain.loaders.youtube_video import YoutubeVideoLoader

# 定义一个测试用的YouTube视频加载器实例
@pytest.fixture
def youtube_video_loader():
    return YoutubeVideoLoader()  # 创建并返回一个YouTube视频加载器实例

# 测试加载数据的方法
def test_load_data(youtube_video_loader):  # 接受上面创建的实例作为参数
    video_url = "https://www.youtube.com/watch?v=VIDEO_ID"  # 假设的视频网址
    mock_loader = Mock()  # 创建一个模拟的加载器
    mock_page_content = "This is a YouTube video content."  # 模拟的视频内容
    # 设置模拟加载器的返回值
    mock_loader.load.return_value = [
        MagicMock(  # 创建一个模拟的对象
            page_content=mock_page_content,  # 设置模拟对象的内容属性
            metadata={"url": video_url, "title": "Test Video"},  # 设置模拟对象的元数据
        )
    ]
    mock_transcript = [{"text": "sample text", "start": 0.0, "duration": 5.0}]  # 模拟字幕数据

    # 使用模拟技术替换真实的YouTube加载器和获取字幕的方法
    with patch("embedchain.loaders.youtube_video.YoutubeLoader.from_youtube_url", return_value=mock_loader), \
         patch("embedchain.loaders.youtube_video.YouTubeTranscriptApi.get_transcript", return_value=mock_transcript):
        result = youtube_video_loader.load_data(video_url)  # 调用加载数据的方法

    # 计算期望的文档ID
    expected_doc_id = hashlib.sha256((mock_page_content + video_url).encode()).hexdigest()

    # 确认返回结果中的文档ID与期望的相同
    assert result["doc_id"] == expected_doc_id

    # 预期的数据格式
    expected_data = [
        {
            "content": "This is a YouTube video content.",  # 视频内容
            "meta_data": {  # 元数据
                "url": video_url,  # 视频URL
                "title": "Test Video",  # 标题
                "transcript": "Unavailable",  # 字幕信息（这里假设不可用）
            }
        }
    ]

    # 确认返回结果中的数据与预期的数据相同
    assert result["data"] == expected_data

# 测试当没有数据时加载数据的方法的行为
def test_load_data_with_empty_doc(youtube_video_loader):  # 接受上面创建的实例作为参数
    video_url = "https://www.youtube.com/watch?v=VIDEO_ID"  # 假设的视频网址
    mock_loader = Mock()  # 创建一个模拟的加载器
    mock_loader.load.return_value = []  # 设置模拟加载器返回空列表

    # 使用模拟技术替换真实的YouTube加载器
    with patch("embedchain.loaders.youtube_video.YoutubeLoader.from_youtube_url", return_value=mock_loader):
        # 尝试调用加载数据的方法，并期待它抛出一个错误
        with pytest.raises(ValueError):
            youtube_video_loader.load_data(video_url)

