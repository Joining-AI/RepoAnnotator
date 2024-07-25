# 引入typing库中的Optional类，这个类可以帮助我们定义变量可以是某种类型，也可以是None。
from typing import Optional

# 引入pydantic库中的BaseModel、Field和field_validator类。这些类帮助我们创建数据模型，确保数据格式正确。
from pydantic import BaseModel, Field, field_validator

# 定义一个名为LlmConfig的类，它继承自BaseModel，这意味着它是一个数据模型。
class LlmConfig(BaseModel):
    # 定义一个名为provider的属性，它的类型是字符串（str），默认值是"openai"。
    # 这个属性描述了大语言模型（LLM）的提供商，比如"ollama"或"openai"。
    provider: str = Field(
        # 这里是对这个属性的描述，告诉人们它代表什么。
        description="Provider of the LLM (e.g., 'ollama', 'openai')",
        # 默认情况下，如果没有提供值，那么它的值就是"openai"。
        default="openai"
    )
    # 定义一个名为config的属性，它的类型可以是字典(dict)或者None（没有值）。
    # 这个属性是用来存放特定LLM配置信息的。
    config: Optional[dict] = Field(
        # 描述这个属性的作用，告诉人们它用来做什么。
        description="Configuration for the specific LLM",
        # 默认情况下，如果没有提供值，那么它的值就是一个空字典{}。
        default={}
    )

    # 定义一个名为validate_config的方法，它会验证config属性的值是否合适。
    # 这个方法会自动在config属性被设置时运行。
    @field_validator("config")
    def validate_config(cls, v, values):
        # 首先，从数据中获取provider的值，也就是LLM的提供商是谁。
        provider = values.data.get("provider")
        # 检查provider的值是否是我们支持的提供商之一（openai, ollama, groq, together, aws_bedrock, litellm）。
        if provider in ("openai", "ollama", "groq", "together", "aws_bedrock", "litellm"):
            # 如果是支持的提供商，那么就直接返回config的值，表示验证通过。
            return v
        else:
            # 如果不是支持的提供商，那么就抛出一个错误，告诉人们不支持这个提供商。
            raise ValueError(f"Unsupported LLM provider: {provider}")

