#coding = utf-8
from __future__ import unicode_literals

from django import forms
from . import models

class VotoForm(forms.ModelForm):
    class Meta:
        model = models.Voto
        fields = ['mocion', 'votacion']
        widgets={'mocion': forms.HiddenInput}

