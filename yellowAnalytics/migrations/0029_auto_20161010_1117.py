# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-10 16:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yellowAnalytics', '0028_monthlygoal_year'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='monthlygoal',
            unique_together=set([('month', 'year', 'program', 'office')]),
        ),
    ]
