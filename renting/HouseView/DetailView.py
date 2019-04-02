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
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from renting import serialize_module
import json,requests
from renting import models
import datetime
from renting.authentication_module import LoginAuth
from renting.create_response import MyResponse

from django.contrib.auth.models import AnonymousUser




def createdate(n):
    now=datetime.datetime.now()
    past_date=now-datetime.timedelta(days=n)
    return past_date


class HouseDetail(APIView):
    def get(self,request,house_num):
        house=models.House.objects.filter(huose_num=house_num).first()
        pic_list=models.HousingPictures.objects.filter(house=house)
        Characteristics=models.HousingCharacteristics.objects.filter(house=house).first()
        check_house=models.HouseCheck.objects.filter(house=house)

        Facilities=models.HousingFacilities.objects.filter(house=house).first()

        if type(request.user) !=AnonymousUser:
            Focus=models.HousingFocus.objects.filter(house=house,check_user=request.user).first()


        broker=models.Broker.objects.all().order_by("?").first()

        if check_house:
            check = check_house[0]
            past_seven = createdate(7)
            # 查询7天内的
            check_seven = models.HouseCheck.objects.filter(house=house, check_date__gt=past_seven)

            past_thirty = createdate(30)
            # 查询30天内的
            check_thirty = models.HouseCheck.objects.filter(house=house, check_date__gt=past_thirty)

            # print(check_thirty.count())
            # print(check_seven.count())
        else:
            check = ""
            check_thirty=""
            check_seven=""
        # house_ser=serialize_module.HouseSer(instance=house,many=False)
        # house_ser=house_ser.data
        url = "http://api.map.baidu.com/geocoder/v2/?address=上海市%s%s&output=json&ak=VRV8llF9Q33W1vXNCsej8xxcVnSOfjk8&callback=" % (
            house.get_area_location_display(), house.house_name)
        res = requests.get(url=url)
        if res.status_code==200:
            loction = res.text
            loction = json.loads(loction)
            lng = loction.get("result").get("location").get("lng")
            lat = loction.get("result").get("location").get("lat")

        return render(request,"homedetail.html",locals())

# 房源点关注
class Attention(APIView):
    authentication_classes = [LoginAuth]

    def post(self,request):
        response=MyResponse()
        print(request.user)
        house_id=request.data.get("house_id")
        attention=request.data.get("attention")
        # 将字符串转成bool
        attention = json.loads(attention)
        print(house_id, attention)
        res=models.HousingFocus.objects.filter(house_id=house_id,check_user=request.user)
        # 如果还没有关注
        if not res:
            models.HousingFocus.objects.create(house_id=house_id,check_user=request.user,attention=1)
            response.msg = "关注成功"
        else:
            if attention:
                models.HousingFocus.objects.filter(house_id=house_id,check_user=request.user).update(attention=1)
                response.msg = "关注成功"
            else:
                # 取消关注
                models.HousingFocus.objects.filter(house_id=house_id,check_user=request.user).update(attention=0)
                response.msg = "取消关注"
                response.status = 101
        return Response(response.get_dic)


