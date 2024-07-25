# 这里是从一个叫做embedchain的程序库中导入一些东西。
from embedchain.models.data_type import (DataType, DirectDataType,
                                         IndirectDataType, SpecialDataType)

# 定义一个函数，名字叫test_subclass_types_in_data_type，它要检查小分类是否都在大分类里面。
def test_subclass_types_in_data_type():
    """这个函数要确保所有小类别的数据类型都能在大类别数据类型里面找到。"""

    # 现在我们要检查DirectDataType这个小分类里的每一个数据类型，看它们是不是也在大分类DataType里面。
    for data_type in DirectDataType:
        # 这里我们用assert语句来确认，如果不在，测试就会失败。
        assert data_type.value in DataType._value2member_map_

    # 接下来，我们做同样的事情，但是这次是检查IndirectDataType这个小分类。
    for data_type in IndirectDataType:
        assert data_type.value in DataType._value2member_map_

    # 最后，我们检查SpecialDataType这个小分类。
    for data_type in SpecialDataType:
        assert data_type.value in DataType._value2member_map_

# 再定义一个函数，名字叫test_data_type_in_subclasses，它要检查大分类里的数据类型是否都有一个小分类归属。
def test_data_type_in_subclasses():
    """这个函数要确保大类别数据类型中的所有数据类型，都能在某个小类别数据类型中找到。"""

    # 我们遍历大分类DataType中的每一个数据类型。
    for data_type in DataType:
        # 如果这个数据类型在DirectDataType小分类中能找到，我们就确认一下。
        if data_type.value in DirectDataType._value2member_map_:
            assert data_type.value in DirectDataType._value2member_map_
        # 如果在IndirectDataType小分类中能找到，我们也确认一下。
        elif data_type.value in IndirectDataType._value2member_map_:
            assert data_type.value in IndirectDataType._value2member_map_
        # 如果在SpecialDataType小分类中能找到，我们同样确认一下。
        elif data_type.value in SpecialDataType._value2member_map_:
            assert data_type.value in SpecialDataType._value2member_map_
        # 如果在任何小分类中都找不到，那就有问题了，测试会失败。
        else:
            assert False, f"{data_type.value} not found in any subclass enums"

