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

from haystack import indexes
from renting.models import House

class HouseIndex(indexes.SearchIndex, indexes.Indexable):
    #类名必须为需要检索的Model_name+Index，这里需要检索Article，所以创建ArticleIndex
    text = indexes.CharField(document=True, use_template=True)#创建一个text字段
    #其它字段
    title = indexes.CharField(model_attr='title')
    house_name = indexes.CharField(model_attr='house_name')
    huose_num = indexes.CharField(model_attr='huose_num')

    def get_model(self):#重载get_model方法，必须要有！
        return House

    def index_queryset(self, using=None):
        return self.get_model().objects.all()