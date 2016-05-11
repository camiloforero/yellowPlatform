# encoding:utf-8
from __future__ import unicode_literals
from django_podio import api
import pdb

def run(appID, params, hook=None):
    podioApi = api.PodioApi(appID, client=True)
    item = podioApi.get_item(params['item_id'], external_id=False)
    if item['values'][120836970]['value'] == 'Si':
        transformer = [
            ('120335287#120914599', 114271376), #Nombre del trainee
            ('120335287#120335070', 114271380), #EP Id, o EXPA Code
            ('120335287#120335071', 114271381), #TN-ID
            (120335289, 114271385), #Cédula
            (120335855, 114271386), #Cédula escaneada
            (120335856, 114271387), #Fecha de inicio de la experiencia
            (120838710, 114271388), #Fecha de pago
            (120838711, 114271389), #Total pagado
            (120838712, 114271390), #FOto del recibo de pago
            (120838713, 114271396), #Seguro internacional
        ]
        extra_data = {
            114271377:1, #Para colocar el programa de OGCDP
            114271383:1  #Para que el comité local sea Andes
        }
            
        ans = podioApi.copy_item(params['item_id'], 14874570, transformer, extra_data)
        return ans
        
