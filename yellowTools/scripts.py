#encoding:utf-8
from __future__ import unicode_literals
from django_expa import expaApi
from django_podio import api as podioApi
from yellowAnalytics.models import Office, Member

def load_country_EBs(expaID):
    api = expaApi.ExpaApi()
    eb_data = api.getCountryEBs(expaID)
    mc_object = Office.objects.get(expaID)
    print "Cargando MC %s " % mc_object.name
    for lc in eb_data:
        lc_object = Office.objects.get(expaID=lc['expaID'])
        print "Cargando EBs de %s " % lc_object.name
        for cargo in lc['cargos']:
            try:
                member = Member(office_id=lc['expaID'], expaID=cargo['expaID'] , name=cargo['name'], role=cargo['cargo'], phone=cargo['contactData'].get('phone'),email=cargo['contactData'].get('email'), alt_email=cargo['contactData'].get('altMail'), facebook=cargo['contactData'].get('facebook'))
                member.save()
            except Exception as e:
                print cargo
                print e


def count_ge_gt(days, office_id):
    api = expaApi.ExpaApi('sebastian.ramirezc@aiesec.net')
    ans = {}
    for application in applications: 
        lc_name = application['person']['home_lc']['name']
        try:
            lc = ans[lc_name]
        except KeyError as e:
            ans[lc_name] = {'GT': 0, 'GE': 0}
            lc = ans[lc_name]
        

def copiar_email_plenos():
    """
    Este script coge el correo electrónico, basado en la estructura, de los miembros en pleno derecho del comité y lo usa para actualizar el campo de correo de la base de datos
    """
    api = podioApi.PodioApi(16186489, client=True)
    plenos = api.get_filtered_items(
        [{
            'key':126714277,
            'values':[1]
        }]
    )
    for pleno in plenos:
        api.updateItem(pleno['item'], {125498432:pleno['values'][125498431]['value']['values'][117701824]['value']})
    return plenos



    

