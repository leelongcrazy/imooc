# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-12 13:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': '课程章节', 'verbose_name_plural': '课程章节'},
        ),
    ]
