# 导入我们需要的一些工具，就像是准备好了工具箱开始做手工。
import os
from typing import Optional

# 这是从一个叫做langchain的宝库里拿出来的工具，用来帮助我们和聊天机器人交流。
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models import JinaChat

# 这是从另一个宝库embedchain里拿出来的配置工具，让我们可以设置一些参数。
from embedchain.config import BaseLlmConfig
# 这个工具帮助我们处理一些数据，让它更容易被保存和读取。
from embedchain.helpers.json_serializable import register_deserializable
# 这是我们的基础聊天机器人框架，我们可以基于它来创建更复杂的机器人。
from embedchain.llm.base import BaseLlm

# 这个装饰器像是给我们的类贴上了一个标签，告诉系统这个类是可以被保存和读取的。
@register_deserializable
class JinaLlm(BaseLlm):
    # 这是我们的聊天机器人的构造函数，当我们创建一个新的聊天机器人时，这里会被调用。
    def __init__(self, config: Optional[BaseLlmConfig] = None):
        # 调用父类的构造函数，就像是站在巨人的肩膀上开始自己的冒险。
        super().__init__(config=config)
        # 检查我们是否有了和JinaChat聊天机器人交流的密钥，如果没有，会提醒我们设置。
        if not self.config.api_key and "JINACHAT_API_KEY" not in os.environ:
            raise ValueError("请设置JINACHAT_API_KEY环境变量或在配置中传递。")

    # 这个方法是用来获取聊天机器人的回答的。
    def get_llm_model_answer(self, prompt):
        # 我们调用一个内部的方法来得到答案，然后返回这个答案。
        response = JinaLlm._get_answer(prompt, self.config)
        return response

    # 这是一个静态方法，它不需要实例化就可以使用，用来从JinaChat得到答案。
    @staticmethod
    def _get_answer(prompt: str, config: BaseLlmConfig) -> str:
        # 首先，我们创建一个空的消息列表，就像准备了一个空的信封。
        messages = []
        # 如果有系统提示，我们就把它加入到信封里。
        if config.system_prompt:
            messages.append(SystemMessage(content=config.system_prompt))
        # 然后，把用户的问题也加入到信封里。
        messages.append(HumanMessage(content=prompt))
        # 准备一些参数，就像是准备好了邮票和地址，准备寄信。
        kwargs = {
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            # 这里我们找到了和JinaChat聊天机器人交流的密钥，如果在配置中没有，就从环境变量里找。
            "jinachat_api_key": config.api_key or os.environ["JINACHAT_API_KEY"],
            "model_kwargs": {},
        }
        # 如果有额外的参数，我们也加进去。
        if config.top_p:
            kwargs["model_kwargs"]["top_p"] = config.top_p
        # 如果需要流式输出，就像是一边写信一边读信，我们就要准备特殊的信纸。
        if config.stream:
            # 这是我们需要的特殊信纸，它能让我们看到信是如何被写的。
            from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
            # 创建一个聊天机器人，用我们准备好的参数和信纸。
            chat = JinaChat(**kwargs, streaming=config.stream, callbacks=[StreamingStdOutCallbackHandler()])
        else:
            # 如果不需要流式输出，我们就用普通的信纸创建一个聊天机器人。
            chat = JinaChat(**kwargs)
        # 最后，我们发送信件（消息），并返回聊天机器人的回复内容。
        return chat(messages).content

