# coding=utf-8
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models

@python_2_unicode_compatible
class PlenoDerecho(models.Model):
    codigo = models.CharField(max_length=8, primary_key=True)
    def __str__(self):
        return self.codigo

@python_2_unicode_compatible
class Mocion(models.Model):
    nombre = models.CharField(max_length=64)
    texto = models.TextField()
    asamblea = models.CharField(max_length=8)
    def __str__(self):
        return self.nombre + ' ' + self.asamblea

@python_2_unicode_compatible
class Voto(models.Model):
    VOTING_CHOICES = (
        ('A', 'En abstención'),
        ('B', 'En blanco'),
        ('C', 'En contra'),
        ('F', 'A favor'),
        )
    votante = models.ForeignKey(PlenoDerecho, models.CASCADE)
    mocion = models.ForeignKey(Mocion, models.CASCADE)
    votacion = models.CharField(max_length=1, choices=VOTING_CHOICES)
    def __str__(self):
        return str(self.mocion) + ' ' + str(self.votacion) 

# Create your models here.
