# 这里我们导入了一个叫做 importlib 的工具箱，它能帮助我们动态加载 Python 模块。
import importlib

# 导入了一个名为 BaseLlmConfig 的类，这个类定义了语言模型的基本配置信息。
from mem0.configs.llms.base import BaseLlmConfig


# 定义了一个叫做 load_class 的函数，它的任务是从字符串中找到对应的类并创建它。
def load_class(class_type):
    # 把字符串中的模块路径和类名分开，比如 "mem0.llms.ollama.OllamaLLM" 变成 "mem0.llms.ollama" 和 "OllamaLLM"。
    module_path, class_name = class_type.rsplit(".", 1)
    # 使用 importlib 工具箱加载模块。
    module = importlib.import_module(module_path)
    # 从模块中获取类，并返回这个类。
    return getattr(module, class_name)


# 定义了一个叫做 LlmFactory 的类，它是用来创建不同语言模型实例的工厂。
class LlmFactory:
    # 这个字典记录了不同的语言模型提供商和它们对应的类的字符串表示。
    provider_to_class = {
        "ollama": "mem0.llms.ollama.py.OllamaLLM",
        "openai": "mem0.llms.openai.OpenAILLM",
        "groq": "mem0.llms.groq.GroqLLM",
        "together": "mem0.llms.together.TogetherLLM",
        "aws_bedrock": "mem0.llms.aws_bedrock.AWSBedrockLLM",
        "litellm": "mem0.llms.litellm.LiteLLM",
    }

    # 这个方法是类的一个特殊方法，可以直接通过类名调用它，不需要创建实例。
    @classmethod
    def create(cls, provider_name, config):
        # 根据提供的提供商名称找到对应的类字符串。
        class_type = cls.provider_to_class.get(provider_name)
        # 如果找到了对应的类字符串，就继续执行。
        if class_type:
            # 通过 load_class 函数加载类。
            llm_instance = load_class(class_type)
            # 创建一个 BaseLlmConfig 类型的配置对象。
            base_config = BaseLlmConfig(**config)
            # 返回一个语言模型实例，传入配置信息。
            return llm_instance(base_config)
        # 如果没有找到对应的类字符串，就抛出错误。
        else:
            raise ValueError(f"Unsupported Llm provider: {provider_name}")
        
# 定义了一个叫做 EmbedderFactory 的类，它是用来创建不同嵌入器实例的工厂。
class EmbedderFactory:
    # 这个字典记录了不同的嵌入器提供商和它们对应的类的字符串表示。
    provider_to_class = {
        "openai": "mem0.embeddings.openai.OpenAIEmbedding",
        "ollama": "mem0.embeddings.ollama.OllamaEmbedding",
        "huggingface": "mem0.embeddings.huggingface.HuggingFaceEmbedding"
    }

    # 这个方法是类的一个特殊方法，可以直接通过类名调用它，不需要创建实例。
    @classmethod
    def create(cls, provider_name):
        # 根据提供的提供商名称找到对应的类字符串。
        class_type = cls.provider_to_class.get(provider_name)
        # 如果找到了对应的类字符串，就继续执行。
        if class_type:
            # 通过 load_class 函数加载类，并创建一个嵌入器实例。
            embedder_instance = load_class(class_type)()
            # 返回这个嵌入器实例。
            return embedder_instance
        # 如果没有找到对应的类字符串，就抛出错误。
        else:
            raise ValueError(f"Unsupported Embedder provider: {provider_name}")

