# 这里我们首先告诉电脑我们需要用到的工具箱里的工具，第一个是Streamlit，它帮助我们在网页上显示东西。
import streamlit as st

# 第二个工具是embedchain，这是一个智能助手，可以帮助我们回答问题和学习新知识。
from embedchain import App


# 这是一个魔法咒语，告诉电脑我们要创建一个智能助手，但是我们只在需要的时候才去创造它，这样可以节省资源。
@st.cache_resource
def embedchain_bot():
    # 创建并返回我们的智能助手。
    return App()


# 在网页上写了一个大标题，就像书的封面一样，上面写着“聊天机器人”。
st.title("💬 Chatbot")

# 然后在下面写了一小段说明，告诉人们这个聊天机器人是由Embedchain和OpenAI共同打造的，就像超级英雄团队一样。
st.caption("🚀 An Embedchain app powered by OpenAI!")

# 这里我们检查电脑的记忆里是否已经有了和用户聊天的历史记录，如果没有，我们就给它准备一段欢迎词。
if "messages" not in st.session_state:
    # 我们把欢迎词放在一个列表里，就像故事书的第一页。
    st.session_state.messages = [
        {
            # 这是机器人说的第一句话，介绍自己并告诉用户它可以做什么。
            "role": "assistant",
            "content": """
        Hi! I'm a chatbot. I can answer questions and learn new things!\n
        Ask me anything and if you want me to learn something do `/add <source>`.\n
        I can learn mostly everything. :)
        """,
        }
    ]

# 接下来，我们让电脑把之前的所有对话都显示出来，就像翻阅故事书的每一页。
for message in st.session_state.messages:
    # 每条消息都有自己的气泡，我们根据发送者（用户或机器人）来改变气泡的样子。
    with st.chat_message(message["role"]):
        # 然后我们把消息内容写在气泡里。
        st.markdown(message["content"])

# 如果用户在聊天框里输入了问题或命令，我们就开始处理。
if prompt := st.chat_input("Ask me anything!"):
    # 我们再次召唤出我们的智能助手。
    app = embedchain_bot()

    # 如果用户输入的是学习命令，我们先把它显示出来，然后告诉用户我们正在添加新知识。
    if prompt.startswith("/add"):
        with st.chat_message("user"):
            # 显示用户的命令。
            st.markdown(prompt)
            # 把用户的命令保存到历史记录中。
            st.session_state.messages.append({"role": "user", "content": prompt})
        # 去掉命令前缀，得到要学习的内容。
        prompt = prompt.replace("/add", "").strip()
        # 显示正在添加新知识的信息。
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Adding to knowledge base...")
            # 让智能助手学习新知识。
            app.add(prompt)
            # 显示添加成功的信息。
            message_placeholder.markdown(f"Added {prompt} to knowledge base!")
            # 把添加成功的消息保存到历史记录中。
            st.session_state.messages.append({"role": "assistant", "content": f"Added {prompt} to knowledge base!"})
            # 停止执行后面的代码，因为任务已经完成。
            st.stop()

    # 如果不是学习命令，那就是普通的问题。
    with st.chat_message("user"):
        # 显示用户的问题。
        st.markdown(prompt)
        # 把用户的问题保存到历史记录中。
        st.session_state.messages.append({"role": "user", "content": prompt})

    # 现在轮到我们的智能助手思考并回答问题了。
    with st.chat_message("assistant"):
        # 先显示一个占位符，告诉用户智能助手正在思考。
        msg_placeholder = st.empty()
        msg_placeholder.markdown("Thinking...")
        # 初始时，完整的回答还是空的。
        full_response = ""

        # 智能助手开始逐字生成回答。
        for response in app.chat(prompt):
            # 清除之前的占位符，因为我们要更新显示。
            msg_placeholder.empty()
            # 把智能助手每次生成的一小段回答加到完整回答里。
            full_response += response

        # 最后，显示完整的回答。
        msg_placeholder.markdown(full_response)
        # 把机器人的回答保存到历史记录中。
        st.session_state.messages.append({"role": "assistant", "content": full_response})

