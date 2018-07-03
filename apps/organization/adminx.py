#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
"""
    Time    : 2018/4/12 14:31
    Author  : LeeLong
    File    : adminx.py
    Software: PyCharm
    Description:
"""
import xadmin

from .models import Teacher, CourseOrg, Cities


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'address', 'city', 'click_num', 'like_num', 'add_time']
    list_filter = ['name', 'desc', 'address', 'city', 'click_num', 'like_num', 'add_time']
    search_fields = ['name', 'desc', 'address', 'city', 'click_num', 'like_num']
    # 设置外键以ajax方式请求, 后台有外键连接过来可进行搜索
    # relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    list_display = ['name', 'org', 'work_year', 'work_company', 'work_position', 'points',
                    'click_num', 'like_num', 'add_time']
    list_filter = ['name', 'org', 'work_year', 'work_company', 'work_position', 'points', 'click_num', 'like_num',
                   'add_time']
    search_fields = ['name', 'org', 'work_year', 'work_company', 'work_position', 'points', 'click_num', 'like_num']


class CitiesAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    list_filter = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']


xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(Cities, CitiesAdmin)
