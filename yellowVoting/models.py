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
    texto = models.TextField(null=True, blank=True)
    asamblea = models.CharField(max_length=8)
    grupo = models.PositiveSmallIntegerField(default=0)
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
    votante = models.ForeignKey(PlenoDerecho, models.CASCADE, related_name="votos")
    mocion = models.ForeignKey(Mocion, models.CASCADE, related_name="votos")
    votacion = models.CharField(max_length=1, choices=VOTING_CHOICES, blank=False)
    def __str__(self):
        return "%s %s" % (self.mocion, self.votacion)
    class Meta:
        unique_together = ("votante", "mocion")

@python_2_unicode_compatible
class Candidato(models.Model):
    nombre = models.CharField(max_length=64)
    foto = models.ImageField(null=True, blank=True)
    asamblea = models.CharField(max_length=8)
    def __str__(self):
        return "%s" % (self.nombre)

@python_2_unicode_compatible
class VotoCandidato(models.Model):
    VOTING_CHOICES = (
        ('N', 'No confianza'),
        ('C', 'Confianza'),
        )
    votante = models.ForeignKey(PlenoDerecho, models.CASCADE, related_name="votosCandidatos")
    candidato = models.ForeignKey(Candidato, models.CASCADE, related_name="votosCandidatos")
    votacion = models.CharField(max_length=1, choices=VOTING_CHOICES, blank=False)
    def __str__(self):
        return "%s %s" % (self.candidato, self.votacion)
    class Meta:
        unique_together = ("votante", "candidato")
