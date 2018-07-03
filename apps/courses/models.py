# coding:utf-8
from datetime import datetime

from django.db import models

# Create your models here.
from DjangoUeditor.models import UEditorField

#  课程信息
from organization.models import CourseOrg, Teacher


class Course(models.Model):
    """
    课程信息
    """
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True, blank=True)
    teacher = models.ForeignKey(Teacher, default='', verbose_name='课程老师', null=True, blank=True)
    name = models.CharField(max_length=20, verbose_name='课程名称')
    course_type = models.CharField(max_length=10, verbose_name='课程类别', default='', null=True, blank=True)
    desc = models.CharField(max_length=50, verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    difficulty = models.CharField(choices=(('low', '初级'), ('mid', '中级'), ('high', '高级')),
                                  max_length=4, verbose_name='学习难度')
    learn_times = models.IntegerField(default=0, verbose_name='学习时间(分钟)')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    like_numbers = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(max_length=200, verbose_name='描述图片', upload_to='courses/%Y/%m')
    click_numbers = models.IntegerField(default=0, verbose_name='点击数量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播显示')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_lesson_nums(self):
        return self.lesson_set.all().count()

    # 在后台管理页面设置 get_lesson_nums 函数显示的别名
    get_lesson_nums.short_description = '章节数量'

    def relate_courses(self):
        return self.objects.filter(course_type=self.course_type).all()

    def __str__(self):
        return self.name


class BannerCourse(Course):
    # 轮播图课程，继承于上面的 Course
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True  # 不生成新的数据表


class Lesson(models.Model):
    """
    课程章节信息
    """
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=50, verbose_name='章节名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_videos(self):
        """
        获取该章节的所有视频
        :return: videos list
        """
        return self.videos_set.all()


class Videos(models.Model):
    """
    每章节的视频信息
    """
    lesson = models.ForeignKey(Lesson, verbose_name='章节名称')
    name = models.CharField(max_length=50, verbose_name='视频名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    """
    右侧资源链接
    """
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=50, verbose_name='视频名称')
    download = models.FileField(max_length=100, upload_to='courses/resource/%Y/%m', verbose_name='课程资源')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
