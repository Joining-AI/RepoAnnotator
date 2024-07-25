# 导入pytest库，这是一个用于编写测试的库。
import pytest

# 从mem0模块导入Memory类，这个类是用来存储和管理“记忆”的。
from mem0 import Memory

# 这个函数是一个特殊的设置函数，会在每个测试函数运行前执行一次。
@pytest.fixture
def memory_store():
    # 创建一个Memory实例并返回它。这个实例将被用来在不同的测试中共享。
    return Memory()

# 定义第一个测试函数：测试创建记忆。
def test_create_memory(memory_store):
    # 设置要存储的数据内容。
    data = "Name is John Doe."
    # 调用memory_store的create方法来创建一个新的记忆，并获取它的标识符（ID）。
    memory_id = memory_store.create(data=data)
    # 检查通过ID获取的记忆内容是否与原来存储的内容一致。
    assert memory_store.get(memory_id) == data

# 定义第二个测试函数：测试获取记忆。
def test_get_memory(memory_store):
    # 设置要存储的数据内容。
    data = "Name is John Doe."
    # 调用memory_store的create方法来创建一个新的记忆，并获取它的标识符（ID）。
    memory_id = memory_store.create(data=data)
    # 通过ID获取记忆内容。
    retrieved_data = memory_store.get(memory_id)
    # 检查获取到的记忆内容是否与原来存储的内容一致。
    assert retrieved_data == data

# 定义第三个测试函数：测试更新记忆。
def test_update_memory(memory_store):
    # 设置要存储的数据内容。
    data = "Name is John Doe."
    # 调用memory_store的create方法来创建一个新的记忆，并获取它的标识符（ID）。
    memory_id = memory_store.create(data=data)
    # 设置新的数据内容。
    new_data = "Name is John Kapoor."
    # 更新记忆内容。
    updated_memory = memory_store.update(memory_id, new_data)
    # 检查更新后的记忆内容是否与新的数据内容一致。
    assert updated_memory == new_data
    # 再次检查更新后通过ID获取的记忆内容是否与新的数据内容一致。
    assert memory_store.get(memory_id) == new_data

# 定义第四个测试函数：测试删除记忆。
def test_delete_memory(memory_store):
    # 设置要存储的数据内容。
    data = "Name is John Doe."
    # 调用memory_store的create方法来创建一个新的记忆，并获取它的标识符（ID）。
    memory_id = memory_store.create(data=data)
    # 删除指定ID的记忆。
    memory_store.delete(memory_id)
    # 检查删除后通过ID获取的记忆内容是否为None，表示记忆已经被成功删除。
    assert memory_store.get(memory_id) is None

# 定义第五个测试函数：测试记忆的历史记录功能。
def test_history(memory_store):
    # 设置要存储的数据内容。
    data = "I like indian food."
    # 调用memory_store的create方法来创建一个新的记忆，并获取它的标识符（ID）。
    memory_id = memory_store.create(data=data)
    # 获取指定ID的记忆的历史记录。
    history = memory_store.history(memory_id)
    # 检查历史记录是否只包含最初存储的数据。
    assert history == [data]
    # 再次检查通过ID获取的记忆内容是否与最初存储的内容一致。
    assert memory_store.get(memory_id) == data

    # 设置新的数据内容。
    new_data = "I like italian food."
    # 更新记忆内容。
    memory_store.update(memory_id, new_data)
    # 再次获取指定ID的记忆的历史记录。
    history = memory_store.history(memory_id)
    # 检查历史记录是否包含最初和新的数据内容。
    assert history == [data, new_data]
    # 最后再检查通过ID获取的记忆内容是否与最新的数据内容一致。
    assert memory_store.get(memory_id) == new_data

# 定义第六个测试函数：测试列出所有记忆。
def test_list_memories(memory_store):
    # 设置第一条要存储的数据内容。
    data1 = "Name is John Doe."
    # 设置第二条要存储的数据内容。
    data2 = "Name is John Doe. I like to code in Python."
    # 创建第一条记忆。
    memory_store.create(data=data1)
    # 创建第二条记忆。
    memory_store.create(data=data2)
    # 获取所有记忆的列表。
    memories = memory_store.list()
    # 检查第一条数据是否在所有记忆的列表里。
    assert data1 in memories
    # 检查第二条数据是否在所有记忆的列表里。
    assert data2 in memories

