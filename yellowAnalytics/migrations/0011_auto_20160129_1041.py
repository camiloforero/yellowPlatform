# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-29 15:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yellowAnalytics', '0010_lc_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lc',
            old_name='total',
            new_name='totalRE',
        ),
    ]
