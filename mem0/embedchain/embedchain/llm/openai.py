# 定义了一个叫做 OpenAILlm 的类，这个类继承自 BaseLlm。
class OpenAILlm(BaseLlm):
    # 这是 OpenAILlm 类的构造函数（就是创建这个类的对象时会自动运行的函数）。
    def __init__(
        self,
        # 这个函数接受两个参数，一个是配置信息（可选），另一个是工具（可选）。
        config: Optional[BaseLlmConfig] = None,
        tools: Optional[Union[Dict[str, Any], Type[BaseModel], Callable[..., Any], BaseTool]] = None,
    ):
        # 把传进来的工具保存在 self.tools 里，这样我们可以在其他地方用到它。
        self.tools = tools
        # 调用父类 BaseLlm 的构造函数，并传递配置信息给它。
        super().__init__(config=config)

    # 这个函数用来获取模型的回答，并计算花费。
    def get_llm_model_answer(self, prompt) -> tuple[str, Optional[dict[str, Any]]]:
        # 如果配置里面打开了计费功能。
        if self.config.token_usage:
            # 先调用一个内部函数获取回答和令牌信息。
            response, token_info = self._get_answer(prompt, self.config)
            # 拼接模型的名字。
            model_name = "openai/" + self.config.model
            # 如果模型名字不在定价表里面，就抛出错误提示用户。
            if model_name not in self.config.model_pricing_map:
                raise ValueError(
                    f"Model {model_name} not found in `model_prices_and_context_window.json`. \
                    You can disable token usage by setting `token_usage` to False."
                )
            # 计算总花费：输入令牌乘以单价加上输出令牌乘以单价。
            total_cost = (
                self.config.model_pricing_map[model_name]["input_cost_per_token"] * token_info["prompt_tokens"]
            ) + self.config.model_pricing_map[model_name]["output_cost_per_token"] * token_info["completion_tokens"]
            # 把花费信息整理成字典形式。
            response_token_info = {
                "prompt_tokens": token_info["prompt_tokens"],
                "completion_tokens": token_info["completion_tokens"],
                "total_tokens": token_info["prompt_tokens"] + token_info["completion_tokens"],
                "total_cost": round(total_cost, 10),
                "cost_currency": "USD",
            }
            # 返回回答内容和花费信息。
            return response, response_token_info

        # 如果没有打开计费功能，直接返回回答。
        return self._get_answer(prompt, self.config)

    # 这个内部函数用来获取模型的回答。
    def _get_answer(self, prompt: str, config: BaseLlmConfig) -> str:
        # 创建一个空列表，用来存放对话信息。
        messages = []
        # 如果配置中有系统提示，先添加一条系统消息。
        if config.system_prompt:
            messages.append(SystemMessage(content=config.system_prompt))
        # 再添加一条人类的消息，就是我们的提问。
        messages.append(HumanMessage(content=prompt))
        # 设置调用模型所需的参数。
        kwargs = {
            "model": config.model or "gpt-3.5-turbo",  # 使用配置中的模型名，如果没有就用 gpt-3.5-turbo。
            "temperature": config.temperature,  # 温度值，控制随机性。
            "max_tokens": config.max_tokens,  # 最大令牌数。
            "model_kwargs": config.model_kwargs or {},  # 模型额外参数。
        }
        # 获取 API 密钥，如果配置中没有就在环境变量里找。
        api_key = config.api_key or os.environ["OPENAI_API_KEY"]
        # 获取基础 URL，如果配置中没有就在环境变量里找。
        base_url = config.base_url or os.environ.get("OPENAI_API_BASE", None)
        # 如果配置中有 top_p 参数，加入参数字典。
        if config.top_p:
            kwargs["top_p"] = config.top_p
        # 如果配置中有默认头部信息，也加入参数字典。
        if config.default_headers:
            kwargs["default_headers"] = config.default_headers
        # 如果配置要求流式输出，设置回调和聊天对象。
        if config.stream:
            callbacks = config.callbacks if config.callbacks else [StreamingStdOutCallbackHandler()]
            chat = ChatOpenAI(
                **kwargs,  # 使用前面定义的参数。
                streaming=config.stream,  # 流式输出开关。
                callbacks=callbacks,  # 回调函数。
                api_key=api_key,  # API 密钥。
                base_url=base_url,  # 基础 URL。
                http_client=config.http_client,  # HTTP 客户端。
                http_async_client=config.http_async_client,  # 异步 HTTP 客户端。
            )
        # 如果不是流式输出，设置聊天对象。
        else:
            chat = ChatOpenAI(
                **kwargs,  # 使用前面定义的参数。
                api_key=api_key,  # API 密钥。
                base_url=base_url,  # 基础 URL。
                http_client=config.http_client,  # HTTP 客户端。
                http_async_client=config.http_async_client,  # 异步 HTTP 客户端。
            )
        # 如果有工具，调用一个特殊的方法处理。
        if self.tools:
            return self._query_function_call(chat, self.tools, messages)

        # 调用聊天对象获得回答。
        chat_response = chat.invoke(messages)
        # 如果开启了计费，返回回答内容和令牌使用情况。
        if self.config.token_usage:
            return chat_response.content, chat_response.response_metadata["token_usage"]
        # 如果没开启计费，只返回回答内容。
        return chat_response.content

    # 这个内部函数用来处理带有工具的回答。
    def _query_function_call(
        self,
        chat: ChatOpenAI,  # 聊天对象。
        tools: Optional[Union[Dict[str, Any], Type[BaseModel], Callable[..., Any], BaseTool]],  # 工具。
        messages: list[BaseMessage],  # 对话信息。
    ) -> str:
        # 导入一些需要的模块。
        from langchain.output_parsers.openai_tools import JsonOutputToolsParser
        from langchain_core.utils.function_calling import convert_to_openai_tool

        # 将工具转换成 OpenAI 可以理解的形式。
        openai_tools = [convert_to_openai_tool(tools)]
        # 绑定工具并设置解析器。
        chat = chat.bind(tools=openai_tools).pipe(JsonOutputToolsParser())
        # 调用聊天对象获得回答，并尝试将其转化为 JSON 格式。
        try:
            return json.dumps(chat.invoke(messages)[0])
        # 如果转化失败，返回错误信息。
        except IndexError:
            return "Input could not be mapped to the function!"

