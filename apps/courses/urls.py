#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
"""
    Time    : 2018/4/15 16:18
    Author  : LeeLong
    File    : urls.py
    Software: PyCharm
    Description:
"""


from django.conf.urls import url

from .views import CourseHomeView, CourseDetailView, CourseVideoView, CourseCommentView, AddCommentView

urlpatterns = [
    url(r'^list/$', CourseHomeView.as_view(), name='course_home'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^video/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name='course_video'),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
    url(r'^addcomment/$', AddCommentView.as_view(), name='add_comment'),
    # url(r'^tlist/$', TeacherListView.as_view(), name='teacher_list'),

]