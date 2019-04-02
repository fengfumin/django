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

from celery import Celery
from celery.schedules import crontab

cel = Celery('celery_demo',
             broker='redis://127.0.0.1:6379/3',
             backend='redis://127.0.0.1:6379/4',
             # 包含以下两个任务文件，去相应的py文件中找任务，对多个任务做分类
             include=['celery_task.tasks1',
                      ])

# 时区
cel.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
cel.conf.enable_utc = False

cel.conf.beat_schedule = {
    # 名字随意命名,定时发送邮件
    'add-every-day': {
            'task': 'celery_task.tasks1.test_celery',
            'schedule': crontab(minute=00, hour=20),
            'args': ()
        },
}