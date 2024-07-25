# 这一行代码的意思是：从名为 "answer_relevancy" 的模块里面导入一个叫做 "AnswerRelevance" 的东西。
# 这就像如果你有一个装满玩具的盒子，然后你说“我要从这个盒子里拿出我的超级英雄玩偶”。
# 但是最后的 "# noqa: F401" 这部分是告诉大人的（编译器或解释器），说：“嘿，我知道我没用到这个超级英雄玩偶，
# 但我是有原因拿它的，所以别提醒我。”
from .answer_relevancy import AnswerRelevance  # noqa: F401

# 下面这一行也是做类似的事情，从 "context_relevancy" 这个模块里取出 "ContextRelevance" 这个东西。
# 同样地，“# noqa: F401” 是告诉大人：“我知道我现在没用它，但我之后会用到的，所以别提醒我。”
from .context_relevancy import ContextRelevance  # noqa: F401

# 最后这一行是从 "groundedness" 这个模块里取出 "Groundedness" 这个东西。
# “# noqa: F401” 还是一样的意思：“我知道我现在没用它，但我之后会用到的，所以别提醒我。”
from .groundedness import Groundedness  # noqa: F401

