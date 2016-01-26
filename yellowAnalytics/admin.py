# coding=utf-8
from django.contrib import admin
from .models import MetaPrograma, MetaSemana, LC

@admin.register(MetaPrograma)
class MetaProgramaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'metaTotal')

@admin.register(MetaSemana)
class MetaSemanaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'meta')

@admin.register(LC)
class LCAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'mc', 'ogcdpMA', 'ogcdpRE', 'igcdpMA', 'igcdpRE', 'ogipMA', 'ogipRE', 'igipMA', 'igipRE')



