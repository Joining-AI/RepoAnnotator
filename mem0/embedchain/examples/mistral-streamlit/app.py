# 导入需要的库，就像从工具箱里拿出你需要的工具。
import os
import streamlit as st
from embedchain import App

# 使用一个特殊的装饰器(@st.cache_resource)，它可以让我们的程序更高效，
# 当我们创建App对象时，如果之前已经创建过，就直接拿来用，不用再重新创建。
@st.cache_resource
def ec_app():
    # 创建一个Embedchain的应用实例，这个应用会读取一个叫"config.yaml"的配置文件。
    return App.from_config(config_path="config.yaml")

# 在侧边栏中，我们让用户输入他们的Hugging Face访问令牌，这是一个秘密码，用来访问一些特殊的功能。
# 我们还提供了一些链接，帮助用户获取和查看这个令牌。
with st.sidebar:
    huggingface_access_token = st.text_input("Hugging face Token", key="chatbot_api_key", type="password")
    "[Get Hugging Face Access Token](https://huggingface.co/settings/tokens)"
    "[View the source code](https://github.com/embedchain/examples/mistral-streamlit)"

# 设置页面标题和描述，让聊天机器人看起来更酷炫。
st.title("💬 Chatbot")
st.caption("🚀 An Embedchain app powered by Mistral!")

# 检查用户的会话状态，确保有消息记录，如果没有，就初始化一些默认的消息。
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """
        嗨！我是一个聊天机器人。我可以回答问题和学习新事物！\n
        问任何你想问的问题，如果你想让我学点什么，就发`/add <source>`。\n
        我几乎能学会所有东西。:)
        """
        }
    ]

# 显示聊天历史，把以前的对话显示出来。
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 等待用户输入，当用户在聊天框里打字并发送后，这段代码会被触发。
if prompt := st.chat_input("Ask me anything!"):
    # 如果用户没有输入Hugging Face的令牌，我们会提示他们输入。
    if not st.session_state.chatbot_api_key:
        st.error("请输入你的Hugging Face访问令牌")
        st.stop()

    # 把用户输入的令牌存到环境变量里，这样我们的程序就能使用它了。
    os.environ["HUGGINGFACE_ACCESS_TOKEN"] = st.session_state.chatbot_api_key
    app = ec_app()  # 获取或创建我们的Embedchain应用实例。

    # 如果用户输入以"/add"开始，这意味着他们想让我们学习一些新的知识。
    if prompt.startswith("/add"):
        # 先把用户的命令显示出来。
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 清除"/add"，留下实际要添加的知识内容。
        prompt = prompt.replace("/add", "").strip()
        
        # 显示正在学习的提示信息。
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("正在添加到知识库...")
            app.add(prompt)  # 让机器人学习新的知识。
            
            # 学习完成后，告诉用户我们已经添加了新的知识。
            message_placeholder.markdown(f"已将{prompt}添加到知识库！")
            st.session_state.messages.append({"role": "assistant", "content": f"已将{prompt}添加到知识库！"})
            st.stop()  # 学习完毕，结束本次操作。

    # 如果不是学习命令，那么就是普通的聊天了。
    with st.chat_message("user"):
        st.markdown(prompt)  # 显示用户的问题。
        st.session_state.messages.append({"role": "user", "content": prompt})  # 记录用户的问题。

    # 这里是机器人思考和回答的部分。
    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        msg_placeholder.markdown("思考中...")  # 显示思考中的动画或文字。
        full_response = ""  # 初始化机器人的回答为空字符串。

        # 循环获取机器人的回答，每次只获取一部分，然后拼接起来。
        for response in app.chat(prompt):
            msg_placeholder.empty()  # 清空之前的思考中提示。
            full_response += response  # 把机器人的回答加到full_response里。

        # 最终显示完整的回答。
        msg_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})  # 记录机器人的回答。

