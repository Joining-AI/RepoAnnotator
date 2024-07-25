# 首先，我们从一个叫做abc的包里拿出了一个叫ABC的东西。
from abc import ABC
# 然后，我们从typing这个包里拿出了一个叫Optional的东西，它可以帮助我们处理可能不存在的信息。
from typing import Optional

# 下面，我们开始定义一个新类，名字叫做BaseLlmConfig，它是从ABC这个东西继承来的。
class BaseLlmConfig(ABC):
    # 这个类是专门用来设置大语言模型的一些配置的。
    """
    大语言模型的配置类。
    """

    # 接下来，我们定义了这个类的一个特别的方法，叫做__init__，这是类的构造器，当我们创建这个类的新实例时，它就会自动运行。
    def __init__(
        self,
        # 这里有四个可以设定的参数：
        model: Optional[str] = None,  # model参数是用来选择使用哪个模型的，如果没选，默认就是None。
        temperature: float = 0,       # temperature参数控制模型回答问题时的随机性。数字越大，答案越随机；数字越小，答案越确定。默认是0。
        max_tokens: int = 3000,       # max_tokens参数决定模型能生成多少字，这里用“字”代表模型输出的基本单位。默认是3000个字。
        top_p: float = 1              # top_p参数控制模型在选择词语时的多样性。数值越大，选择的词语种类越多。默认是1。
    ):
        # 下面这些代码是把上面设定的参数保存到类的属性中，这样我们就可以在类的其他地方使用它们了。
        self.model = model            # 把model参数保存到self.model属性里。
        self.temperature = temperature # 把temperature参数保存到self.temperature属性里。
        self.max_tokens = max_tokens  # 把max_tokens参数保存到self.max_tokens属性里。
        self.top_p = top_p            # 把top_p参数保存到self.top_p属性里。

