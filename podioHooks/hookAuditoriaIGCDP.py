# encoding:utf-8
from django_podio import api
import pdb

def run(appID, params, hook=None):
    podioApi = api.PodioApi(appID, client=True)
    item = podioApi.get_item(params['item_id'], external_id=False)
    if item['values'][50175872]['value'] == 'Social' and item['values'][117107512]['value'] == 'Si':
        transformer = [
            (44389815, 113794808), #Nombre del trainee
            (51046438, 113794809), #Email
            (44389816, 113794810), #EP Id, o EXPA Code
            (117106118, 113794811), #TN-ID
            (50175085, 113796635), #Fecha de llegada a Colombia
            (117106119, 113794814), #Fecha de realización
            (117106120, 113794815), #Fecha de finalización
            (44389821, 113794816), #Pasaporte
            (50175084, 113794817), #Pasaporte con estampado de la visa
            (44389822, 113794818), #Seguro internacional
            (50174533, 113794819), #Memodeal
        ]
        extra_data = {
            113794813:1, #TODO es un campo de categoría, probablemente LC
            113796330:1 #TODO qué es esto? Es un campo de categoría, pero no sabría cual
        }
            
        ans = podioApi.copy_item(params['item_id'], 14817777, transformer, extra_data)
        return ans
        
