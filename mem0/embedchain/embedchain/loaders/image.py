# 引入了一些必要的库，就像收集工具箱里的工具一样。
import base64
import hashlib
import os
from pathlib import Path

# 导入了处理OpenAI API的库，这个库能帮助我们与强大的人工智能对话。
from openai import OpenAI

# 这个库帮助我们处理JSON格式的数据，让数据可以被保存和读取。
from embedchain.helpers.json_serializable import register_deserializable

# 基础加载器，用于加载不同类型的数据。
from embedchain.loaders.base_loader import BaseLoader

# 定义了一个常量字符串，告诉AI我们需要它描述图片的内容。
DESCRIBE_IMAGE_PROMPT = "Describe the image:"

# 使用装饰器注册了一个类，这个类可以被序列化成JSON，方便存储和传输。
@register_deserializable

# 这是我们主要使用的类，它负责加载图像并获取描述。
class ImageLoader(BaseLoader):

    # 初始化函数，设置了一些默认参数，比如描述的最大长度、API密钥等。
    def __init__(self, max_tokens: int = 500, api_key: str = None, prompt: str = None):
        # 调用父类的初始化方法，继承一些通用功能。
        super().__init__()
        
        # 设置自定义的提示语，如果没有提供就使用默认的。
        self.custom_prompt = prompt or DESCRIBE_IMAGE_PROMPT
        
        # 设置描述的最大字数。
        self.max_tokens = max_tokens
        
        # 获取API密钥，如果没提供就从环境变量中读取。
        self.api_key = api_key or os.environ["OPENAI_API_KEY"]
        
        # 创建OpenAI客户端对象，这样我们就能调用其API了。
        self.client = OpenAI(api_key=self.api_key)

    # 静态方法，用于将图片文件编码成Base64格式，这样就可以在网络上传输。
    @staticmethod
    def _encode_image(image_path: str):
        # 打开图片文件，以二进制模式读取。
        with open(image_path, "rb") as image_file:
            # 读取文件内容，编码成Base64，然后解码成字符串。
            return base64.b64encode(image_file.read()).decode("utf-8")

    # 创建请求的方法，发送给OpenAI API，让它生成描述。
    def _create_completion_request(self, content: str):
        # 使用GPT模型创建完成请求，传入用户角色和内容。
        return self.client.chat.completions.create(
            model="gpt-4o", messages=[{"role": "user", "content": content}], max_tokens=self.max_tokens
        )

    # 处理URL或文件路径的方法，判断是网络图片还是本地文件。
    def _process_url(self, url: str):
        # 如果URL以"http"开头，说明是网络上的图片。
        if url.startswith("http"):
            # 返回一个包含提示语和图片URL的列表。
            return [{"type": "text", "text": self.custom_prompt}, {"type": "image_url", "image_url": {"url": url}}]
        # 如果是本地文件，检查文件是否存在。
        elif Path(url).is_file():
            # 获取文件扩展名，去掉点号。
            extension = Path(url).suffix.lstrip(".")
            
            # 将图片编码成Base64格式。
            encoded_image = self._encode_image(url)
            
            # 构造图片数据的Data URI格式。
            image_data = f"data:image/{extension};base64,{encoded_image}"
            
            # 返回一个包含提示语和图片数据的列表。
            return [{"type": "text", "text": self.custom_prompt}, {"type": "image", "image_url": {"url": image_data}}]
        # 如果既不是网络链接也不是本地文件，抛出错误。
        else:
            raise ValueError(f"Invalid URL or file path: {url}")

    # 加载数据的主要方法，接收一个URL或文件路径作为输入。
    def load_data(self, url: str):
        # 处理URL或文件路径，得到描述图像所需的信息。
        content = self._process_url(url)
        
        # 发送请求给OpenAI API，获取描述结果。
        response = self._create_completion_request(content)
        
        # 提取AI生成的描述文本。
        content = response.choices[0].message.content
        
        # 生成文档ID，用于唯一标识这次操作。
        doc_id = hashlib.sha256((content + url).encode()).hexdigest()
        
        # 返回一个字典，包含文档ID和数据信息，其中数据包括描述文本和元数据（URL和类型）。
        return {"doc_id": doc_id, "data": [{"content": content, "meta_data": {"url": url, "type": "image"}}]}

