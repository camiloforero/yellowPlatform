# coding=utf-8
from django.contrib import admin
from .models import Persona, Universidad

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'expaID')

@admin.register(Universidad)
class UniversidadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)


# Register your models here.
