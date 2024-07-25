# 这里我们从typing模块中导入了Any和Optional这两个工具。
# 它们可以帮助我们更好地理解函数中变量的类型。
from typing import Any, Optional

# 下面定义了一个叫做merge_metadata_dict的函数，
# 它的工作是合并两个字典（left和right）中的信息。
# 如果两个字典有相同的键，它会检查这些键的值类型是否相同，
# 并根据不同的情况合并它们。
def merge_metadata_dict(left: Optional[dict[str, Any]], right: Optional[dict[str, Any]]) -> Optional[dict[str, Any]]:
    """
    这个函数的作用是把两个人的信息（左和右）的元数据合并起来。
    
    参数：
        left (dict[str, Any]): 这是人类消息的元数据。
        right (dict[str, Any]): 这是AI消息的元数据。
        
    返回：
        dict[str, Any]: 合并后的元数据字典，去重后存储到数据库中。
    """
    
    # 如果左右两边的字典都是空的，直接返回None，表示没有东西可合并。
    if not left and not right:
        return None
    # 如果左边的字典是空的，那么就直接返回右边的字典。
    elif not left:
        return right
    # 如果右边的字典是空的，那么就直接返回左边的字典。
    elif not right:
        return left

    # 我们先复制左边的字典，这样不会改变原始的字典内容。
    merged = left.copy()

    # 现在我们要遍历右边字典的所有键值对。
    for k, v in right.items():
        # 如果这个键在合并后的字典中不存在，我们就直接添加进去。
        if k not in merged:
            merged[k] = v
        # 如果键存在，但它的值类型和右边字典的值类型不同，那就有问题了。
        elif type(merged[k]) != type(v):
            # 抛出一个错误，告诉程序员这里有问题。
            raise ValueError(f'additional_kwargs["{k}"] already exists in this message,' " but with a different type.")
        # 如果键对应的值是一个字符串，我们可以简单地将它们拼接起来。
        elif isinstance(merged[k], str):
            merged[k] += v
        # 如果键对应的值是一个字典，我们需要递归地调用这个函数再次合并。
        elif isinstance(merged[k], dict):
            merged[k] = merge_metadata_dict(merged[k], v)
        # 如果以上条件都不满足，说明我们遇到了未知的情况，抛出错误。
        else:
            raise ValueError(f"Additional kwargs key {k} already exists in this message.")
    
    # 最后，返回合并后的字典。
    return merged

