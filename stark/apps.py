from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class StarkConfig(AppConfig):
    name = 'stark'

    # 启动stark组件
    def ready(self):
        return autodiscover_modules("stark")
