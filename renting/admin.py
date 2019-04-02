from django.contrib import admin
from renting import models
# Register your models here.
class HouseConfig(admin.ModelAdmin):
    list_display = ["title","huose_num","house_name","area_location"]
    # 字段建立链接
    list_display_links = ["title","huose_num","house_name"]
    search_fields = ["title","huose_num","house_name"]


admin.site.register(models.TokenInfo)
admin.site.register(models.HousingPictures)
admin.site.register(models.House,HouseConfig)
admin.site.register(models.HousingCharacteristics)
admin.site.register(models.UserInfo)
admin.site.register(models.Broker)
admin.site.register(models.HouseCheck)
admin.site.register(models.HousingFocus)
admin.site.register(models.HousingFacilities)
admin.site.register(models.UserOrder)


