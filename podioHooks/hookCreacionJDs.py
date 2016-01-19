# code TODO utf8
from django_podio import api
from django_documents import documentsApi

from django.core.mail import EmailMessage
from django.utils.html import strip_tags

import pdb

def run(appID, params):
    def dictSwitch(oldDict, transformer):
        newDict = {}
        for key, value in oldDict.iteritems():
            try:
                newDict[transformer[key]] = value
            except KeyError:
                newDict[key] = value
        return newDict
    transformer = {
        'english-writing': 'writing', 
        'english-reading': 'reading',
        'english-listening': 'listening',
        'english-speaking': 'speaking',
        'world-citizen-after': 'wc_a',
        'solution-driven-before': 'sd_b',
        'empowering-others-after': 'eo_a',
        'horas-semanales': 'horas_semanales',
        'title': 'cargo',
        'world-citizen-before': 'wc_b',
        'self-aware-before': 'sa_b',
        'empowering-others-before': 'eo_b',
        'self-aware-after': 'sa_a',
        'lider': 'lider__nombre',
        'main-functions': 'main_functions',
        'software-knowledge': 'software_knowledge',
        'specific-knowledge': 'specific_knowledge',
        'kpis': 'critical_success_factors',
        'job-description': 'job_description',
        'solution-driven-after': 'sd_a',
        }

    podioApi = api.PodioApi(appID)
    item = podioApi.getItem(params['item_id'], no_html=True)
    
    data = dictSwitch(item['values'], transformer)
    data['lider'] = item['values']['lider']['values']['title']
    data['area'] = item['values']['lider']['values']['nombre-del-cargo'].replace('LCVP ', "")
    data['horas_semanales'] = data['horas_semanales'].split('.')[0]
    print data

    generator = documentsApi.ODTTemplate('jdTemplate.odt')
    if item['values']['formato-del-jd'] == 'Word':
        fileExtension = '.odt' 
        jd = generator.renderODT(data)
    
    else:
        fileExtension = '.pdf'
        jd = generator.render(data)
    
    fileName = 'JD - %s' % data['cargo']
    email = EmailMessage()
    email.subject = fileName 
    email.body = 'Lo puedes encontrar como un archivo adjunto'
    email.from_email = 'im@aiesecandes.org'
    email.to = [item['values']['lider']['values']['correo-corporativo-aiesecandesorg'],]
    print email.to
    fileData = jd.read()
    #email.attach(fileName + fileExtension, fileData)
    #email.send()
    podioApi.appendFile(params['item_id'], fileName + fileExtension, fileData)


        
