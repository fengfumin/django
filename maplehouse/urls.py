"""maplehouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^renting/', include('renting.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from maplehouse import settings
from renting import views
from renting.HouseView import HomeView, DetailView, BrokerView, SubwayView, PayView, PersonalView
from django.views.generic.base import RedirectView
from stark.service.stark import site

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 自定义后台管理路由
    url(r'^stark/',site.urls ),
    # media文件夹配置,用户可以无限制访问
    url(r'^media(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    # 注册
    url(r'^register/$', views.register),
    # 登入
    url(r'^login/$', views.login),
    url(r'^login_out/$', views.login_out),
    # 修改密码
    url(r'^change_password/$', views.change_password),
    # 随机验证码
    url(r'^get_valid_code/$', views.get_valid_code),
    # 主页
    url(r'^$', HomeView.Home.as_view()),
    url(r'^home/$', HomeView.Home.as_view()),
    url(r'^home-(?P<location>(\d+))-(?P<price>(\d+))-(?P<area>(\d+))/$', HomeView.Home.as_view()),
    url(r'^home-(?P<location>(\d+))-(?P<price>(\d+))-(?P<area>(\d+))-(?P<page>(\d+))/$', HomeView.Home.as_view()),
    # 详情页
    url(r'^detail/(?P<house_num>(\d+))/$', DetailView.HouseDetail.as_view()),
    # 关注连接
    url(r'^attention/$', DetailView.Attention.as_view()),
    # 经纪人信息页面
    url(r'^broker/$', BrokerView.BrokerInfo.as_view()),
    # 地铁地图
    url(r'^subway/$', SubwayView.Subway.as_view()),
    # 在线支付
    url(r'^pay/$', PayView.Pay.as_view()),
    # 支付回调地址
    url(r'^callback/$', PayView.CallBack.as_view()),
    # 个人主页设置
    url(r'^personal/$', PersonalView.Personal.as_view()),
    # 全文检索
    url(r'^search/', include('haystack.urls')),
    url(r'^favicon.ico$', RedirectView.as_view(url=r'static/img/ooopic.ico')),

]
