# coding=utf-8
from django.contrib import admin
from .models import MetaPrograma, MonthlyGoal, LC

@admin.register(MetaPrograma)
class MetaProgramaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'metaTotal')

@admin.register(MonthlyGoal)
class MonthlyGoalAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'MA', 'RE')

@admin.register(LC)
class LCAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'mc', 'ogcdpMA', 'ogcdpRE', 'igcdpMA', 'igcdpRE', 'ogipMA', 'ogipRE', 'igipMA', 'igipRE')



