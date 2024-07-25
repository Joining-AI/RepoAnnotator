import os
import random
from dotenv import load_dotenv, find_dotenv
from http import HTTPStatus
from pathlib import Path
import dashscope
import requests
import json
from openai import OpenAI

class QwenService:
    def __init__(self, version='long'):
        # 加载当前目录的.env文件
        load_dotenv()
        
        self.version = 'qwen-' + version
        self.client = None
        self.initialized = False
        self.input_tokens = 0  # 输入字数
        self.output_tokens = 0  # 输出字数
        self.stream = False  # 默认不使用stream模式
        # 获取项目根目录
        self.project_root = os.getenv('PROJECT_ROOT')
        if not self.project_root:
            # 如果 PROJECT_ROOT 环境变量不存在，查找 .env 文件，并以其所在目录为根目录
            env_path = find_dotenv()
            if env_path:
                self.project_root = os.path.dirname(env_path)
            else:
                raise FileNotFoundError(".env 文件未找到，且未设置 PROJECT_ROOT 环境变量。")
        
        # 获取 JSON 文件的路径
        self.price_json_file_path = os.path.join(self.project_root, 'Data', 'Qwen','qwen_price.json')
        self.error_json_file_path = os.path.join(self.project_root, 'Data', 'Qwen', 'qwen_error.json')
     
        # 从环境变量中导入API密钥并初始化服务
        api_key = os.getenv('QWEN_API', None)
        if api_key:
            try:
                dashscope.api_key = api_key
                self.client = dashscope.Generation()
                self.initialized = True
                print("服务初始化成功")
            except Exception as e:
                print(f"初始化服务失败: {e}")
                self.initialized = False
        else:
            raise ValueError("API密钥未在环境变量中设置")
        
    def ask(self, prompt: str, language='中文', stream: bool = None) -> str:
        if not self.initialized:
            raise RuntimeError("服务未初始化")
        
        if stream is None:
            stream = self.stream
        try:
            # 计算输入字数
            self.input_tokens += len(prompt)
            
            # 确保将请求格式化为正确的消息格式
            messages = [{'role': 'system', 'content': f'你是一个忠实细致的助手，你的输出应该使用{language}'},
                        {'role': 'user', 'content': prompt}]
            
            if stream:
                client = OpenAI(
                    api_key=os.getenv('QWEN_API'),
                    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
                )
                
                completion = client.chat.completions.create(
                    model=self.version,
                    messages=messages,
                    stream=True
                )
                
                output_content = ""
                for chunk in completion:
                    if chunk.choices[0].delta.content is not None:
                        chunk_content = chunk.choices[0].delta.content
                        output_content += chunk_content
                        # 打印输出以模拟实时渲染
                        print(chunk_content, end='', flush=True)
                
                self.output_tokens += len(output_content)
                return output_content
            
            else:
                resp = self.client.call(model=self.version, messages=messages, seed=random.randint(1, 10000), result_format='message')

                if resp.status_code == HTTPStatus.OK:
                    output_content = ""
                    if hasattr(resp, 'output') and 'choices' in resp.output:
                        choices = resp.output['choices']
                        if choices and 'message' in choices[0] and 'content' in choices[0]['message']:
                            output_content = choices[0]['message']['content']
                            # 从usage中读取tokens使用情况
                            self.input_tokens += resp.usage['input_tokens']
                            self.output_tokens += resp.usage['output_tokens']
                        else:
                            output_content = "未找到有效的响应内容"
                            self.output_tokens += len(output_content)
                    else:
                        output_content = "响应中不包含choices"
                        self.output_tokens += len(output_content)
                    return output_content
                else:
                    return f"请求失败: {resp.code} - {resp.message}"
        except Exception as e:
            return f"请求过程中发生错误: {e}"
        
    def ask_file(self, file_path: str, prompt: str, language='中文') -> str:
        if not self.initialized:
            raise RuntimeError("服务未初始化")

        file_id = None
        try:
            client = OpenAI(
                api_key=os.getenv('QWEN_API'),
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
            
            file = client.files.create(file=Path(file_path), purpose="file-extract")
            file_id = file.id
            
            messages = [
                {'role': 'system', 'content': f'你是一个忠实细致的助手，你的输出应该使用{language}'},
                {'role': 'system', 'content': f'fileid://{file.id}'},
                {'role': 'user', 'content': prompt}
            ]
            
            completion = client.chat.completions.create(
                model=self.version,
                messages=messages,
                stream=False
            )
            
            # 确保正确解析返回内容
            if completion.choices and completion.choices[0].message and completion.choices[0].message.content:
                output_content = completion.choices[0].message.content
                # 从usage中读取tokens使用情况
                self.input_tokens += completion.usage['input_tokens']
                self.output_tokens += completion.usage['output_tokens']
                
                # 删除云文件
                self.delete_file(file_id)
                
                return output_content
            else:
                print(completion)
                self.delete_file(file_id)
                return "未找到有效的响应内容"
                
        except Exception as e:
            if file_id:
                self.delete_file(file_id)
            return f"请求过程中发生错误: {e}"
        
    # 完备
    def list_files(self):
        """列出当前所有云文件的ID"""
        if not self.initialized:
            raise RuntimeError("服务未初始化")

        try:
            client = OpenAI(
                api_key=os.getenv('QWEN_API'),
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
            
            files = client.files.list()
            file_ids = [file.id for file in files.data]
            return file_ids
            
        except Exception as e:
            return f"获取文件列表时发生错误: {e}"
        
    # 完备
    def delete_file(self, file_id: str):
        """删除指定的云文件ID"""
        if not self.initialized:
            raise RuntimeError("服务未初始化")

        try:
            client = OpenAI(
                api_key=os.getenv('QWEN_API'),
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
            
            client.files.delete(file_id)
            return f"文件 {file_id} 已删除"
            
        except Exception as e:
            return f"删除文件时发生错误: {e}"

    # 完备
    def clear_all_files(self):
        """一键清空所有云文件"""
        if not self.initialized:
            raise RuntimeError("服务未初始化")

        try:
            client = OpenAI(
                api_key=os.getenv('QWEN_API'),
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
            
            files = client.files.list()
            for file in files.data:
                client.files.delete(file.id)
                print("已删除文件: ", file.id)
            
            return "所有文件已删除"
            
        except Exception as e:
            return f"清空文件时发生错误: {e}"
   
    def show_model_info(self):
        # 读取并打印 qwen_price.json 文件内容
        self._print_json_file(self.price_json_file_path, "价格信息")

    def show_error_info(self):
        # 读取并打印 qwen_error.json 文件内容
        self._print_error_json_file(self.error_json_file_path, "错误信息")

    def _print_json_file(self, file_path, title):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                name_list = data.get("name_list", [])
                print("API 价格信息：\n")
                
                for name in name_list:
                    api_info = data.get(name, {})
                    input_price = api_info.get("input_price", "N/A")
                    output_price = api_info.get("output_price", "N/A")
                    print(f"API种类: {name}")
                    print(f"  输入价格: {input_price*1000000} 元/百万token")
                    print(f"  输出价格: {output_price*1000000} 元/百万token\n")
        
        except FileNotFoundError:
            print(f"文件 {file_path} 未找到。")
        except json.JSONDecodeError:
            print(f"文件 {file_path} 不是一个有效的 JSON 文件。")

    def _print_error_json_file(self, file_path, title):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                print(f"API {title}：\n")
                
                for error_code, errors in data.items():
                    for sub_key, message in errors.items():
                        print(f"错误代码: {error_code} - {sub_key}")
                        print(f"  错误信息: {message}\n")
        
        except FileNotFoundError:
            print(f"文件 {file_path} 未找到。")
        except json.JSONDecodeError:
            print(f"文件 {file_path} 不是一个有效的 JSON 文件。")
