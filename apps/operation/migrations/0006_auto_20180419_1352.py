# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-19 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0005_auto_20180419_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfavorite',
            name='fav_type',
            field=models.IntegerField(blank=True, choices=[(0, '机构'), (1, '课程'), (2, '老师')], default='o', null=True, verbose_name='收藏类型'),
        ),
    ]
