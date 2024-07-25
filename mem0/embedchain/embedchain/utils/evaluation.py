# 首先，从一个叫做 "enum" 的工具箱里拿出一个叫 "Enum" 的工具。
from enum import Enum
# 再从一个叫做 "typing" 的工具箱里拿出一个叫 "Optional" 的工具。
from typing import Optional
# 接着从一个叫做 "pydantic" 的大盒子中拿出一个叫 "BaseModel" 的小盒子。
from pydantic import BaseModel

# 定义了一个名字叫做 "EvalMetric" 的新种类的东西，它是一个特殊的列表，里面放的是不会变的选项（用 "Enum" 工具做的）。
class EvalMetric(Enum):
    # 这个列表里的第一个选项叫做 "CONTEXT_RELEVANCY"，它代表了“上下文的相关性”。
    CONTEXT_RELEVANCY = "context_relevancy"
    # 第二个选项叫做 "ANSWER_RELEVANCY"，它代表了“答案的相关性”。
    ANSWER_RELEVANCY = "answer_relevancy"
    # 第三个选项叫做 "GROUNDEDNESS"，它代表了“依据充分性”。
    GROUNDEDNESS = "groundedness"

# 现在我们要做一个新的小盒子叫做 "EvalData"，这个小盒子继承自之前拿出来的 "BaseModel" 小盒子。
class EvalData(BaseModel):
    # 这个小盒子里要放的第一个东西叫做 "question"，它用来装问题的文字。
    question: str
    # 第二个东西叫做 "contexts"，它是一个列表，里面可以装很多字符串，这些字符串代表不同的上下文信息。
    contexts: list[str]
    # 第三个东西叫做 "answer"，它用来装答案的文字。
    answer: str
    # 最后一个东西叫做 "ground_truth"，它有时候会被用到，有时候不会。如果不用的话，它可以是空的。
    # 当前情况下我们还没有用到它。
    ground_truth: Optional[str] = None  # Not used as of now

