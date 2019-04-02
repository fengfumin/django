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
from django.conf.urls import url
from django.shortcuts import HttpResponse, render, redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.forms import ModelForm
from stark.utils.pagination import Pagination
from django.db.models import Q


class ShowList(object):
    def __init__(self, config_obj, queryset, request):
        self.config_obj = config_obj
        self.request = request
        self.queryset = queryset
        # 分页功能三行代码
        current_page = self.request.GET.get("page", 1)
        self.page_obj = Pagination(current_page=current_page, all_count=self.queryset.count(), params=self.request.GET)
        self.page_queryset = self.queryset[self.page_obj.start:self.page_obj.end]

    def get_header(self):
        # 表头展示
        head_list = []
        for head in self.config_obj.get_new_list_display():
            if isinstance(head, str):
                # 如果list_display里有字符串,并且是__str__,那就返回数据表名大写
                if head == "__str__":
                    val = self.config_obj.model._meta.model_name.upper()
                else:
                    # 否则就返回数据表中的verbose_name
                    val = self.config_obj.model._meta.get_field(head).verbose_name
            else:
                # 如果is_header是True,就返回"编辑","删除","选择"
                val = head(self.config_obj, is_header=True)
            head_list.append(val)
        return head_list

    def get_body(self):
        # 表单展示
        body_list = []
        for data in self.page_queryset:
            tmp = []
            for field_or_func in self.config_obj.get_new_list_display():
                if isinstance(field_or_func, str):
                    # 通过反射获取字段内容
                    val = getattr(data, field_or_func)
                    # 如果有list_display的字段在links中,那么就增加编辑的a标签编辑链接
                    if field_or_func in self.config_obj.list_display_links:
                        _url = self.config_obj.get_reverse_url("edit", data)
                        val = mark_safe("<a href='%s'>%s</a>" % (_url, val))
                else:
                    # 获取mark_safe的标签
                    val = field_or_func(self.config_obj, obj=data)
                tmp.append(val)
            body_list.append(tmp)

        return body_list

    def get_actions(self):
        tmp = []
        for action in self.config_obj.actions:
            tmp.append({
                "name": action.__name__,
                "desc": action.desc
            })
        return tmp

    def get_filter(self):
        tmp_dict = {}
        for field in self.config_obj.list_filter:
            tmp_list = []
            rel_model = self.config_obj.model._meta.get_field(field).rel.to
            rel_queryset = rel_model.objects.all()
            filter_value = self.request.GET.get(field)
            import copy
            params1 = copy.deepcopy(self.request.GET)
            if field in params1:
                params1.pop(field)
                s = mark_safe("<a href='?%s'>All</a>" % params1.urlencode())
            else:
                s = mark_safe("<a href=''>All</a>")
            tmp_list.append(s)

            params = copy.deepcopy(self.request.GET)
            for data in rel_queryset:
                params[field] = data.pk
                if filter_value == str(data.pk):
                    s = mark_safe("<a href='?%s' class='active'>%s</a>" % (params.urlencode(), str(data)))
                else:
                    s = mark_safe("<a href='?%s'>%s</a>" % (params.urlencode(), str(data)))
                tmp_list.append(s)
            tmp_dict[field] = tmp_list
        return tmp_dict


