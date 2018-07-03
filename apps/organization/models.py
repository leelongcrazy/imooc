from datetime import datetime

from django.db import models


# Create your models here.


class Cities(models.Model):
    """
    城市信息
    """
    name = models.CharField(max_length=20, verbose_name='城市名字')
    desc = models.CharField(max_length=100, verbose_name='城市描述', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    """
    课程机构信息
    """
    name = models.CharField(max_length=50, verbose_name='课程机构')
    org_type = models.CharField(max_length=2, verbose_name='机构类别', choices=(('jg', '培训机构'), ('gr', '个人'), ('gx', '高校')),
                                default='jg')
    desc = models.TextField(verbose_name='机构介绍')
    click_num = models.IntegerField(default=500, verbose_name='点击数')
    like_num = models.IntegerField(default=500, verbose_name='收藏数')
    students = models.IntegerField(default=500, verbose_name='学习人数')
    course_nums = models.IntegerField(default=0, verbose_name='课程数量')
    image = models.ImageField(max_length=200, verbose_name='描述图片', upload_to='org/%Y/%m', null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name='联系地址', null=True, blank=True)
    tag = models.CharField(max_length=10, verbose_name='机构标签',default='学术一流', null=True, blank=True)
    city = models.ForeignKey(Cities, verbose_name='所在城市', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=20, verbose_name='教师名字')
    org = models.ForeignKey(CourseOrg, verbose_name='所属机构', null=True, blank=True)
    work_year = models.IntegerField(default=5, verbose_name='工作年限', null=True, blank=True)
    work_company = models.CharField(max_length=50, verbose_name='公司', null=True, blank=True)
    work_position = models.CharField(max_length=50, verbose_name='职位', null=True, blank=True)
    points = models.CharField(max_length=150, verbose_name='教学特点', null=True, blank=True)
    click_num = models.IntegerField(default=1000, verbose_name='点击数', null=True, blank=True)
    like_num = models.IntegerField(default=1000, verbose_name='收藏数', null=True, blank=True)
    image = models.ImageField(max_length=200, verbose_name='头像', upload_to='teacher/%Y/%m', null=True,
                              blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_nums(self):
        return self.course_set.all().count()
