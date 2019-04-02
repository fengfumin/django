# -*- coding: utf-8 -*-
# __author__="maple"
"""
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
from stark.service.stark import site,ModelStark
from renting import models

class HouseConfig(ModelStark):
    list_display = ["title","house_name","area_location"]
    list_display_links = ["house_name"]
    search_fields = ["title","house_name",]

    def patch_init(self, request, queryset):
        pass
    patch_init.desc = '批量价格处理'

    def patch_delete(self, request, queryset):
        pass

    patch_delete.desc = '批量数据删除'

    actions = [patch_init, patch_delete]


class HouseCheckConfig(ModelStark):
    list_filter = ["house","check_user"]

class UserOrderConfig(ModelStark):
    list_filter = ["house","user"]

site.register(models.House,HouseConfig)
site.register(models.UserInfo)
site.register(models.Broker)
site.register(models.HousingFacilities)
site.register(models.HousingCharacteristics)
site.register(models.HousingPictures)
site.register(models.UserOrder,UserOrderConfig)
site.register(models.HouseCheck,HouseCheckConfig)
