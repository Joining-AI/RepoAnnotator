# 导入一些必要的工具包，就像我们画画前需要准备画笔和颜料一样。
import os
from collections.abc import Iterable
from pathlib import Path
from typing import Optional, Union

# 这里导入的是处理语言模型输出结果的工具，就像翻译机帮助我们理解外语一样。
from langchain.callbacks.stdout import StdOutCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# 下面这两行是配置语言模型用的，就像是调整画笔的粗细和颜色。
from embedchain.config import BaseLlmConfig
from embedchain.helpers.json_serializable import register_deserializable
from embedchain.llm.base import BaseLlm

# 这个装饰器就像是告诉别人，“嘿，我这个类是可以被序列化的哦！”
@register_deserializable
class GPT4ALLLlm(BaseLlm):
    def __init__(self, config: Optional[BaseLlmConfig] = None):
        # 这里是初始化，就像是开始准备画画前，先铺好画纸。
        super().__init__(config=config)
        # 如果没有指定模型，那就默认使用这个模型，就像如果没有选颜色，就用蓝色画天空。
        if self.config.model is None:
            self.config.model = "orca-mini-3b-gguf2-q4_0.gguf"
        # 创建模型实例，就像是把画笔准备好。
        self.instance = GPT4ALLLlm._get_instance(self.config.model)
        # 设置是否流式输出，就像画画时是慢慢一笔一笔画还是直接完成。
        self.instance.streaming = self.config.stream

    # 这个方法是获取模型的回答，就像是问画里的小动物问题，然后它回答你。
    def get_llm_model_answer(self, prompt):
        return self._get_answer(prompt=prompt, config=self.config)

    # 静态方法，用于获取模型实例，就像去文具店买画笔。
    @staticmethod
    def _get_instance(model):
        # 尝试导入GPT4All模型，就像尝试找到画笔。
        try:
            from langchain_community.llms.gpt4all import GPT4All as LangchainGPT4All
        except ModuleNotFoundError:
            # 如果找不到画笔，就告诉我们要去买。
            raise ModuleNotFoundError(
                "The GPT4All python package is not installed. Please install it with `pip install --upgrade embedchain[opensource]`"
            )
        # 检查模型路径，就像检查画笔是不是在包里。
        model_path = Path(model).expanduser()
        if os.path.isabs(model_path):
            if os.path.exists(model_path):
                # 如果模型路径正确，就创建模型实例。
                return LangchainGPT4All(model=str(model_path))
            else:
                # 如果模型不存在，就报错。
                raise ValueError(f"Model does not exist at {model_path=}")
        else:
            # 如果模型路径不完整，允许下载模型。
            return LangchainGPT4All(model=model, allow_download=True)

    # 这个方法是获取答案的核心，就像真正开始画画并得到作品。
    def _get_answer(self, prompt: str, config: BaseLlmConfig) -> Union[str, Iterable]:
        # 检查运行时是否可以切换模型，就像不能在画画过程中换画笔。
        if config.model and config.model != self.config.model:
            raise RuntimeError("GPT4ALLLlm does not support switching models at runtime.")
        
        # 准备消息，就像在画布上打草稿。
        messages = []
        if config.system_prompt:
            messages.append(config.system_prompt)
        messages.append(prompt)
        
        # 设置生成参数，就像设置画笔的硬度和颜色。
        kwargs = {
            "temp": config.temperature,
            "max_tokens": config.max_tokens,
        }
        if config.top_p:
            kwargs["top_p"] = config.top_p

        # 设置回调，就像设置画画过程中的反馈机制。
        callbacks = [StreamingStdOutCallbackHandler()] if config.stream else [StdOutCallbackHandler()]
        
        # 开始生成，就像开始画画。
        response = self.instance.generate(prompts=messages, callbacks=callbacks, **kwargs)
        answer = ""
        # 收集答案，就像收集画完的画。
        for generations in response.generations:
            answer += " ".join(map(lambda generation: generation.text, generations))
        return answer

