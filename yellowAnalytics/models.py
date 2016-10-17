# coding:utf-8
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
    totalMA = models.PositiveSmallIntegerField(default=0)
    totalRE = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.totalMA = self.ogcdpMA + self.ogipMA + self.igcdpMA + self.igipMA
        self.totalRE = self.ogcdpRE + self.ogipRE + self.igcdpRE + self.igipRE
        super(LC, self).save(*args, **kwargs)

@python_2_unicode_compatible
class Program(models.Model):
    name = models.CharField(max_length=8, primary_key=True)
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Office(models.Model):
    """
    This class represents an office, any kind of office. Is a more general version of the previous MC, LC and Region division, and is meant to eventually replace them everywhere
    """
    name = models.CharField(max_length=64, unique=True)
    expaID = models.PositiveIntegerField(primary_key=True)
    office_type = models.CharField(max_length=8)
    superoffice = models.ForeignKey('Office', models.SET_NULL, related_name='suboffices', null=True)
    scoreboard_enabled = models.BooleanField("Este campo representa si el scoreboard está habilitado para esta entidad o no", default=False)
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class LogrosPrograma(models.Model):
    """
    This class represents an LCs accomplishments from the beginning of the year
    """
    program = models.ForeignKey(Program, models.CASCADE, related_name='logros')
    office = models.ForeignKey(Office, models.CASCADE, related_name='logros')
    approved = models.PositiveSmallIntegerField()
    realized = models.PositiveSmallIntegerField()
    def __str__(self):
        return unicode(self.program) + ' ' + unicode(self.office)
    class Meta:
        unique_together = ('program', 'office')

@python_2_unicode_compatible
class MonthlyGoal(models.Model):
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    approved = models.PositiveSmallIntegerField(null=True)
    realized = models.PositiveSmallIntegerField(null=True)
    program = models.ForeignKey(Program, models.CASCADE, related_name='monthly_goals')
    office = models.ForeignKey(Office, models.CASCADE, related_name='monthly_goals')
    def __str__(self):
        return 'Meta: ' + self.program_id + ' - Mes ' + str(self.month) + ' - Año: ' + str(self.year)
    class Meta:
        unique_together = ('month', 'year', 'program', 'office')

@python_2_unicode_compatible
class MonthlyAchievement(models.Model):
    month = models.PositiveSmallIntegerField()
    approved = models.PositiveSmallIntegerField(null=True)
    realized = models.PositiveSmallIntegerField(null=True)
    program = models.ForeignKey(Program, models.CASCADE, related_name='monthly_achievements')
    office = models.ForeignKey(Office, models.CASCADE, related_name='monthly_achievements')
    def __str__(self):
        return 'Logro: ' + self.program_id + ' - Mes ' + str(self.month)
    class Meta:
        unique_together = ('month', 'program', 'office')

@python_2_unicode_compatible
class YearlyGoal(models.Model):
    MA = models.PositiveSmallIntegerField()
    RE = models.PositiveSmallIntegerField()
    program = models.ForeignKey(Program, models.CASCADE, related_name='yearly_goals')
    office = models.ForeignKey(Office, models.CASCADE, related_name='yearly_goals')
    def __str__(self):
        return self.program_id + ' - Meta anual'
    class Meta:
        unique_together = ('program', 'office')

@python_2_unicode_compatible
class Member(models.Model):
    office = models.ForeignKey(Office, models.CASCADE, related_name='members')
    expaID = models.PositiveIntegerField("Expa ID", primary_key=True)
    name = models.CharField("Nombre", max_length=128, help_text="El nombre compleeto del miembro")
    role = models.CharField("Rol", max_length=128, help_text="El rol que esa persona desempeña en la organización")
    phone = models.CharField("Teléfono", max_length=32, help_text="EL número telefónico", null=True)
    email = models.CharField("Correo", max_length=64, help_text="El correo electrónico", null=True)
    alt_email = models.CharField("Correo alternativo", max_length=64, help_text="El correo electrónico", null=True)
    facebook = models.CharField("Facebook", max_length=64, help_text="El facebook", null=True)
    
    def __str__(self):
        return self.name + ' :' + self.office.name
