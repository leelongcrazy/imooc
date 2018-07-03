#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
"""
    Time    : 2018/4/18 11:24
    Author  : LeeLong
    File    : urls.py
    Software: PyCharm
    Description:
"""
from django.conf.urls import url

from .views import UserCenterView, UserCenterMyCourseView, UserCenterMessageView, UserCenterFavCourseView,\
    SendEmailCodeView, UpdateEmailView, UploadImageView, UpdatePwdView, UserCenterFavOrgView, UserCenterFavTeacherView

urlpatterns = [
    # 个人信息主页
    url(r'^info/$', UserCenterView.as_view(), name='user_center'),

    # 个人课程
    url(r'^course/$', UserCenterMyCourseView.as_view(), name='user_course'),

    # 消息页面
    url(r'^message/$', UserCenterMessageView.as_view(), name='user_message'),

    # 收藏课程
    url(r'^fav/course/$', UserCenterFavCourseView.as_view(), name='user_fav_course'),

    # 课程机构收藏
    url(r'^fav/org/$', UserCenterFavOrgView.as_view(), name='user_fav_org'),

    # 老师收藏
    url(r'^fav/teacher/$', UserCenterFavTeacherView.as_view(), name='user_fav_teacher'),

    # 头像修改
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),

    # 密码重设
    url(r'^resetpwd/$', UpdatePwdView.as_view(), name='update_pwd'),

    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='send_email_code'),

    # 邮箱更改页面
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    ]