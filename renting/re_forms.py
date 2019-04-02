# -*- coding: utf-8 -*-
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

from django import forms
from django.forms import widgets
from renting import models
from django.core.exceptions import ValidationError


# forms组件类
class RegForm(forms.Form):
    # 各名字要与userinfo表字段名字一致
    username = forms.CharField(min_length=3, max_length=16, label='用户名',
                               error_messages={"min_length": "用户名太短了", "max_length": "用户名太长了",
                                               "required": "用户名不能为空"},
                               widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入用户名"}))
    password = forms.CharField(min_length=3, max_length=16, label='密码',
                               error_messages={"min_length": "密码太短了", "max_length": "密码太长了",
                                               "required": "密码不能为空"},
                               widget=widgets.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入密码"}))
    re_password = forms.CharField(min_length=3, max_length=16, label='确认密码',
                                  error_messages={"min_length": "确认密码太短了", "max_length": "确认密码太长了",
                                                  "required": "确认密码不能为空"},
                                  widget=widgets.PasswordInput(
                                      attrs={"class": "form-control", "placeholder": "请输入确认密码"}))
    nickname = forms.CharField(max_length=16, label='昵称',
                               error_messages={"max_length": "昵称太长了",
                                               "required": "昵称不能为空"},
                               widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入昵称"}))
    email = forms.EmailField(label='邮箱',required=False,
                             error_messages={'invalid': '邮箱格式不合法',},
                             widget=widgets.EmailInput(attrs={"class": "form-control", "placeholder": "请输入邮箱,可以不填"}))
    phone = forms.IntegerField(min_value=10000000000, max_value=99999999999, label='手机号',
                               error_messages={"min_value": "手机号必须是11位数", "max_value": "手机号必须是11位数",
                                               "required": "手机号不能为空" },
                               widget=widgets.NumberInput(
                                   attrs={"class": "form-control", "placeholder": "请输入手机号", }))

    # 局部钩子函数,用于判断用户名是否已存在,只能判断一个字段
    # 函数名称clean_username中的username必须与form中username一致
    def clean_username(self):
        name = self.cleaned_data.get("username")
        res = models.UserInfo.objects.filter(username=name).first()
        if res:
            raise ValidationError("用户名已存在")
        return name

    def clean_email(self):
        email=self.cleaned_data.get("email")
        if email:
            res=models.UserInfo.objects.filter(email=email).first()
            if res:
                raise ValidationError("该邮箱已存在")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        res = models.UserInfo.objects.filter(email=phone).first()
        if res:
            raise ValidationError("该手机号已存在")
        return phone

    # 全局钩子,用来判断两次密码是否一致,能判断所有字段
    def clean(self):
        pwd = self.cleaned_data.get("password")
        re_pwd = self.cleaned_data.get("re_password")
        if pwd != re_pwd:
            raise ValidationError("两次密码不一致")
        return self.cleaned_data
