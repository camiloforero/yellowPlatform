# coding: utf-8
from django_podio import api, tools
import pdb

def run(appID, params, hook=None):
    podioApi = api.PodioApi(appID, client=True)
    item = podioApi.get_item(params['item_id'], external_id=False)
    print item
    transformer = {
        '118632836#117779491':'118634506',#Area
        '118632836#117701833':'119050124',#TMP, TLP o EB
    }
    new_dict = tools.dictSwitch(item['values'], {}, transformer, ignore_unknown = True)
    ans = podioApi.updateItem(params['item_id'], new_dict)
    return ans
        
