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


import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maplehouse.settings")
django.setup()
from django.core.mail import send_mail
import threading
from maplehouse import settings
import time
from renting import models
from celery_task.celery import cel

@cel.task
def test_celery():
    user=models.UserOrder.objects.all()
    for u in user:
        timeArray=time.strptime(str(u.past_date), "%Y-%m-%d %H:%M:%S")
        past_date=int(time.mktime(timeArray))
        now=time.time()
        print(past_date-now)
        if past_date-now<60*60*24*10:
            t = threading.Thread(target=send_mail, args=("maple租房网",
                                                         '你的租赁时间快到期了',
                                                         settings.EMAIL_HOST_USER,
                                                         ["ffm1110@163.com"])
                                 )
            t.start()
    return



