# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-29 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yellowAnalytics', '0011_auto_20160129_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='lc',
            name='totalMA',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
