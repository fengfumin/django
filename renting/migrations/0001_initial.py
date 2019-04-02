# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-03-16 12:52
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('uuid', models.CharField(max_length=128, unique=True, verbose_name='交互唯一id')),
                ('nickname', models.CharField(max_length=64, null=True, verbose_name='昵称')),
                ('phone', models.BigIntegerField(help_text='用于手机验证码登录', null=True, unique=True, verbose_name='电话')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='email address')),
                ('role', models.SmallIntegerField(choices=[(0, '租房者'), (1, '管理人')], default=0, verbose_name='角色')),
                ('img', models.FileField(default='avatar/user/default.png', null=True, upload_to='avatar/user/', verbose_name='头像')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户管理表',
                'verbose_name_plural': '用户管理表',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Broker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128, verbose_name='经纪人登入名')),
                ('password', models.CharField(max_length=128, verbose_name='经纪人登入密码')),
                ('nickname', models.CharField(max_length=64, null=True, verbose_name='经纪人真名')),
                ('put_date', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('img', models.FileField(default='avatar/broker/default.png', null=True, upload_to='avatar/broker/', verbose_name='头像')),
                ('serve_years', models.IntegerField(null=True, verbose_name='经纪人服务年限')),
                ('serve_area', models.CharField(max_length=128, null=True, verbose_name='经纪人服务区域')),
                ('belong_store', models.CharField(max_length=128, null=True, verbose_name='经纪人所属店铺')),
                ('phone', models.BigIntegerField(help_text='用于手机验证码登录', null=True, unique=True, verbose_name='电话')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='email address')),
            ],
            options={
                'verbose_name': '经纪人表',
                'verbose_name_plural': '经纪人表',
            },
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('huose_num', models.CharField(max_length=128, unique=True, verbose_name='房源唯一id号')),
                ('title', models.CharField(max_length=128, null=True, verbose_name='房源标题')),
                ('house_name', models.CharField(max_length=64, null=True, verbose_name='小区名称')),
                ('area', models.FloatField(null=True, verbose_name='面积')),
                ('bedroom_num', models.SmallIntegerField(null=True, verbose_name='几室')),
                ('drawing_room_num', models.SmallIntegerField(null=True, verbose_name='几厅')),
                ('orientation', models.IntegerField(choices=[(0, '东'), (1, '南'), (2, '西'), (3, '北')], default=1, null=True, verbose_name='方位')),
                ('floor_type', models.IntegerField(choices=[(0, '低楼层'), (1, '中楼层'), (2, '高楼层'), (3, '顶层')], default=0, null=True, verbose_name='楼层位置')),
                ('floor_num', models.IntegerField(null=True, verbose_name='楼层数')),
                ('publish_date', models.DateTimeField(auto_now_add=True, verbose_name='房源发布时间')),
                ('month_price', models.IntegerField(null=True, verbose_name='每月租房价格')),
                ('area_location', models.IntegerField(choices=[(0, '浦东新区'), (1, '闵行区'), (2, '徐汇区'), (3, '普陀区'), (4, '宝山区'), (5, '长宁区'), (6, '杨浦区'), (7, '松江区'), (8, '虹口区'), (9, '嘉定区'), (10, '黄浦区'), (11, '静安区'), (12, '青浦区')], default=0, null=True, verbose_name='房源辖区')),
                ('rent_way', models.IntegerField(choices=[(0, '整租'), (1, '合租')], default=0, null=True, verbose_name='出租方式')),
                ('decoration', models.IntegerField(choices=[(0, '精装'), (1, '简装'), (2, '毛坯')], default=0, null=True, verbose_name='装修情况')),
            ],
            options={
                'verbose_name': '房源表',
                'verbose_name_plural': '房源表',
            },
        ),
        migrations.CreateModel(
            name='HouseCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_date', models.DateTimeField(auto_now_add=True, verbose_name='查看时间')),
                ('broker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='renting.Broker', verbose_name='经纪人')),
                ('check_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='看房用户')),
                ('house', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='renting.House', verbose_name='房源')),
            ],
            options={
                'verbose_name': '房源查看表',
                'verbose_name_plural': '房源查看表',
            },
        ),
        migrations.CreateModel(
            name='HousingCharacteristics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lightspot', models.CharField(max_length=255, null=True, verbose_name='房源亮点')),
                ('introduce', models.CharField(max_length=255, null=True, verbose_name='户型介绍')),
                ('traffic', models.CharField(max_length=255, null=True, verbose_name='交通出行')),
                ('rim', models.CharField(max_length=255, null=True, verbose_name='周边配套')),
                ('housing_message', models.CharField(max_length=255, null=True, verbose_name='小区信息')),
                ('house', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='renting.House')),
            ],
            options={
                'verbose_name': '房源配套设施表',
                'verbose_name_plural': '房源配套设施表',
            },
        ),
        migrations.CreateModel(
            name='HousingFacilities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('washing_machine', models.BooleanField(default=0, verbose_name='是否有洗衣机')),
                ('refrigerator', models.BooleanField(default=0, verbose_name='是否有冰箱')),
                ('television', models.BooleanField(default=0, verbose_name='是否有电视')),
                ('air_conditioner', models.BooleanField(default=0, verbose_name='是否有空调')),
                ('water_heater', models.BooleanField(default=0, verbose_name='是否有热水器')),
                ('natural_gas', models.BooleanField(default=0, verbose_name='是否有天然气')),
                ('bed', models.BooleanField(default=0, verbose_name='是否有床')),
                ('wifi', models.BooleanField(default=0, verbose_name='是否有网络')),
                ('elevator', models.BooleanField(default=0, verbose_name='是否有电梯')),
                ('house', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='renting.House')),
            ],
            options={
                'verbose_name': '房源配套设施表',
                'verbose_name_plural': '房源配套设施表',
            },
        ),
        migrations.CreateModel(
            name='HousingFocus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attention', models.BooleanField(verbose_name='是否关注')),
                ('check_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='关注用户')),
                ('house', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='renting.House')),
            ],
            options={
                'verbose_name': '房源关注表',
                'verbose_name_plural': '房源关注表',
            },
        ),
        migrations.CreateModel(
            name='HousingPictures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.FileField(default='avatar/house/default.png', null=True, upload_to='avatar/house/', verbose_name='房源图片')),
                ('house', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='renting.House')),
            ],
            options={
                'verbose_name': '房源图片表',
                'verbose_name_plural': '房源图片表',
            },
        ),
        migrations.CreateModel(
            name='TokenInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=128, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('broker', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='renting.Broker')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'token表',
                'verbose_name_plural': 'token表',
            },
        ),
    ]
