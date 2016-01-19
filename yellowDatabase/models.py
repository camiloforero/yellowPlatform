from __future__ import unicode_literals

from django.db import models

class Persona(models.Model):
    full_name= models.CharField(max_length=64, editable=False)
    expaId = models.PositiveIntegerField(unique=True, null=True) 
    cedula = models.PositiveIntegerField(unique=True, null=True) 
    direccion = models.CharField(max_length=128, null=True)
    telefono = models.CharField(max_length=32, null=True)
    universidad = models.ForeignKey('Universidad', models.PROTECT, null=True)
    carrera = models.CharField(max_length=32, null=True)
    fecha_nacimiento = models.DateField(null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE)
    def __unicode__(self):
        return full_name


class Universidad(models.Model):
    nombre = models.CharField(max_length=64)
    direccion = models.CharField(max_length=128)


