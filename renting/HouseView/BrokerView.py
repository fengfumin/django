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

from django.shortcuts import render
from rest_framework.views import APIView

from renting import models

from django.core.paginator import Paginator


class BrokerInfo(APIView):
    def get(self,request):
        brokers=models.Broker.objects.all().order_by("pk")

        paginator = Paginator(brokers, 20)
        # 获取前端请求的页数,需要给一个默认页数
        current_page = request.GET.get("page", 1)
        current_page = int(current_page)
        # 生成page对象,就是一页
        page = paginator.page(current_page)
        # 判断总页数是否大于5
        if paginator.num_pages > 5:
            # 点击页数是否小于等于3
            if current_page <= 3:
                # 生成一个1到5的区间
                page_range = range(1, 6)
            #     当前页数大于最大页数减2
            elif current_page + 2 >= paginator.num_pages:
                # 生成一个最大页数减4,到最大页数加1的区间
                page_range = range(paginator.num_pages - 4, paginator.num_pages + 1)
            else:
                # 生成一个点击页数减2,到点击页数加2的区间,
                page_range = range(current_page - 2, current_page + 3)
        else:
            # 前端显示5页
            page_range = paginator.page_range
        return render(request,"broker.html",locals())