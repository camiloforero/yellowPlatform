# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-06 00:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yellowAnalytics', '0012_lc_totalma'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogrosPrograma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MA', models.PositiveSmallIntegerField()),
                ('RE', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MonthlyGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.PositiveSmallIntegerField()),
                ('goal', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('name', models.CharField(max_length=64, unique=True)),
                ('expaID', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('superoffice', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='suboffices', to='yellowAnalytics.Office')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('name', models.CharField(max_length=8, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='metasemana',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='metasemana',
            name='programa',
        ),
        migrations.DeleteModel(
            name='MetaSemana',
        ),
        migrations.AddField(
            model_name='monthlygoal',
            name='office',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_goals', to='yellowAnalytics.Office'),
        ),
        migrations.AddField(
            model_name='monthlygoal',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_goals', to='yellowAnalytics.Program'),
        ),
        migrations.AddField(
            model_name='logrosprograma',
            name='office',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logros', to='yellowAnalytics.Office'),
        ),
        migrations.AddField(
            model_name='logrosprograma',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logros', to='yellowAnalytics.Program'),
        ),
        migrations.AlterUniqueTogether(
            name='monthlygoal',
            unique_together=set([('month', 'program', 'office')]),
        ),
        migrations.AlterUniqueTogether(
            name='logrosprograma',
            unique_together=set([('program', 'office')]),
        ),
    ]