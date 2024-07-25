from typing import Optional  # 这行代码从typing模块导入了Optional，它允许我们在定义变量时说这个变量可以是某种类型，也可以是None。
from pydantic import BaseModel, Field, field_validator, model_validator  # 这行代码从pydantic模块导入了一些工具，用来创建数据模型和验证数据。

