# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-18 14:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_auto_20180416_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='teacher/%Y/%m', verbose_name='头像'),
        ),
    ]
