# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-22 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yellowAnalytics', '0007_auto_20160122_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lc',
            name='igcdpMA',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='lc',
            name='igcdpRE',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='lc',
            name='igipMA',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='lc',
            name='igipRE',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='lc',
            name='ogcdpMA',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Matches OGCDP'),
        ),
        migrations.AlterField(
            model_name='lc',
            name='ogcdpRE',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='lc',
            name='ogipMA',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='lc',
            name='ogipRE',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
