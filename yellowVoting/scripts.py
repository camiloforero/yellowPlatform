#encoding:utf-8
from __future__ import unicode_literals

import random
from . import models

def generar_plenos(numPlenos):
    #Primero se borran todos los plenos actuales
    models.PlenoDerecho.objects.all().delete()
    #Luego se vuelven a generar con un rango de 1000 a 9999
    for codigo in random.sample(xrange(1000, 9999), numPlenos):
        nuevoPleno = models.PlenoDerecho(codigo=codigo)
        nuevoPleno.save()
    
