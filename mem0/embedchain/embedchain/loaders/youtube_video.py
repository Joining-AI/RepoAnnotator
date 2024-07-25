# 引入一些工具包，这些就像是我们做手工前准备的材料。
import hashlib           # 这个工具可以帮我们生成一种特殊的编码，用来唯一标识东西。
import json              # 这个工具帮助我们处理和读取一种叫做JSON的数据格式。
import logging           # 这个工具让我们可以在程序运行时记录信息，就像写日记一样。

# 尝试加载一个特别的库，这个库可以帮助我们从YouTube视频中获取字幕。
try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    # 如果没有这个库，会告诉用户需要安装它，就像告诉他们缺少了做手工的一个重要工具。
    raise ImportError("YouTube视频需要额外的依赖。用`pip install youtube-transcript-api`来安装")

# 再次尝试加载一些库，这次是为了处理YouTube视频的其他信息。
try:
    from langchain_community.document_loaders import YoutubeLoader
    from langchain_community.document_loaders.youtube import _parse_video_id
except ImportError:
    # 同样地，如果缺少这些库，会提示用户如何安装。
    raise ImportError("YouTube视频需要额外的依赖。用`pip install pytube==15.0.0`来安装") from None

# 引入两个工具，一个用于让类可以被序列化（就像把玩具装进盒子里），另一个用于清理字符串（就像擦干净玩具）。
from embedchain.helpers.json_serializable import register_deserializable
from embedchain.loaders.base_loader import BaseLoader
from embedchain.utils.misc import clean_string

# 这里注册了一个可以序列化的类，就像给玩具盒贴上标签，让它能被识别。
@register_deserializable
class YoutubeVideoLoader(BaseLoader):
    def load_data(self, url):
        # 这个函数的作用是从YouTube视频中加载数据。
        video_id = _parse_video_id(url)   # 先解析出视频的ID，就像找到视频的钥匙。

        # 初始化我们想要的语言列表，这里默认是英语。
        languages = ["en"]
        
        # 尝试获取视频的字幕，就像试图从视频里找出隐藏的宝藏。
        try:
            # 获取所有可用的字幕语言，然后选择其中的一种（这里是默认英语）。
            languages = [transcript.language_code for transcript in YouTubeTranscriptApi.list_transcripts(video_id)]
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            # 把字幕转换成JSON格式，避免一些奇怪的符号，就像确保宝藏地图上的标记清晰可读。
            transcript = json.dumps(transcript, ensure_ascii=True)
        except Exception:
            # 如果获取字幕失败，记录错误并设定字幕为“不可用”。
            logging.exception(f"无法为视频 {url} 获取字幕")
            transcript = "Unavailable"

        # 使用YoutubeLoader加载视频信息，就像从视频里提取更多的信息宝藏。
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=True, language=languages)
        doc = loader.load()   # 加载视频信息到文档中。

        # 检查是否成功加载了数据，如果没有，抛出错误，就像发现宝箱是空的一样。
        if not len(doc):
            raise ValueError(f"对于网址：{url}，没有找到数据")

        # 清理内容，就像整理好宝藏里的物品。
        content = doc[0].page_content
        content = clean_string(content)

        # 收集元数据，就像收集宝藏的描述和来源信息。
        metadata = doc[0].metadata
        metadata["url"] = url
        metadata["transcript"] = transcript

        # 把内容和元数据组合起来，就像把宝藏和它的描述放在同一个袋子里。
        output = [
            {
                "content": content,
                "meta_data": metadata,
            }
        ]

        # 创建一个唯一的文档ID，就像给每个宝藏打上独一无二的标签。
        doc_id = hashlib.sha256((content + url).encode()).hexdigest()

        # 最后，返回一个字典，里面包含了文档ID和整理好的数据，就像把宝藏和标签一起打包好。
        return {
            "doc_id": doc_id,
            "data": output,
        }

