#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
"""
    Time    : 2018/4/12 12:27
    Author  : LeeLong
    File    : adminx.py.py
    Software: PyCharm
    Description:
"""
import xadmin
from .models import EmailVerifyRecord, PictureBanner
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = 'iMooc学习网后台管理系统'
    site_footer = 'iMooc学习网'
    menu_style = 'accordion'


#  在后台注册邮箱验证管理功能
class EmailVerifyRecordAdmin(object):
    # 验证码字段后台管理显示
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 后台添加搜索功能
    search_fields = ['code', 'email', 'send_type']
    # 过滤器筛选
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fas fa-envelope'


class PictureBannerAdmin(object):
    # 轮播图字段后台管理显示
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    # 后台添加搜索功能
    search_fields = ['title', 'image', 'url', 'index']
    # 过滤器筛选
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(PictureBanner, PictureBannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
