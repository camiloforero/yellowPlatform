# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-19 00:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yellowAnalytics', '0025_auto_20160918_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlygoal',
            name='approved',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='monthlygoal',
            name='realized',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
