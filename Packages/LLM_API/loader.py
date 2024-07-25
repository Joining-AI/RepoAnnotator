from .qwen import QwenService

class LLMLoader:
    def __init__(self, service_type=None, version=None):
        self.service = self._initialize_service(service_type, version)
    
    def _initialize_service(self, service_type, version):
        if service_type in ['qwen', None]:
            version = version or 'long'
            # 'glm-4' 'glm-4v' 'glm-3-turbo'
            return QwenService(version)
#        elif service_type in ['zhipu']:
#            version = version or 'glm-3-turbo'
#            return GLMService(version)
#        elif service_type in ['kimi']:
#            version = version or '32k'
#            # '8k'1M/12￥ '32k'1M/24￥ '128k'1M/60￥
#            return KimiService(version)
#        elif service_type in ['deepseek']:
#            version = version or 'chat'
#            return DeepSeekService(version)
#        elif service_type in ['huida']:
#            version = version or 'gpt-4o'
#            # '8k'1M/12￥ '32k'1M/24￥ '128k'1M/60￥
#            return HuidaService(version)
#        elif service_type in ['sensetime']:
#            version = version or 'SenseChat'
#            # SenseChat SenseChat-32K SenseChat-128K SenseChat-Turbo SenseChat-FunctionCall
#            return SenseService(version=version)
        else:
            raise ValueError('未知的服务类型')