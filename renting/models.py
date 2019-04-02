from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType



# Create your models here.
class UserInfo(AbstractUser):
    '''
    用户信息表(包括看房者,经纪人,管理员)
    '''
    uuid = models.CharField(max_length=128, verbose_name="交互唯一id", unique=True)
    nickname = models.CharField(max_length=64, verbose_name="昵称", null=True)
    phone = models.BigIntegerField(unique=True, help_text="用于手机验证码登录", null=True, verbose_name="电话")
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        blank=True,
        null=True
    )
    role_choices = ((0, '租房者'), (1, '管理人'))
    role = models.SmallIntegerField(choices=role_choices, default=0, verbose_name="角色")
    img = models.FileField(upload_to="avatar/user/", default="avatar/user/default.png", verbose_name="头像",
                           null=True)
    def __str__(self):
        return "%s" % self.username

    class Meta:
        verbose_name = "用户管理表"
        verbose_name_plural = "用户管理表"


class Broker(models.Model):
    '''
    经纪人
    '''
    username=models.CharField(max_length=128,verbose_name="经纪人登入名")
    password=models.CharField(max_length=128,verbose_name="经纪人登入密码")
    nickname = models.CharField(max_length=64, verbose_name="经纪人真名", null=True)
    put_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    img = models.FileField(upload_to="avatar/broker/", default="avatar/broker/default.png", verbose_name="头像", null=True)
    serve_years = models.IntegerField(verbose_name="经纪人服务年限", null=True)
    serve_area = models.CharField(verbose_name="经纪人服务区域", max_length=128, null=True)
    belong_store = models.CharField(verbose_name="经纪人所属店铺", max_length=128, null=True)
    phone = models.BigIntegerField(help_text="用于手机验证码登录", null=True, verbose_name="电话")
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        blank=True,
        null=True
    )
    def __str__(self):
        return "%s" % self.nickname
    class Meta:
        verbose_name = "经纪人表"
        verbose_name_plural = "经纪人表"


class TokenInfo(models.Model):
    '''
    token表
    '''
    user = models.OneToOneField(to="UserInfo", to_field="id", null=True)
    broker = models.OneToOneField(to="Broker", to_field="id", null=True)
    token = models.CharField(max_length=128, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.user.username

    class Meta:
        verbose_name = "token表"
        verbose_name_plural = "token表"


class House(models.Model):
    '''
    房源表
    '''
    huose_num = models.CharField(max_length=128, verbose_name="房源唯一id号", unique=True)
    title = models.CharField(max_length=128, verbose_name="房源标题", null=True)
    house_name = models.CharField(max_length=64, verbose_name="小区名称", null=True)
    area = models.FloatField(verbose_name="面积", null=True)
    bedroom_num = models.SmallIntegerField(verbose_name="几室", null=True)
    drawing_room_num = models.SmallIntegerField(verbose_name="几厅", null=True)
    orientation_choices = ((0, "东"), (1, "南"), (2, "西"), (3, "北"))
    orientation = models.IntegerField( verbose_name="方位", default=1, choices=orientation_choices,
                                      null=True)
    floor_type_choices = ((0, "低楼层"), (1, "中楼层"), (2, "高楼层"), (3, "顶层"),(4,"底层"))
    floor_type = models.IntegerField( verbose_name="楼层位置", default=0, choices=floor_type_choices,
                                     null=True)
    floor_num = models.IntegerField(verbose_name="楼层数", null=True)
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name="房源发布时间")
    month_price = models.IntegerField(verbose_name="每月租房价格", null=True)
    area_location_choices = ((0, "浦东新区"), (1, "闵行区"), (2, "徐汇区"), (3, "普陀区"),
                             (4, "宝山区"), (5, "长宁区"), (6, "杨浦区"), (7, "松江区"),
                             (8, "虹口区"), (9, "嘉定区"), (10, "黄浦区"), (11, "静安区"),
                             (12, "青浦区"))
    area_location = models.IntegerField( verbose_name="房源辖区", default=0, choices=area_location_choices,
                                        null=True)
    rent_way_choices = ((0, "整租"), (1, "合租"))
    rent_way = models.IntegerField( verbose_name="出租方式", default=0, choices=rent_way_choices, null=True)
    decoration_choices = ((0, "精装"), (1, "简装"), (2, "毛坯"))
    decoration = models.IntegerField( verbose_name="装修情况", default=0, choices=decoration_choices,
                                     null=True)
    trading_area=models.CharField(max_length=64,verbose_name="商圈",null=True)
    title_img = models.FileField(upload_to="avatar/house/", default="avatar/house/default.png", verbose_name="标题图片",
                           null=True)

    def __str__(self):
        return "%s" % self.title

    class Meta:
        verbose_name = "房源表"
        verbose_name_plural = "房源表"


