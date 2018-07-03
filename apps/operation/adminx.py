#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
"""
    Time    : 2018/4/12 14:44
    Author  : LeeLong
    File    : adminx.py
    Software: PyCharm
    Description:
"""
import xadmin

from .models import UserAsk, UserCourse, UserMessage, UserFavorite, CourseComment


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    list_filter = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']


xadmin.site.register(UserCourse, UserCourseAdmin)


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']


xadmin.site.register(UserAsk, UserAskAdmin)


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']


xadmin.site.register(UserFavorite, UserFavoriteAdmin)


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    list_filter = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']


xadmin.site.register(UserMessage, UserMessageAdmin)


class CourseCommentAdmin(object):
    list_display = ['user', 'course', 'comment', 'add_time']
    list_filter = ['user', 'course', 'comment', 'add_time']
    search_fields = ['user', 'course', 'comment']


xadmin.site.register(CourseComment, CourseCommentAdmin)
