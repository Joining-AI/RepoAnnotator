# 首先，我们从一个叫做embedchain的程序里，找到一个名叫app的部分，
# 然后在app这个部分里面，我们又找到了一个叫做App的东西。
from embedchain.app import App

# 下面，我们开始定义一个新的班级，名字叫做Pipeline，这个班级其实继承自上面提到的App班级。
# 就像是Pipeline这个班级的学生可以学习到App班级的所有课程一样。
class Pipeline(App):

    # 在Pipeline这个班级的介绍里，我们写着这样一句话：
    # "这个班级已经过时了，大家应该去学习App这个班级。"
    # 这就像是告诉别人，Pipeline这个班级不再教新的东西了，想学新知识的同学应该去App班级。
    """
    This is deprecated. Use `App` instead.
    """

    # 这个pass就像是说：“这个班级现在没有额外的课程安排。”
    # 意思是Pipeline班级除了继承App班级的内容外，自己没有添加新的课程。
    pass

