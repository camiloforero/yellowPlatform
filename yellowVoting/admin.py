# coding=utf-8
from django.contrib import admin
from .models import Mocion, Voto, PlenoDerecho

@admin.register(Mocion)
class MocionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'asamblea')

@admin.register(Voto)
class VotoAdmin(admin.ModelAdmin):
    list_display = ('votante', 'mocion', 'votacion')
    readonly_fields = ('votacion', )

@admin.register(PlenoDerecho)
class PlenoDerechoAdmin(admin.ModelAdmin):
    list_display = ('codigo',)

# Register your models here.
