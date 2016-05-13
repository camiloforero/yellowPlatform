# encoding:utf-8
from __future__ import unicode_literals
from django_podio import api
import pdb

def run(appID, params, hook=None):
    podioApi = api.PodioApi(appID, client=True)
    item = podioApi.get_item(params['item_id'], external_id=False)
    if item['values'][120840533]['value'] == 'Si':
        transformer = [
            ('120839833#120914599', 113795330), #Nombre del trainee
            ('120839833#120836241', 113795330), #Email del trainee
            ('120839833#120335070', 113795331), #EP Id, o EXPA Code
            ('120839833#120335071', 113795337), #Opportunity ID
            (120839834, 113795332), #Number of exchanges 
            (120839835, 113795335), #Skype ID
            (120839836, 113795336), #Facebook link
            (122096055, 113798817), #Tipo de documento
            (122096056, 113795341), #ID del documento
            (122096169, 113795344), #Fecha de viaje
            (122096170, 113795345), #Fecha de refreso
            (120839839, 113795344), #Día de comienzo del intercambio
            (120839837, 113795338), #Contacto en Colombia
            (120839838, 113795340), #Contacto en el exterior
            (120839840, 113795346), #Canal de coumunicación
            (120839842, 113795348), #Pasaporte o cédula escaneados
            (120839843, 113795349), #Seguro internacional
            (120839844, 113798819), #Visa
            (120839841, 113795347), #Documentos adjuntos
            (120839845, 113795350), #Seguro internacional de ASSIST Card?
            (122096171, 113799877), #Autorizo a AIESEC en Colombia
        ]
        extra_data = {
            113795333:1  #Para que el comité local sea Andes
        }
            
        ans = podioApi.copy_item(params['item_id'], 14817837, transformer, extra_data)
        return ans
        
