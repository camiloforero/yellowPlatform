# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-22 16:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yellowVoting', '0004_auto_20160416_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voto',
            name='mocion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votos', to='yellowVoting.Mocion'),
        ),
    ]
