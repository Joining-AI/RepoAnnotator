# 导入需要的库，就像是准备画画前挑选好颜料和画笔
import os
import queue
import re
import tempfile
import threading

import streamlit as st

from embedchain import App
from embedchain.config import BaseLlmConfig
from embedchain.helpers.callbacks import (StreamingStdOutCallbackHandlerYield,
                                          generate)

# 定义一个函数，用来创建一个聊天机器人，需要传入数据库路径和API密钥
def embedchain_bot(db_path, api_key):
    # 使用传入的配置信息来初始化一个聊天机器人
    return App.from_config(
        # 配置信息，告诉机器人如何工作
        config={
            # LLM（语言模型）的设置，这里用的是OpenAI的GPT-3.5模型
            "llm": {
                "provider": "openai",  # 使用OpenAI作为语言模型的提供者
                "config": {
                    "model": "gpt-3.5-turbo-1106",  # 指定使用的模型版本
                    "temperature": 0.5,  # 控制回答的随机性
                    "max_tokens": 1000,  # 最大回答长度
                    "top_p": 1,  # 控制回答的多样性
                    "stream": True,  # 是否流式传输回答
                    "api_key": api_key,  # OpenAI的API密钥
                },
            },
            # 向量数据库的设置，用于存储和检索信息
            "vectordb": {
                "provider": "chroma",  # 使用Chroma作为向量数据库
                "config": {
                    "collection_name": "chat-pdf",  # 数据集名称
                    "dir": db_path,  # 数据库路径
                    "allow_reset": True,  # 允许重置数据库
                },
            },
            # 嵌入器的设置，用于将文本转换成向量
            "embedder": {"provider": "openai", "config": {"api_key": api_key}},  # 使用OpenAI的嵌入器
            # 分块器的设置，用于将长文本分割成小块
            "chunker": {"chunk_size": 2000, "chunk_overlap": 0, "length_function": "len"},  # 分块大小、重叠部分、长度计算方式
        }
    )

# 定义一个函数，用来获取数据库的临时路径
def get_db_path():
    # 创建一个临时目录
    tmpdirname = tempfile.mkdtemp()
    # 返回这个临时目录的路径
    return tmpdirname

# 定义一个函数，用来获取或创建聊天机器人实例
def get_ec_app(api_key):
    # 如果session_state中已经有聊天机器人实例了
    if "app" in st.session_state:
        print("找到了session_state中的聊天机器人")  # 打印一条消息
        app = st.session_state.app  # 直接从session_state中获取
    else:  # 如果session_state中没有聊天机器人实例
        print("正在创建新的聊天机器人")  # 打印一条消息
        # 调用get_db_path()函数获取数据库路径
        db_path = get_db_path()
        # 调用embedchain_bot()函数创建聊天机器人实例
        app = embedchain_bot(db_path, api_key)
        # 将新创建的聊天机器人实例存入session_state
        st.session_state.app = app
    # 返回聊天机器人实例
    return app

# 这里是在侧边栏里做的一些事情
with st.sidebar:
    # 这行代码让用户输入他们的OpenAI API密钥，并保存在一个叫做openai_access_token的变量中。
    # 用户输入的信息会被隐藏起来，因为类型设置为"密码"。
    openai_access_token = st.text_input("OpenAI API Key", key="api_key", type="password")
    # 这两行告诉用户我们不会保存他们的API密钥，并告诉他们如何获取API密钥。
    "WE DO NOT STORE YOUR OPENAI KEY."
    "Just paste your OpenAI API key here and we'll use it to power the chatbot. [Get your OpenAI API key](https://platform.openai.com/api-keys)"  # noqa: E501

    # 如果用户已经输入了API密钥并保存在session_state里，那么就用这个密钥创建一个应用实例。
    if st.session_state.api_key:
        app = get_ec_app(st.session_state.api_key)

# 让用户上传PDF文件
pdf_files = st.file_uploader("Upload your PDF files", accept_multiple_files=True, type="pdf")
# 获取之前添加过的PDF文件名列表
add_pdf_files = st.session_state.get("add_pdf_files", [])

