#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
"""
    Time    : 2018/4/14 18:29
    Author  : LeeLong
    File    : urls.py
    Software: PyCharm
    Description:
"""
from django.conf.urls import url

from .views import OrgListView, UserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeachView, OrgUserFavoriteView,\
    TeacherListView

urlpatterns = [
    # 机构列表首页
    url(r'^list/$', OrgListView.as_view(), name='org_list'),
    # 用户咨询表单
    url(r'^userask/$', UserAskView.as_view(), name='user_ask'),
    # 机构首页
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    # 机构课程页
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    # 机构描述页
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    # 机构讲师页
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeachView.as_view(), name='org_teach'),
    # 用户机构收藏处理功能
    url(r'^favorite/$', OrgUserFavoriteView.as_view(), name='favorite'),

    # 讲师列表页
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
]