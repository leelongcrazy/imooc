#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
"""
    Time    : 2018/4/12 13:24
    Author  : LeeLong
    File    : adminx.py
    Software: PyCharm
    Description:
"""
import xadmin
from courses.models import Course, BannerCourse, Lesson, Videos, CourseResource


class LessonInline(object):
    # 在课程管理页面可进行章节信息的添加
    model = Lesson
    extra = 0


class CourseAdmin(object):
    # 后台管理显示字段列表
    list_display = ['name', 'desc', 'course_type', 'course_org', 'teacher', 'get_lesson_nums', 'learn_times',
                    'students', 'like_numbers', 'is_banner', 'add_time']
    # 后台可以筛选的字段
    list_filter = ['name', 'desc', 'detail', 'difficulty', 'students', 'like_numbers',
                   'image', 'click_numbers', 'add_time']
    # 筛选作用字段
    search_fields = ['name', 'desc', 'detail', 'difficulty', 'learn_times', 'students',
                     'like_numbers', 'image', 'click_numbers', 'add_time']
    # 按点击量降序排列显示
    ordering = ['-click_numbers']
    # 设置只读字段
    readonly_fields = ['click_numbers', 'add_time']
    # 设置字段不显示
    excluded = ['like_numbers']
    # 在课程管理页面可进行章节信息的添加
    inlines = [LessonInline]
    # 设置字段可以在管理课程列表页面直接修改
    list_editable = ['desc', 'difficulty']
    # 设置管理页面自动刷新
    refresh_times = [3, 5]
    # style_fields = {'detail': 'ueditor'}

    def queryset(self):
        # 过滤非轮播课程
        qset = super(CourseAdmin, self).queryset()
        return qset.filter(is_banner=False)

    def save_model(self):
        # 保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()

        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class BannerCourseAdmin(object):
    # 后台管理显示字段列表
    list_display = ['name', 'desc', 'course_type', 'course_org', 'teacher', 'learn_times',
                    'students', 'like_numbers', 'is_banner', 'add_time']
    # 后台可以筛选的字段
    list_filter = ['name', 'desc', 'detail', 'difficulty', 'students', 'like_numbers',
                   'image', 'click_numbers', 'add_time']
    # 筛选作用字段
    search_fields = ['name', 'desc', 'detail', 'difficulty', 'learn_times', 'students',
                     'like_numbers', 'image', 'click_numbers', 'add_time']
    # 按点击量降序排列显示
    ordering = ['-click_numbers']
    # 设置只读字段
    readonly_fields = ['click_numbers', 'add_time']
    # 设置字段不显示
    excluded = ['like_numbers']
    # 在课程管理页面可进行章节信息的添加
    inlines = [LessonInline]
    # 设置管理页面自动刷新
    refresh_times = [3, 5]

    def queryset(self):
        # 过滤轮播课程
        qset = super(BannerCourseAdmin, self).queryset()
        return qset.filter(is_banner=True)


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    list_filter = ['course__name', 'name', 'add_time']
    search_fields = ['course', 'name']


class VideosAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    list_filter = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    list_filter = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Videos, VideosAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
