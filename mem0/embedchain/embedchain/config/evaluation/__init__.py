# 从 base 这个模块里导入几个类
# 我们就像是从一个盒子里拿出我们需要的东西一样
from .base import (  # 从当前文件夹下的 base 模块里拿东西
    AnswerRelevanceConfig,  # 拿出“答案相关性配置”这个工具
    ContextRelevanceConfig,  # 拿出“上下文相关性配置”这个工具
    # 下面这行的 #noqa: F401 是告诉检查代码的人：“这里多拿了一个工具，但不用担心，这是有原因的”
    GroundednessConfig  # 拿出“依据性配置”这个工具
)

