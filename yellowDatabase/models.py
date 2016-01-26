from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.contrib.auth.models import User

@python_2_unicode_compatible
class Persona(models.Model):
    full_name= models.CharField(max_length=64, editable=False)
    expaID = models.PositiveIntegerField(unique=True, null=True) 
    cedula = models.PositiveIntegerField(unique=True, null=True) 
    direccion = models.CharField(max_length=128, null=True)
    telefono = models.CharField(max_length=32, null=True)
    universidad = models.ForeignKey('Universidad', models.PROTECT, null=True, related_name='estudiantes')
    carrera = models.CharField(max_length=32, null=True)
    fecha_nacimiento = models.DateField(null=True)
    user = models.OneToOneField(User, models.CASCADE)
    def __str__(self):
        return full_name


class Universidad(models.Model):
    nombre = models.CharField(max_length=64)
    direccion = models.CharField(max_length=128)
    def __str__(self):
        return nombre 


