# 导入队列模块，用于在程序内部进行消息传递。
import queue

# 导入streamlit模块，这是一个用来创建交互式Web应用的Python库。
import streamlit as st

# 从embedchain库中导入App类，这是用来创建嵌入式应用程序的主要工具。
from embedchain import App

# 从embedchain.config模块中导入BaseLlmConfig类，这是配置语言模型的基础类。
from embedchain.config import BaseLlmConfig

# 从embedchain.helpers.callbacks模块中导入两个类：StreamingStdOutCallbackHandlerYield和generate函数，
# 这些是用来处理流式输出和生成答案的。
from embedchain.helpers.callbacks import (StreamingStdOutCallbackHandlerYield,
                                          generate)

# 使用Streamlit的缓存装饰器来缓存unacademy_ai函数的结果，这样如果再次调用此函数时，结果会被复用而不是重新计算。
@st.cache_resource
def unacademy_ai():
    # 创建一个新的App实例。
    app = App()
    # 返回创建好的App实例。
    return app

# 调用上面定义的unacademy_ai函数，并将返回的App实例赋值给变量app。
app = unacademy_ai()

# 设置助手头像的URL地址。
assistant_avatar_url = "https://cdn-images-1.medium.com/v2/resize:fit:1200/1*LdFNhpOe7uIn-bHK9VUinA.jpeg"

# 使用Markdown格式设置页面标题，并显示助手的头像。
st.markdown(f"# <img src='{assistant_avatar_url}' width={35} /> Unacademy UPSC AI", unsafe_allow_html=True)

# 定义一个样式化的说明文字，包含一些基本信息和链接。
styled_caption = """
<p style="font-size: 17px; color: #aaa;">
🚀 An <a href="https://github.com/embedchain/embedchain">Embedchain</a> app powered with Unacademy\'s UPSC data!
</p>
"""

# 在界面上显示这个说明文字。
st.markdown(styled_caption, unsafe_allow_html=True)

# 创建一个可展开的部分，里面包含了如何创建自己的Unacademy UPSC AI的说明。
with st.expander(":grey[Want to create your own Unacademy UPSC AI?]", expanded=False):
    # 写出创建自己AI的步骤和代码示例。
    st.write(
        """

