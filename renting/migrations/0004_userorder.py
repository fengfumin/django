# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-03-20 16:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('renting', '0003_auto_20190319_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=128, verbose_name='订单号')),
                ('order_state', models.BooleanField(help_text='True为已支付', verbose_name='订单状态')),
                ('start_date', models.DateTimeField(verbose_name='租赁开始时间')),
                ('past_date', models.DateTimeField(verbose_name='租赁结束时间')),
                ('house', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='renting.House', verbose_name='房源')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
    ]
