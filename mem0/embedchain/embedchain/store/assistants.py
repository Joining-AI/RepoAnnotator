# 这里我们导入了一些工具箱里的工具，它们能帮助我们完成一些任务。
import logging
import os
import re
import tempfile
import time
import uuid
from pathlib import Path
from typing import cast

# 下面这两行是从一个叫openai的大盒子里拿出我们需要的东西。
from openai import OpenAI
from openai.types.beta.threads import Message
from openai.types.beta.threads.text_content_block import TextContentBlock

# 这几行是从embedchain这个大盒子里拿出我们需要的一些小工具。
from embedchain import Client, Pipeline
from embedchain.config import AddConfig
from embedchain.data_formatter import DataFormatter
from embedchain.models.data_type import DataType
from embedchain.telemetry.posthog import AnonymousTelemetry
from embedchain.utils.misc import detect_datatype

# 这行代码是说，如果用户的文件夹还没建好，就帮他们建一个。
Client.setup()

# 定义一个名为 OpenAIAssistant 的类
class OpenAIAssistant:
    # 这个方法在创建类的实例时会被调用
    def __init__(self,
                 # 类实例的一些默认参数
                 name=None,
                 instructions=None,
                 tools=None,
                 thread_id=None,
                 model="gpt-4-1106-preview",
                 data_sources=None,
                 assistant_id=None,
                 log_level=logging.INFO,
                 collect_metrics=True):
        # 设置智能助手的名字，默认是 "OpenAI Assistant"
        self.name = name or "OpenAI Assistant"
        # 设置给智能助手的指令
        self.instructions = instructions
        # 设置智能助手可用的工具，默认只有一个检索工具
        self.tools = tools or [{"type": "retrieval"}]
        # 设置使用的模型，默认是 gpt-4-1106-preview
        self.model = model
        # 设置数据源列表，默认为空
        self.data_sources = data_sources or []
        # 设置日志级别
        self.log_level = log_level
        # 创建一个 OpenAI 客户端对象
        self._client = OpenAI()
        # 初始化智能助手
        self._initialize_assistant(assistant_id)
        # 如果没有给定线程 ID，则创建一个新的
        self.thread_id = thread_id or self._create_thread()
        # 创建一个字典来记录一些属性信息
        self._telemetry_props = {"class": self.__class__.__name__}
        # 创建一个匿名遥测对象，用于收集数据
        self.telemetry = AnonymousTelemetry(enabled=collect_metrics)
        # 记录初始化事件
        self.telemetry.capture(event_name="init", properties=self._telemetry_props)

    # 添加数据到智能助手的方法
    def add(self, source, data_type=None):
        # 准备数据源路径
        file_path = self._prepare_source_path(source, data_type)
        # 将文件添加到智能助手中
        self._add_file_to_assistant(file_path)
        
        # 记录添加数据的事件
        event_props = {
            **self._telemetry_props,
            "data_type": data_type or detect_datatype(source),
        }
        self.telemetry.capture(event_name="add", properties=event_props)
        # 输出一条信息，表示数据已经成功添加
        logging.info("Data successfully added to the assistant.")

    # 和智能助手聊天的方法
    def chat(self, message):
        # 发送消息
        self._send_message(message)
        # 记录聊天事件
        self.telemetry.capture(event_name="chat", properties=self._telemetry_props)
        # 获取最新的响应并返回
        return self._get_latest_response()

    # 删除线程的方法
    def delete_thread(self):
        # 删除当前线程
        self._client.beta.threads.delete(self.thread_id)
        # 创建新的线程
        self.thread_id = self._create_thread()

    # 内部方法：初始化智能助手
    def _initialize_assistant(self, assistant_id):
        # 生成文件 ID 列表
        file_ids = self._generate_file_ids(self.data_sources)
        # 根据提供的 ID 或者创建新的智能助手
        self.assistant = (
            self._client.beta.assistants.retrieve(assistant_id)
            if assistant_id
            else self._client.beta.assistants.create(
                name=self.name, model=self.model, file_ids=file_ids, instructions=self.instructions, tools=self.tools
            )
        )

    # 创建新线程的方法
    def _create_thread(self):
        # 创建新线程并返回它的 ID
        thread = self._client.beta.threads.create()
        return thread.id

    # 准备数据源路径的方法
    def _prepare_source_path(self, source, data_type=None):
        # 如果源是一个文件，则直接返回文件路径
        if Path(source).is_file():
            return source
        # 否则检测数据类型
        data_type = data_type or detect_datatype(source)
        # 使用数据格式化器处理数据
        formatter = DataFormatter(data_type=DataType(data_type), config=AddConfig())
        # 加载数据
        data = formatter.loader.load_data(source)["data"]
        # 保存临时数据
        return self._save_temp_data(data=data[0]["content"].encode(), source=source)

    # 将文件添加到智能助手的方法
    def _add_file_to_assistant(self, file_path):
        # 上传文件到 OpenAI
        file_obj = self._client.files.create(file=open(file_path, "rb"), purpose="assistants")
        # 将文件添加到智能助手中
        self._client.beta.assistants.files.create(assistant_id=self.assistant.id, file_id=file_obj.id)

    # 生成文件 ID 的方法
    def _generate_file_ids(self, data_sources):
        # 遍历数据源并生成文件 ID 列表
        return [
            self._add_file_to_assistant(self._prepare_source_path(ds["source"], ds.get("data_type")))
            for ds in data_sources
        ]

    # 发送消息的方法
    def _send_message(self, message):
        # 发送消息
        self._client.beta.threads.messages.create(thread_id=self.thread_id, role="user", content=message)
        # 等待响应完成
        self._wait_for_completion()

    # 等待响应完成的方法
    def _wait_for_completion(self):
        # 创建运行任务
        run = self._client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant.id,
            instructions=self.instructions,
        )
        # 获取运行任务的 ID 和状态
        run_id = run.id
        run_status = run.status

        # 循环等待直到任务完成
        while run_status in ["queued", "in_progress", "requires_action"]:
            # 每次请求之间休眠一小段时间以避免触发限速
            time.sleep(0.1)
            # 获取最新的运行状态
            run = self._client.beta.threads.runs.retrieve(thread_id=self.thread_id, run_id=run_id)
            run_status = run.status
            # 如果任务失败，则抛出异常
            if run_status == "failed":
                raise ValueError(f"Thread run failed with the following error: {run.last_error}")

    # 获取最新响应的方法
    def _get_latest_response(self):
        # 获取历史记录
        history = self._get_history()
        # 如果有历史记录，则格式化并返回最新的一条消息；否则返回 None
        return self._format_message(history[0]) if history else None

    # 获取历史记录的方法
    def _get_history(self):
        # 获取线程中的消息列表
        messages = self._client.beta.threads.messages.list(thread_id=self.thread_id, order="desc")
        # 返回消息列表
        return list(messages)

    # 格式化消息的方法
    @staticmethod
    def _format_message(thread_message):
        # 将消息转换为 Message 对象
        thread_message = cast(Message, thread_message)
        # 提取消息内容
        content = [c.text.value for c in thread_message.content if isinstance(c, TextContentBlock)]
        # 将所有文本内容合并成一个字符串
        return " ".join(content)

    # 保存临时数据的方法
    @staticmethod
    def _save_temp_data(data, source):
        # 替换文件名中的特殊字符
        special_chars_pattern = r'[\\/:*?"<>|&=% ]+'
        sanitized_source = re.sub(special_chars_pattern, "_", source)[:256]
        # 创建一个临时目录
        temp_dir = tempfile.mkdtemp()
        # 构建文件路径
        file_path = os.path.join(temp_dir, sanitized_source)
        # 写入数据到文件中
        with open(file_path, "wb") as file:
            file.write(data)
        # 返回文件路径
        return file_path

# 定义一个叫AIAssistant的类
class AIAssistant:

