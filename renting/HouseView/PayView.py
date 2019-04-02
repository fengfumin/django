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
from django.shortcuts import render, redirect, HttpResponse
from rest_framework.views import APIView
from renting.authentication_module import LoginAuth
from renting import models
import datetime
from common.pay import AliPay
import time


def ali():
    '''
    生成支付对象
    :return:
    '''
    # 沙箱环境地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info
    app_id = "2016092500595152"
    # 支付宝收到用户的支付,会向商户发两个请求,一个get请求,一个post请求
    # POST请求，用于最后的检测
    notify_url = "http://www.maplepython.com/callback/"
    # GET请求，用于页面的跳转展示
    return_url = "http://www.maplepython.com/callback/"
    # 用户私钥
    merchant_private_key_path = "keys/app_private_2048.txt"
    # 支付宝公钥
    alipay_public_key_path = "keys/alipay_public_2048.txt"
    # 生成一个AliPay的对象
    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=merchant_private_key_path,
        alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,  # 默认False,
    )
    return alipay


class Pay(APIView):
    authentication_classes = [LoginAuth]

    def get(self, request):
        now = datetime.datetime.now()
        last = datetime.datetime.now() + datetime.timedelta(days=30)
        house_num = request.GET.get("house")
        return render(request, "pay.html", locals())

    def post(self, request):
        start = request.POST.get("start")
        last = request.POST.get("last")
        house_num = request.POST.get("house_num")
        timeArray1 = time.strptime(start, "%Y-%m-%d")
        timeArray2 = time.strptime(last, "%Y-%m-%d")
        day = timeArray2.tm_yday - timeArray1.tm_yday
        if day < 30:
            return HttpResponse("租赁时间不能少于30天")
        print(day, type(day), house_num)
        house = models.House.objects.filter(huose_num=house_num).first()

        money = house.month_price * day / 30
        # 生成一个对象
        print(money)
        alipay = ali()
        # 生成支付的url
        # 对象调用direct_pay
        # 该方法生成一个加密串
        order_id = "x2" + str(time.time())
        query_params = alipay.direct_pay(
            subject="租房%s天" % day,  # 商品简单描述
            out_trade_no=order_id,  # 商户订单号
            total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
            start_date=start,
            past_date=last,
        )

        # 保存订单
        models.UserOrder.objects.create(user=request.user, house=house,
                                        order_id=order_id, start_date=start, past_date=last, order_state=0)

        pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
        print(pay_url)
        return redirect(pay_url)


class CallBack(APIView):
    authentication_classes = [LoginAuth]
    alipay = ali()

    def get(self, request):
        params = request.GET
        dic_params = {k: v for k, v in params.items()}
        sign = dic_params.pop('sign', None)
        status = self.alipay.verify(dic_params, sign)
        print('GET验证', status)
        return HttpResponse('支付成功')

    def post(self, request):
        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib.parse import parse_qs
        body_str = request.body.decode('utf-8')
        print(body_str)

        post_data = parse_qs(body_str)
        print('支付宝给我的数据:::---------', post_data)
        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]
        print('转完之后的字典', post_dict)
        # 做二次验证
        sign = post_dict.pop('sign', None)
        # 通过调用alipay的verify方法去认证
        status = self.alipay.verify(post_dict, sign)

        print('POST验证', status)
        if status:
            # 修改自己订单状态
            models.UserOrder.objects.filter(order_id=post_dict.get("out_trade_no")).update(
                order_state=1)

        return HttpResponse('POST返回')
