# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-14 12:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20180412_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='org_type',
            field=models.CharField(choices=[('jg', '培训机构'), ('gr', '个人'), ('gx', '高校')], default='jg', max_length=2),
        ),
    ]
