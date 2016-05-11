# encoding=utf-8
from __future__ import unicode_literals
from django_podio import api, tools
from django_documents import documentsApi
from django_mailTemplates import mailApi

from datetime import datetime


import pdb

def run(appID, params, hook=None):
    podioApi = api.PodioApi(appID)
    item = podioApi.getItem(params['item_id'], no_html=True)

    if item['values']['enviar-certificado'] == 'Si':
        data = tools.hyphen_to_underscore(item['values'])
        data['project_start_date'] = data['project_start_date']['start_date']
        data['project_end_date'] = data['project_end_date']['start_date']
        data['work_hours'] = data['work_hours'].split('.')[0]
        data['today'] = datetime.today().strftime('%Y-%m-%d')
        generator = documentsApi.ODTTemplate('certVoluntariado.odt')
        fileExtension = '.pdf'
        jd = generator.render(data)
        
        fileName = 'Certificado Voluntariado - %s' % data['title']
        email = mailApi.MailApi('mailCertificado')
        status = email.send_mail('igcdp@aiesecandes.org', 
            [item['values']['email'], ], data, 
            attachments=[{'filename': fileName + fileExtension, 'data': jd.read()}, ]
            )
        jd.seek(0)
        print 'return code AppendFile'
        podioApi.appendFile(params['item_id'], fileName + fileExtension, jd)
        print 'fin return code AppendFile'


        
