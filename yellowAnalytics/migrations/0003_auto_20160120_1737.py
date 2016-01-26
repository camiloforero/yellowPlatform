# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-20 22:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yellowAnalytics', '0002_auto_20160120_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaSemana',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semana', models.PositiveSmallIntegerField()),
                ('meta', models.PositiveSmallIntegerField()),
                ('programa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metasSemanales', to='yellowAnalytics.MetaPrograma')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='metasemana',
            unique_together=set([('semana', 'programa')]),
        ),
    ]