# 默认配置类
class ModelStark(object):
    # 定义一个配置信息
    list_display = ["__str__"]
    # 默认字段编辑链接
    list_display_links = []
    # 默认的modelform类
    model_form_class = None
    # 默认的搜素字段,空
    search_fields = []
    # 默认的批量操作,空
    actions = []
    # 默认的外键字段过滤,空
    list_filter = []

    def __init__(self, model):
        self.model = model
        # 获取app名
        self.app_label = self.model._meta.app_label
        # 获取数据表名
        self.model_name = self.model._meta.model_name
        self.key_word = ""

    def get_reverse_url(self, type, obj=None):
        '''
        反向解析获取url
        :param type: list,add,edit,delete
        :param obj: 数据表中的每条记录对象
        :return:
        '''
        if obj:
            _url = reverse("%s_%s_%s" % (self.app_label, self.model_name, type), args=(obj.pk,))
        else:
            _url = reverse('%s_%s_%s' % (self.app_label, self.model_name, type))
        return _url

    def check_col(self, is_header=False, obj=None):
        if is_header:
            return "选择"
        return mark_safe("<input type='checkbox'/>")

    def edit_col(self, is_header=False, obj=None):
        if is_header:
            return "编辑"
        _url = self.get_reverse_url('edit', obj)
        return mark_safe('<a href="%s">编辑</a>' % _url)

    def delete_col(self, is_header=False, obj=None):
        if is_header:
            return "删除"
        _url = self.get_reverse_url('delete', obj)
        return mark_safe('<a href="%s">删除</a>' % _url)

    # 将list_display中添加新的函数功能
    def get_new_list_display(self):
        tmp = []
        tmp.append(ModelStark.check_col)
        tmp.extend(self.list_display)
        if not self.list_display_links:
            tmp.append(ModelStark.edit_col)
        tmp.append(ModelStark.delete_col)
        return tmp

    def get_search(self, request, queryset):
        key_word = request.GET.get("q")
        self.key_word = ""
        if key_word:
            self.key_word = key_word
            q = Q()
            q.connector = "or"
            for field in self.search_fields:
                q.children.append(("%s__icontains" % field, key_word))
            queryset = queryset.filter(q)
        return queryset

    def get_filter(self,request,queryset):
        q=Q()
        for filter_field in self.list_filter:
            if filter_field in request.GET:
                filter_val=request.GET.get(filter_field)
                q.children.append((filter_field,filter_val))
        queryset = queryset.filter(q)
        return queryset

    # 显示
    def list_view(self, request):
        # action功能
        if request.method == "POST":
            action = request.POST.get("action")
            if action:
                pk_list = request.POST.getlist("selected_action")
                queryset = self.model.objects.filter(pk_in=pk_list)
                real_action = getattr(self, action)
                real_action(request, queryset)

        queryset = self.model.objects.all()
        # search功能
        queryset = self.get_search(request, queryset)
        # filter功能
        queryset = self.get_filter(request, queryset)

        show_obj = ShowList(self, queryset, request)
        url = self.get_reverse_url("add")

        return render(request, 'stark/list_view.html', locals())

    def get_model_form_class(self):
        if self.model_form_class:
            return self.model_form_class

        class ModelFormClass(ModelForm):
            class Meta:
                model = self.model
                fields = "__all__"

            def __init__(self, *args, **kwargs):
                super(ModelFormClass,self).__init__(*args, **kwargs)
                # 统一给ModelForm生成字段添加样式
                for name, field in self.fields.items():
                    field.widget.attrs['class'] = 'form-control'

        return ModelFormClass

    # 新增
    def add_view(self, request):
        model_form_class = self.get_model_form_class()
        model_form_obj = model_form_class()
        if request.method == "POST":
            model_form_obj = model_form_class(request.POST)
            if model_form_obj.is_valid():
                model_form_obj.save()
                return redirect(self.get_reverse_url("list"))
        return render(request, 'stark/add.html', locals())

    # 修改
    def edit_view(self, request, id):
        model_form_class = self.get_model_form_class()
        edit_obj = self.model.objects.filter(pk=id).first()
        model_form_obj = model_form_class(instance=edit_obj)
        if request.method == "POST":
            model_form_obj = model_form_class(request.POST, instance=edit_obj)
            if model_form_obj.is_valid():
                model_form_obj.save()
                return redirect(self.get_reverse_url('list'))
        return render(request, 'stark/edit.html', locals())

    # 删除
    def delete_view(self, request):
        self.model.objects.filter(pk=id).delete()
        return redirect(self.get_reverse_url('list'))

    @property
    def urls(self):
        # 二次路由分发
        # print(self)这个self是ModelStark产生的对象
        tmp = [
            url(r'^$', self.list_view, name='%s_%s_list' % (self.app_label, self.model_name)),
            url(r'^add/', self.add_view, name='%s_%s_add' % (self.app_label, self.model_name)),
            url(r'^edit/(\d+)/', self.edit_view, name='%s_%s_edit' % (self.app_label, self.model_name)),
            url(r'^delete/(\d+)/', self.delete_view, name='%s_%s_delete' % (self.app_label, self.model_name))
        ]
        return tmp, None, None


class StarkSite(object):

    def __init__(self):
        self._registry = {}

    def register(self, model, admin_class=None, **options):
        if not admin_class:
            admin_class = ModelStark
        # 这里的model是app注册的数据库表,admin_class是配置类
        self._registry[model] = admin_class(model)

    def get_urls(self):
        tmp = []
        for model_class, config_obj in self._registry.items():
            print(config_obj)  # config_obj是配置类ModelStark产生的实例对象
            # 获取模型类(数据库表)的app名
            app_label = model_class._meta.app_label
            # 获取模型类的类名字
            model_name = model_class._meta.model_name
            # 拼接路由
            tmp.append(
                url(r"^%s/%s/" % (app_label, model_name), config_obj.urls)
            )
        return tmp

    @property
    def urls(self):
        return self.get_urls(), None, None


# 创建单例
site = StarkSite()
