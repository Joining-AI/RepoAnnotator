# 这一行是从一个叫做mem0的程序里的configs模块中，找到prompts这个子模块，
# 然后把里面的UPDATE_MEMORY_PROMPT这个东西导入进来。你可以想象成从一个大盒子里拿出一个小盒子。
from mem0.configs.prompts import UPDATE_MEMORY_PROMPT

# 下面开始定义一个函数，名字叫get_update_memory_prompt。
# 这个函数是做什么的呢？它会帮我们生成一段话，这段话是用来更新记忆的提示。
# 它需要三个信息：已经有的记忆(existing_memories)，新的记忆(memory)，和一个模板(template)。
# 如果你不给它指定模板，它就会用UPDATE_MEMORY_PROMPT这个我们之前拿出来的小盒子。
def get_update_memory_prompt(existing_memories, memory, template=UPDATE_MEMORY_PROMPT):
    # 这里就是用模板(template)来生成那句话了。
    # 它会把已有的记忆和新的记忆填进模板里，然后返回这句话。
    return template.format(existing_memories=existing_memories, memory=memory)

# 接下来又定义了一个新函数，名字叫get_update_memory_messages。
# 这个函数会帮我们创建一个消息列表，这个列表里只有一个消息。
# 这个消息是告诉别人我们要更新记忆了。
def get_update_memory_messages(existing_memories, memory):
    # 这里就是创建那个消息列表了。
    # 首先，我们创建一个字典，字典里有两个键：'role'和'content'。
    # 'role'的值是'user'，表示这是一个用户发的消息。
    # 'content'的值是通过调用get_update_memory_prompt函数得到的，就是那段更新记忆的提示。
    # 最后，我们把这个字典放进一个列表里，然后返回这个列表。
    return [
        {
            "role": "user",
            "content": get_update_memory_prompt(existing_memories, memory),
        },
    ]

