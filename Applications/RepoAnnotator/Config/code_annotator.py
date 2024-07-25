import re

data_template=f'''
=start_pad= annotated_code_lines_here =end_pad=

记得在注释代码部分的开头和结尾保留=start_pad= 和 =end_pad=
'''

prompt='''
你是一个聪明的代码助手，你的工作是在不破坏代码功能的同时，为代码添加详细的注释，便于人们的理解。
请你为我解释下面的代码，逐行中文注释，并且不许减少一行代码。

接下来是正式的任务：
--------------------------------------------------------------------------------
请根据给定的代码片段，添加逐行详细的中文注释。
对于这一段代码:

{input_1}

我希望你识别出它所涉及到的主题，并且采用下面的格式回复：

{data_template}
'''

def validation(data):
    # 将数据转换为小写以确保兼容大小写
    data_lower = data.lower()
    start_pad = "=start_pad="
    end_pad = "=end_pad="
    
    # 找到 =start_pad= 和 =end_pad= 的位置
    start_index = data_lower.find(start_pad)
    end_index = data_lower.rfind(end_pad)
    
    # 验证 =start_pad= 和 =end_pad= 是否存在且顺序正确
    if start_index == -1 or end_index == -1 or start_index >= end_index:
        return False

    # 验证 =start_pad= 和 =end_pad= 之间是否有内容
    content_between = data[start_index + len(start_pad):end_index].strip()
    if not content_between:
        return False

    # 验证 =start_pad= 和 =end_pad= 是否在注释代码部分的开头和结尾
    pattern = re.compile(rf'{re.escape(start_pad)}.*?{re.escape(end_pad)}', re.DOTALL)
    if not pattern.search(data_lower):
        return False
    
    return True

correction='''
下列内容中含有一个错误的数据格式：

{answer}

请你修改它，使其符合以下格式：

{data_template}
'''
