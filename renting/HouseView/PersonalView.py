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
from renting.authentication_module import LoginAuth
from renting import models

# 登入装饰器

class Personal(APIView):

    authentication_classes = [LoginAuth]

    def get(self,request):
        check_houses=models.HousingFocus.objects.filter(check_user=request.user,attention=1)
        orders=models.UserOrder.objects.filter(user=request.user)

        return render(request,"personal.html",locals())