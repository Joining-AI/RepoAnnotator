# 定义一个函数，名字叫 generate_error_message_for_api_keys
def generate_error_message_for_api_keys(error: ValueError) -> str:
    # 创建一个字典，里面存放了一些环境变量的名字和它们对应的别名
    env_mapping = {
        "OPENAI_API_KEY": "OPENAI_API_KEY",       # 这是 OpenAI 的 API 密钥
        "OPENAI_API_TYPE": "OPENAI_API_TYPE",     # 这是 OpenAI 的 API 类型
        "OPENAI_API_BASE": "OPENAI_API_BASE",     # 这是 OpenAI 的 API 基础地址
        "OPENAI_API_VERSION": "OPENAI_API_VERSION", # 这是 OpenAI 的 API 版本
        "COHERE_API_KEY": "COHERE_API_KEY",       # 这是 Cohere 的 API 密钥
        "TOGETHER_API_KEY": "TOGETHER_API_KEY",   # 这是 Together 的 API 密钥
        "ANTHROPIC_API_KEY": "ANTHROPIC_API_KEY", # 这是 Anthropic 的 API 密钥
        "JINACHAT_API_KEY": "JINACHAT_API_KEY",   # 这是 Jinachat 的 API 密钥
        "HUGGINGFACE_ACCESS_TOKEN": "HUGGINGFACE_ACCESS_TOKEN", # 这是 Hugging Face 的访问令牌
        "REPLICATE_API_TOKEN": "REPLICATE_API_TOKEN", # 这是 Replicate 的 API 令牌
    }

    # 使用列表推导式创建一个新的列表，这个列表包含了在错误信息中提到的所有环境变量的别名
    missing_keys = [env_mapping[key] for key in env_mapping if key in str(error)]
    
    # 如果 missing_keys 列表不是空的，也就是说找到了一些缺失的环境变量
    if missing_keys:
        # 把找到的缺失环境变量别名连接成一个字符串，中间用逗号和空格隔开
        missing_keys_str = ", ".join(missing_keys)
        
        # 返回一个提示信息，告诉用户需要设置哪些环境变量，并给出一个例子说明怎么设置
        return f"""请在运行 Docker 容器的时候设置这些环境变量：{missing_keys_str}。
例如：`docker run -e {missing_keys[0]}=xxx embedchain/rest-api:latest` 
"""
    else:
        # 如果没有找到任何缺失的环境变量，就直接返回原始的错误信息
        return "错误: " + str(error)

