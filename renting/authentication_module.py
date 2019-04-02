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

from rest_framework.authentication import BaseAuthentication
from django.core.cache import cache
from renting import models
from rest_framework.exceptions import AuthenticationFailed


class LoginAuth(BaseAuthentication):
    def authenticate(self, request):
        # 从请求中获取用户携带的token
        token=request.COOKIES.get("token")
        # 从Redis中取出token
        user=cache.get(token)
        print(token,user)
        if user:
            return user,token
        else:
            raise AuthenticationFailed("你还没登入")
