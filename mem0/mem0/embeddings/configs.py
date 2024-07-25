# 导入一些我们需要的工具
from typing import Optional
# 这里我们从typing库中导入了Optional这个工具，它在定义变量时可以指定变量可以是某种类型或者None。

from pydantic import BaseModel, Field, field_validator
# 我们从pydantic库中导入了三个工具：BaseModel、Field和field_validator。
# BaseModel是用来创建数据模型的基础类；
# Field是用来给模型字段添加额外信息（比如描述或默认值）的；
# field_validator是用来校验字段数据是否合法的。

# 定义了一个名为EmbedderConfig的类，继承自BaseModel
class EmbedderConfig(BaseModel):
    # 这里开始定义EmbedderConfig这个类，它会用来存储和验证嵌入模型的配置信息。

    provider: str = Field(  # 定义一个名为provider的字段，类型为字符串
        description="Provider of the embedding model (e.g., 'ollama', 'openai')",  # 描述这个字段的作用
        default="openai",  # 设置默认值为'openai'
    )
    # 这行代码创建了一个字段叫provider，它用于存储提供嵌入模型的服务商的名字，
    # 比如它可以是'ollama'或'openai'。如果没有给出这个字段的值，那么默认就是'openai'。

    config: Optional[dict] = Field(  # 定义一个名为config的字段，类型为字典或者None
        description="Configuration for the specific embedding model",  # 描述这个字段的作用
        default=None  # 设置默认值为None
    )
    # 这行代码创建了一个字段叫config，它用于存储特定嵌入模型的详细配置信息，
    # 这个字段可以是一个字典也可以是None。如果没有给出这个字段的值，那么默认就是None。

    @field_validator("config")  # 定义一个校验器，专门检查config字段
    def validate_config(cls, v, values):  # 校验器的函数名和参数
        provider = values.data.get("provider")  # 从values数据中获取provider的值
        # 这里我们先从传入的values数据中找到provider的值，因为我们要根据不同的provider来决定是否接受config的值。

        if provider in ["openai", "ollama"]:  # 检查provider是否是openai或ollama
            return v  # 如果是，就直接返回config的值，表示它是有效的
        else:
            raise ValueError(f"Unsupported embedding provider: {provider}")  # 如果不是，抛出错误，表示不支持这个provider
    # 这段代码的意思是，如果provider是'openai'或'ollama'中的一个，那么config的值就是有效的；
    # 否则，就会抛出一个错误，告诉用户不支持他们提供的那个服务商。

