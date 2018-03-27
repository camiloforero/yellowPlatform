# coding=utf-8
from django.contrib import admin
from .models import MetaPrograma, MonthlyGoal, YearlyGoal, Office, Program, Member

@admin.register(MetaPrograma)
class MetaProgramaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'metaTotal')

@admin.register(YearlyGoal)
class YearlyGoalAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'MA', 'RE')

@admin.register(MonthlyGoal)
class MonthlyGoalAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'approved', 'realized',)

@admin.register(Office)
class LCAdmin(admin.ModelAdmin):
    list_display = ('name', 'expaID', 'office_type', 'superoffice')
    search_fields = ['name', 'office_type', 'superoffice__name']

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

admin.site.register(Member)
