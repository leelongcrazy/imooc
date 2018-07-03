# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-12 15:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='联系地址'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='click_num',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='点击数'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='like_num',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='收藏数'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='所属机构'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='points',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='教学特点'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='work_company',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='公司'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='work_position',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='职位'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='work_year',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='工作年限'),
        ),
    ]
