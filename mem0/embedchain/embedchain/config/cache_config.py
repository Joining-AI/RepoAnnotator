# 导入所需的模块
from typing import Any, Optional  # 导入类型提示相关的模块
from embedchain.config.base_config import BaseConfig  # 导入基础配置类
from embedchain.helpers.json_serializable import register_deserializable  # 导入注册可序列化功能的装饰器

# 使用装饰器注册类以便于序列化
@register_deserializable
class CacheSimilarityEvalConfig(BaseConfig):  # 定义一个类，继承自BaseConfig
    """
    这个类用于比较两个嵌入（embedding）的相似度，通过计算它们之间的距离。
    在检索阶段，“search_result”是近似最近邻搜索使用的距离值，并已存储在“cache_dict”中。
    “max_distance”用来限制这个距离的最大值，确保其位于0到“max_distance”之间。
    “positive”表示距离与两个实体的相似度成正比还是反比。
    如果“positive”设为“False”，那么最终得分将是“max_distance”减去这个距离值。

    :param max_distance: 最大距离的界限。
    :type max_distance: float
    :param positive: 距离越大表示两个实体越相似时为True，否则为False。
    :type positive: bool
    """

    def __init__(  # 初始化方法
        self,
        strategy: Optional[str] = "distance",  # 策略，默认为“distance”
        max_distance: Optional[float] = 1.0,  # 最大距离，默认为1.0
        positive: Optional[bool] = False,  # 是否为正比，默认为False
    ):
        self.strategy = strategy  # 设置策略属性
        self.max_distance = max_distance  # 设置最大距离属性
        self.positive = positive  # 设置是否为正比属性

    @staticmethod
    def from_config(config: Optional[dict[str, Any]]):  # 从配置字典创建实例的方法
        if config is None:  # 如果配置为空
            return CacheSimilarityEvalConfig()  # 返回默认构造的实例
        else:
            return CacheSimilarityEvalConfig(  # 否则根据配置创建实例
                strategy=config.get("strategy", "distance"),  # 获取策略，默认为“distance”
                max_distance=config.get("max_distance", 1.0),  # 获取最大距离，默认为1.0
                positive=config.get("positive", False),  # 获取是否为正比，默认为False
            )

