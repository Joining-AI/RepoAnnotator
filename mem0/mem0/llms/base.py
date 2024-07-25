# 引入一些特殊工具箱里的东西，让我们的代码可以做一些特别的事情。
from typing import Optional  # 这个工具帮助我们告诉别人，某个东西可能有，也可能没有。
from abc import ABC, abstractmethod  # 这些工具是魔术师的帽子，能让我们的类变成一种特殊的类，叫做抽象基类。

# 下面这个是从另一个地方拿来的配置文件的工具，就像从工具箱里拿出一个特定的螺丝刀。
from mem0.configs.llms.base import BaseLlmConfig

# 现在，我们要创造一个新的类，就像发明一个新的玩具，叫它LLMBase。它继承自魔术师的帽子（ABC）。
class LLMBase(ABC):

    # 这是创建新玩具时要做的事情，也就是构造函数。
    def __init__(self, config: Optional[BaseLlmConfig] = None):
        # 如果没有给玩具带上配置（config），我们就自己做一个默认的配置。
        if config is None:
            self.config = BaseLlmConfig()  # 这里我们用螺丝刀做了一个新的配置。
        else:
            self.config = config  # 如果有现成的配置，我们就直接用它。

    # 下面这个方法是个魔法门，只有继承这个类的其他类才能打开它，因为它是抽象的。
    @abstractmethod
    def generate_response(self, messages):
        # 这个魔法门的作用是根据给它的一堆消息（messages），生成一个回答（response）。
        # 消息是一串由“角色”和“内容”组成的字典列表。
        # 但是，我们现在还不知道具体怎么实现这个魔法，所以这里只是留下一个空壳子，写了个"pass"。
        pass

