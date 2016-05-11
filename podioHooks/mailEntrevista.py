# code TODO utf8
from django_podio import api
from django_mailTemplates import mailApi

def run(appID, params, hook=None):
    podioApi = api.PodioApi(appID)
    item = podioApi.getItem(params['item_id'])
    email = mailApi.MailApi('testMail')
    status = email.send_mail('im@aiesecandes.org', ['camilo.forero@aiesec.net', 'camilo.forero3@googlemail.com', 'igcdp.pk@aiesecandes.org'], context=item['values'])
    print status
    return 'success %s' % item['values']['email'] 
        
