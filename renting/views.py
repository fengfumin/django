from django.shortcuts import render,HttpResponse,redirect
from renting import re_forms
from renting import models
from django.http import JsonResponse
# auth组件
from django.contrib import auth
import random
# 图片模块
from PIL import Image, ImageDraw, ImageFont
# 以二进制或字符串保存在内存中
from io import BytesIO, StringIO

from uuid import uuid4
# 缓存组件
from django.core.cache import cache
# 登入装饰器
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    if request.method == "GET":
        reg_form = re_forms.RegForm()
        return render(request, "register.html", locals())
    if request.is_ajax():
        response = {"status": 100, "msg": None}
        # 把前端数据通过forms进行过滤
        reg_form = re_forms.RegForm(request.POST)
        # 开启过滤
        if reg_form.is_valid():
            # 通过过滤的数据
            form_data = reg_form.cleaned_data
            # 删除确认密码数据
            form_data.pop("re_password")
            # 获取头像图片
            img_file = request.FILES.get('img_file')
            # 判断头像是否有,没有使用字段设置默认的
            if img_file:
                form_data['img'] = img_file
            # 注意用create_user
            form_data["uuid"]=uuid4()
            res = models.UserInfo.objects.create_user(**form_data)
            response["msg"] = "注册成功"
        else:
            response["msg"] = reg_form.errors
            response["status"] = 101
        return JsonResponse(response)


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.is_ajax():
        response = {"status": 100, "msg": None}
        name = request.POST.get('name')
        password = request.POST.get('password')
        code = request.POST.get('valid_code')
        valid_code = request.session.get("valid_code")
        print(code, valid_code)
        if code.upper() == valid_code.upper():
            # 得用auth组件查询
            user = auth.authenticate(username=name, password=password)
            print(user)
            if user:
                token = uuid4()
                models.TokenInfo.objects.update_or_create(user=user, defaults={'token': token})
                # 将token存到Redis中,设置超时时间一天
                cache.set(token, user, 60 * 60 * 24)
                response["msg"] = "登入成功"
                resp=JsonResponse(response)
                # 将token存入cookie中
                resp.set_cookie("token", token,max_age=60 * 60 * 24)
                # 将user保存到request中
                auth.login(request, user)
                return resp
            else:
                response["msg"] = "用户名或密码错误!"
                response["status"] = 101
        else:
            response["msg"] = "验证码错误!"
            response["status"] = 102
        return JsonResponse(response)

@login_required(login_url="/login/")
def login_out(request):
    auth.logout(request)
    token = request.COOKIES.get("token")
    cache.delete(token)
    return redirect("/home/")



def change_password(request):
    # 判断是否登入状态
    if request.user.is_authenticated():
        if request.method == "GET":
            return render(request, "personal.html")
        else:
            response = {"status": 100, "msg": None}
            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")
            renew_password = request.POST.get("renew_password")
            if request.user.check_password(old_password):
                if not new_password:
                    response["status"] = 102
                    response["msg"] = "新密码不能为空"
                elif new_password != renew_password:
                    response["status"] = 103
                    response["msg"] = "两次密码不一致"
                else:
                    request.user.set_password(new_password)
                    request.user.save()
                    auth.logout(request)
                    response["msg"] = "密码修改成功"
            else:
                response["status"] = 101
                response["msg"] = "旧密码错误"
            return JsonResponse(response)
    else:
        return redirect("/personal/")

# 随机图片验证码
def get_valid_code(request):
    # 随机字母数字
    def rndChar():
        char_num = random.randint(0, 9)
        # 大写字母
        char_upper = chr(random.randint(65, 90))
        # 小写字母
        char_lower = chr(random.randint(97, 122))
        # 随机抽取一个数字或字母
        char_str = str(random.choice([char_num, char_upper, char_lower]))
        return char_str

    # 随机颜色1,颜色淡
    def rndColor1():
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    # 随机颜色2,颜色深
    def rndColor2():
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    # 创建image对象,就是画纸
    width = 60 * 5
    height = 60
    image = Image.new('RGB', (width, height), rndColor1())
    # 创建font对象,用来选择字体
    font = ImageFont.truetype(r"static/font/calligraph421-bt-roman.woff.ttf", 40)
    # 创建draw对象,就是画板
    draw = ImageDraw.Draw(image)

    # 输出文字
    random_code = ''
    for t in range(5):
        # 写入的随机数字字母
        char_str = rndChar()
        # 元组参数是写入的位置,x,y轴,char_str输入的文字,font字体,fill背景颜色
        draw.text((60 * t + 10, 5), char_str, font=font, fill=rndColor2())
        random_code += char_str

    # 划线
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        # x1, y1, x2, y2分别是线的开始位置和结束位置坐标
        draw.line((x1, y1, x2, y2), fill=rndColor1())

    # 画点
    for i in range(30):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor1())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor1())

    # 验证码保存到session中
    request.session['valid_code'] = random_code
    # 将图片保存到内存中
    f = BytesIO()
    image.save(f, 'jpeg')
    data = f.getvalue()
    return HttpResponse(data)