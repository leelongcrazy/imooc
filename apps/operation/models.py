from datetime import datetime

from django.db import models

# Create your models here.
from courses.models import Course
from users.models import UserInfo


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name='用户名')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    course_name = models.CharField(max_length=50, verbose_name='课程名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name


class CourseComment(models.Model):
    user = models.ForeignKey(UserInfo, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')
    comment = models.CharField(max_length=200, verbose_name='课程评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserInfo, verbose_name='用户')
    fav_id = models.IntegerField(default=0, verbose_name='课程数据id')
    fav_type = models.IntegerField(default=1, choices=((1, '课程'), (2, '机构'), (3, '老师')), verbose_name='收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name='接收用户')
    message = models.CharField(max_length=200, verbose_name='消息内容')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    has_read = models.BooleanField(default=False, verbose_name='是否已读')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserInfo, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name
