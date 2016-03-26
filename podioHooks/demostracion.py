# code TODO utf8
from django_podio import api
import pdb

def run(appID, params):
    testApi = api.PodioApi(appID)
    item = testApi.getItem(params['item_id'])
    pdb.set_trace()

    return 'success %s' % item['values']['mailprueba'] 
        
