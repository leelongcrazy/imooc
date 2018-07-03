# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-14 17:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_courseorg_org_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='course_nums',
            field=models.IntegerField(default=10, verbose_name='课程数量'),
        ),
        migrations.AddField(
            model_name='courseorg',
            name='students',
            field=models.IntegerField(default=500, verbose_name='学习人数'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='click_num',
            field=models.IntegerField(default=500, verbose_name='点击数'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='like_num',
            field=models.IntegerField(default=500, verbose_name='收藏数'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='org_type',
            field=models.CharField(choices=[('jg', '培训机构'), ('gr', '个人'), ('gx', '高校')], default='jg', max_length=2, verbose_name='机构类别'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='click_num',
            field=models.IntegerField(blank=True, default=1000, null=True, verbose_name='点击数'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='like_num',
            field=models.IntegerField(blank=True, default=1000, null=True, verbose_name='收藏数'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='work_year',
            field=models.IntegerField(blank=True, default=5, null=True, verbose_name='工作年限'),
        ),
    ]