class HousingFacilities(models.Model):
    '''
    房源配套设施表
    '''
    house = models.OneToOneField(to="House", on_delete=models.CASCADE, null=True)
    washing_machine = models.BooleanField(default=0, verbose_name="是否有洗衣机")
    refrigerator = models.BooleanField(default=0, verbose_name="是否有冰箱")
    television = models.BooleanField(default=0, verbose_name="是否有电视")
    air_conditioner = models.BooleanField(default=0, verbose_name="是否有空调")
    water_heater = models.BooleanField(default=0, verbose_name="是否有热水器")
    natural_gas = models.BooleanField(default=0, verbose_name="是否有天然气")
    bed = models.BooleanField(default=0, verbose_name="是否有床")
    wifi = models.BooleanField(default=0, verbose_name="是否有网络")
    elevator = models.BooleanField(default=0, verbose_name="是否有电梯")

    def __str__(self):
        return "%s" % self.house.title

    class Meta:
        verbose_name = "房源配套设施表"
        verbose_name_plural = "房源配套设施表"


class HousingCharacteristics(models.Model):
    '''
    房源特色表
    '''
    house = models.OneToOneField(to="House", on_delete=models.CASCADE, null=True)
    lightspot = models.CharField(max_length=255, verbose_name="房源亮点", null=True)
    introduce = models.CharField(max_length=255, verbose_name="户型介绍", null=True)
    traffic = models.CharField(max_length=255, verbose_name="交通出行", null=True)
    rim = models.CharField(max_length=255, verbose_name="周边配套", null=True)
    housing_message = models.CharField(max_length=255, verbose_name="小区信息", null=True)

    def __str__(self):
        return "%s" % self.house.title

    class Meta:
        verbose_name = "房源特色表"
        verbose_name_plural = "房源特色表"


class HousingPictures(models.Model):
    '''
    房源图片表
    '''
    house = models.ForeignKey(to="House", on_delete=models.CASCADE, null=True)
    picture = models.FileField(upload_to="avatar/house/", default="avatar/house/default.png", verbose_name="房源图片",
                               null=True)

    class Meta:
        verbose_name = "房源图片表"
        verbose_name_plural = "房源图片表"

    def __str__(self):
        return "%s" % self.house.title

class HouseCheck(models.Model):
    '''
    房源查看表,房源与用户多对多关系
    '''
    house=models.ForeignKey(to="House",on_delete=models.CASCADE, null=True,verbose_name="房源")
    check_user=models.ForeignKey(to="UserInfo",on_delete=models.CASCADE, null=True,verbose_name="看房用户")
    broker=models.ForeignKey(to="Broker",on_delete=models.CASCADE, null=True,verbose_name="经纪人")
    check_date=models.DateTimeField(verbose_name="查看时间",auto_now_add=True)

    class Meta:
        verbose_name = "房源查看表"
        verbose_name_plural = "房源查看表"

    def __str__(self):
        return "%s" % self.house.title



class HousingFocus(models.Model):
    '''
    房源关注表
    '''
    house = models.ForeignKey(to="House", on_delete=models.CASCADE, null=True)
    check_user = models.ForeignKey(to="UserInfo", on_delete=models.CASCADE, null=True, verbose_name="关注用户")
    attention=models.BooleanField(verbose_name="是否关注")

    class Meta:
        verbose_name = "房源关注表"
        verbose_name_plural = "房源关注表"

    def __str__(self):
        return "%s" % self.house.title


class UserOrder(models.Model):
    user=models.ForeignKey(to="UserInfo",on_delete=models.CASCADE, null=True,verbose_name="用户")
    house=models.ForeignKey(to="House",on_delete=models.CASCADE, null=True,verbose_name="房源")
    order_id=models.CharField(max_length=128,verbose_name="订单号")
    order_state=models.BooleanField(verbose_name="订单状态",help_text="True为已支付")
    start_date=models.DateTimeField(verbose_name="租赁开始时间")
    past_date=models.DateTimeField(verbose_name="租赁结束时间")

    class Meta:
        verbose_name = "订单表"
        verbose_name_plural = "订单表"

    def __str__(self):
        return "%s" % self.order_id