# 遍历用户上传的所有PDF文件
for pdf_file in pdf_files:
    # 获取文件名
    file_name = pdf_file.name
    # 如果这个文件已经被添加过了，就不需要再次处理
    if file_name in add_pdf_files:
        continue
    try:
        # 检查用户是否已经输入了API密钥
        if not st.session_state.api_key:
            # 如果没有输入密钥，显示错误信息并停止程序执行
            st.error("Please enter your OpenAI API Key")
            st.stop()
        # 创建一个临时文件，用于存储上传的PDF文件
        temp_file_name = None
        with tempfile.NamedTemporaryFile(mode="wb", delete=False, prefix=file_name, suffix=".pdf") as f:
            # 把PDF文件内容写入临时文件
            f.write(pdf_file.getvalue())
            temp_file_name = f.name
        # 如果临时文件创建成功
        if temp_file_name:
            # 显示正在把文件加入知识库的消息
            st.markdown(f"Adding {file_name} to knowledge base...")
            # 把临时文件添加到应用的知识库中
            app.add(temp_file_name, data_type="pdf_file")
            # 清空一下显示区域
            st.markdown("")
            # 把文件名添加到已处理的文件列表中
            add_pdf_files.append(file_name)
            # 删除临时文件
            os.remove(temp_file_name)
        # 显示文件已成功添加到知识库的消息
        st.session_state.messages.append({"role": "assistant", "content": f"Added {file_name} to knowledge base!"})
    # 如果出现异常，显示错误信息并停止程序执行
    except Exception as e:
        st.error(f"Error adding {file_name} to knowledge base: {e}")
        st.stop()
# 更新已处理的PDF文件列表
st.session_state["add_pdf_files"] = add_pdf_files

# 设置网页标题
st.title("📄 Embedchain - Chat with PDF")
# 设置一个好看的介绍文字
styled_caption = '<p style="font-size: 17px; color: #aaa;">🚀 An <a href="https://github.com/embedchain/embedchain">Embedchain</a> app powered by OpenAI!</p>'  # noqa: E501
st.markdown(styled_caption, unsafe_allow_html=True)

# 如果messages还没有在session_state中，就初始化它
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """
                Hi! I'm chatbot powered by Embedchain, which can answer questions about your pdf documents.\n
                Upload your pdf documents here and I'll answer your questions about them! 
            """,
        }
    ]

# 遍历消息列表并显示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 如果用户输入了一个问题
if prompt := st.chat_input("Ask me anything!"):
    # 检查用户是否已经输入了API密钥
    if not st.session_state.api_key:
        # 如果没有输入密钥，显示错误信息并停止程序执行
        st.error("Please enter your OpenAI API Key", icon="🤖")
        st.stop()

    # 使用用户的API密钥创建一个应用实例
    app = get_ec_app(st.session_state.api_key)

    # 显示用户的问题
    with st.chat_message("user"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.markdown(prompt)

    # 显示机器人的回答
    with st.chat_message("assistant"):
        # 先预留一个位置显示机器人正在思考
        msg_placeholder = st.empty()
        msg_placeholder.markdown("Thinking...")
        # 初始化一个空的回答
        full_response = ""

        # 定义一个队列，用于接收回答的片段
        q = queue.Queue()

        # 定义一个函数，让应用生成回答和引用来源
        def app_response(result):
            # 获得配置信息
            llm_config = app.llm.config.as_dict()
            # 设置回调函数，用于获取实时的回答片段
            llm_config["callbacks"] = [StreamingStdOutCallbackHandlerYield(q=q)]
            config = BaseLlmConfig(**llm_config)
            # 获取回答和引用来源
            answer, citations = app.chat(prompt, config=config, citations=True)
            # 把结果保存到字典中
            result["answer"] = answer
            result["citations"] = citations

        # 创建一个字典来保存结果
        results = {}
        # 创建一个线程来异步获取回答
        thread = threading.Thread(target=app_response, args=(results,))
        thread.start()

        # 从队列中获取回答的片段，并逐步显示
        for answer_chunk in generate(q):
            full_response += answer_chunk
            msg_placeholder.markdown(full_response)

        # 等待线程结束
        thread.join()
        # 从结果字典中获取最终的回答和引用来源
        answer, citations = results["answer"], results["citations"]
        # 如果有引用来源，就加上来源信息
        if citations:
            full_response += "\n\n**Sources**:\n"
            sources = []
            for i, citation in enumerate(citations):
                source = citation[1]["url"]
                # 从URL中提取文件名
                pattern = re.compile(r"([^/]+)\.[^\.]+\.pdf$")
                match = pattern.search(source)
                if match:
                    source = match.group(1) + ".pdf"
                sources.append(source)
            # 去除重复的文件名
            sources = list(set(sources))
            # 显示所有来源的文件名
            for source in sources:
                full_response += f"- {source}\n"

        # 显示最终的回答
        msg_placeholder.markdown(full_response)
        # 打印回答，方便开发者查看
        print("Answer: ", full_response)
        # 把回答保存到session_state中
        st.session_state.messages.append({"role": "assistant", "content": full_response})

