# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-15 20:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_course_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_tag',
            field=models.CharField(default='', max_length=10, verbose_name='课程标签'),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_type',
            field=models.CharField(default='', max_length=10, verbose_name='课程类别'),
        ),
    ]
