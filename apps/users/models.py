from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class UserInfo(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    birth_day = models.DateTimeField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(("male", '男'), ("female", '女')),
                              default='male', verbose_name='性别')
    address = models.CharField(max_length=100, default='', verbose_name='地址')
    mobile = models.CharField(max_length=11, default='', verbose_name='手机号')
    image = models.ImageField(max_length=100, upload_to='images/%Y/%m', default='/images/default.png',
                              verbose_name='头像')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=40, verbose_name='邮箱')
    send_type = models.CharField(choices=(('register', '注册'), ('forget', '找回密码'), ('email_update', '邮箱修改')),
                                 max_length=20, verbose_name='验证码类型')
    send_time = models.DateTimeField(verbose_name='发送时间', default=datetime.now)

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     return self.email


class PictureBanner(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    image = models.ImageField(max_length=200, upload_to='banner/%Y/%m', verbose_name='图片')
    url = models.URLField(max_length=100, verbose_name='地址链接')
    index = models.IntegerField(default=100, verbose_name='顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
