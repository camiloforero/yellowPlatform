from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models

@python_2_unicode_compatible
class MetaPrograma(models.Model):
    programa = models.CharField(max_length=8, primary_key=True)
    metaTotal = models.PositiveSmallIntegerField()
    def __str__(self):
        return self.programa

@python_2_unicode_compatible
class MetaSemana(models.Model):
    semana = models.PositiveSmallIntegerField()
    meta = models.PositiveSmallIntegerField()
    programa = models.ForeignKey(MetaPrograma, models.CASCADE, related_name='metasSemanales')
    def __str__(self):
        return self.programa_id + ' - Semana ' + str(self.semana)
    class Meta:
        unique_together = ('semana', 'programa')

@python_2_unicode_compatible
class Region(models.Model):
    nombre = models.CharField(max_length=32, unique=True)
    expaID = models.PositiveIntegerField(primary_key=True)
    def __str__(self):
        return self.nombre

@python_2_unicode_compatible
class MC(models.Model):
    nombre = models.CharField(max_length=32, unique=True)
    expaID = models.PositiveIntegerField(primary_key=True)
    region = models.ForeignKey(Region, models.PROTECT, related_name='mcs')
    def __str__(self):
        return self.nombre

@python_2_unicode_compatible
class LC(models.Model):
    nombre = models.CharField(max_length=64, unique=True)
    expaID = models.PositiveIntegerField(primary_key=True)
    mc = models.ForeignKey(MC, models.PROTECT, related_name='lcs')
    ogcdpMA = models.PositiveSmallIntegerField('Matches OGCDP', default=0)
    igcdpMA = models.PositiveSmallIntegerField(default=0)
    ogipMA = models.PositiveSmallIntegerField(default=0)
    igipMA = models.PositiveSmallIntegerField(default=0)
    ogcdpRE = models.PositiveSmallIntegerField(default=0)
    igcdpRE = models.PositiveSmallIntegerField(default=0)
    ogipRE = models.PositiveSmallIntegerField(default=0)
    igipRE = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.nombre

@python_2_unicode_compatible
class LogrosPrograma(models.Model):
    programa = models.CharField(max_length=8, primary_key=True)
    logros = models.PositiveSmallIntegerField()
    lc = models.ForeignKey(LC, models.PROTECT, related_name='programas')
    def __str__(self):
        return self.programa

