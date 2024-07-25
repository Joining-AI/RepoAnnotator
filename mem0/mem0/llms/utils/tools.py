# 这里定义了一个名为 ADD_MEMORY_TOOL 的工具。
ADD_MEMORY_TOOL = {
    # 工具的类型是函数。
    "type": "function",
    # 函数的信息如下：
    "function": {
        # 函数的名字叫做 add_memory。
        "name": "add_memory",
        # 这个函数是用来添加一条记忆的。
        "description": "Add a memory",
        # 函数需要接收的参数信息如下：
        "parameters": {
            # 参数类型是一个对象（就像一个小盒子，可以放一些东西进去）。
            "type": "object",
            # 对象里面可以放的东西（属性）如下：
            "properties": {
                # 可以放一个叫做 data 的东西，它是一个字符串。
                "data": {"type": "string", "description": "Data to add to memory"}
            },
            # 必须要有的东西就是 data。
            "required": ["data"],
        },
    },
}

