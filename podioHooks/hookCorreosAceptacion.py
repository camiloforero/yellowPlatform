# coding=utf-8
from __future__ import unicode_literals
from django_podio import api, tools
from django_mailTemplates import mailApi
from django.core.mail import EmailMessage
from django.utils.html import strip_tags

import pdb

def run(appID, params, hook=None):
    """
    Runs a hook.

    Parameters:
        appID: The ID of the application that called the hook

        params: The parameters coming from the POST data inside the hook
    """
    template = {
        'Ingles': 'englishAcceptedMail',
        'Español': 'spanishAcceptedMail',
        }
    transformer = {
        'title': 'name', 
        }

    podioApi = api.PodioApi(appID)
    item = podioApi.getItem(params['item_id'], no_html=True)
    if item['values']['paso-entrevista'] == 'Si':
        data = tools.dictSwitch(item['values'], transformer)
        data['project_name'] = item['values']['project-you-are-applying']['values']['title']
        data['tn_id'] = item['values']['project-you-are-applying']['values']['tn-id-2']

        email = mailApi.MailApi(template[item['values']['project-you-are-applying']['values']['idioma-proyecto']]) 
        status = email.send_mail('igcdp.pk@aiesecandes.org', [item['values']['email'], ], data) 
        podioApi.comment('item', params['item_id'],
                     {'value': 'El correo ha sido enviado satisfactoriamente a ' + item['values']['email'] + ' con código ' + str(status)})
