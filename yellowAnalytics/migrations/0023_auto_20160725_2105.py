# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-26 02:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yellowAnalytics', '0022_auto_20160725_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='role',
            field=models.CharField(help_text='El rol que esa persona desempe\xf1a en la organizaci\xf3n', max_length=128, verbose_name='Rol'),
        ),
    ]
