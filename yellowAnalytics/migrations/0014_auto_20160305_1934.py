# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-06 00:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yellowAnalytics', '0013_auto_20160305_1924'),
    ]

    operations = [
        migrations.RenameField(
            model_name='monthlygoal',
            old_name='goal',
            new_name='MA',
        ),
        migrations.AddField(
            model_name='monthlygoal',
            name='RE',
            field=models.PositiveSmallIntegerField(default=4),
            preserve_default=False,
        ),
    ]
