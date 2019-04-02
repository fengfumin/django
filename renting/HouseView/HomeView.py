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

# 分页组件
from django.core.paginator import Paginator


class Home(APIView):
    # authentication_classes = [LoginAuth]
    def get(self, request, *args, **kwargs):
        house_num=request.GET.get("house_num")
        # home - (?P < location > (\d+))-(?P < price > (\d+))-(?P < area > (\d+))-(?P < page > (\d+)) /
        location_dic = {"浦东新区": 1, "闵行区": 2, "徐汇区": 3, "普陀区": 4,
                        "宝山区": 5, "长宁区": 6, "杨浦区": 7, "松江区": 8,
                        "虹口区": 9, "嘉定区": 10, "黄浦区": 11, "静安区": 12, "青浦区": 13, }

        price_dic = {"1500元以下": 1, "1500-2500元": 2, "2500-3500元": 3, "3500-5000元": 4,
                     "5000-8000元": 5, "8000-10000元": 6, "10000元以上": 7}

        area_dic = {"50㎡以下": 1, "50-70㎡": 2, "90-110㎡": 3, "110-130㎡": 4, "130-150㎡": 5, "150-200㎡": 6,
                    "200㎡以上": 7}

        price_list = {1: {"month_price__lte": 1500}, 2: {"month_price__lte": 2500, "month_price__gte": 1500},
                      3: {"month_price__lte": 3500, "month_price__gte": 2500},
                      4: {"month_price__lte": 5000, "month_price__gte": 3500},
                      5: {"month_price__lte": 8000, "month_price__gte": 5000},
                      6: {"month_price__lte": 10000, "month_price__gte": 8000},
                      7: {"month_price__gte": 10000}}

        area_list = {1: {"area__lte": 50}, 2: {"area__gte": 50, "area__lte": 70},
                     3: {"area__gte": 90, "area__lte": 110},
                     4: {"area__gte": 110, "area__lte": 130}, 5: {"area__gte": 130, "area__lte": 150},
                     6: {"area__gte": 150, "area__lte": 200}, 7: {"area__gte": 200}}

        if len(kwargs) < 3:
            kwargs["location"] = 0
            kwargs["price"] = 0
            kwargs["area"] = 0

        for k, v in kwargs.items():
            temp = int(v)
            kwargs[k] = temp
        print(kwargs)

        location_id = kwargs.get('location')
        price_id = kwargs.get('price')
        area_id = kwargs.get('area')
        page_id = kwargs.get('page')

        # 查询所有
        houses = models.House.objects.all().order_by("pk")

        if location_id == 0 and price_id == 0 and area_id == 0:
            houses = models.House.objects.all().order_by("pk")

        # 查询区域
        elif location_id != 0 and price_id == 0 and area_id == 0:
            houses = models.House.objects.filter(area_location=location_id - 1).order_by("pk")

        # 查询价格
        elif location_id == 0 and price_id in price_list and area_id == 0:
            houses = models.House.objects.filter(**price_list[price_id]).order_by("pk")

        # 查询面积
        elif location_id == 0 and area_id in area_list and price_id == 0:
            houses = models.House.objects.filter(**area_list[area_id]).order_by("pk")
        # 查询区域和价格
        elif location_id != 0 and price_id in price_list and area_id == 0:
            houses = models.House.objects.filter(area_location=location_id - 1, **price_list[price_id]).order_by("pk")
        # 查询区域和面积
        elif location_id != 0 and area_id in area_list and price_id == 0:
            houses = models.House.objects.filter(area_location=location_id - 1, **area_list[area_id]).order_by("pk")
        # 查询价格和面积
        elif location_id == 0 and area_id in area_list and price_id in price_list:
            houses = models.House.objects.filter(**area_list[area_id], **price_list[price_id]).order_by("pk")
        # 查询价格和面积和区域
        elif location_id != 0 and area_id in area_list and price_id in price_list:
            houses = models.House.objects.filter(area_location=location_id - 1, **area_list[area_id],
                                                 **price_list[price_id]).order_by("pk")

        if house_num:
            houses=models.House.objects.filter(huose_num=house_num)

        paginator = Paginator(houses, 20)
        # 获取前端请求的页数,需要给一个默认页数
        current_page = page_id
        try:
            # 捕捉异常页码
            page = paginator.page(current_page)
        except Exception:
            current_page = 1
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

        return render(request, "home.html", {"page": page, "page_range": page_range,
                                             "current_page": current_page, "location_dic": location_dic
            , "price_dic": price_dic, "area_dic": area_dic,"kwargs": kwargs
                                             })
