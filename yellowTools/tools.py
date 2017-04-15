#encoding:utf-8
from __future__ import unicode_literals
"""
This module contains useful tools that facilitate some repetitive tasks or have logic that varies with time. 
TODO: Move the hardcoded danitza.marentes/oscar.serrato and leouardo.turriago emails to a settings file
"""

def set_program(eps):
    for ep in eps:
        managers = ep['managers']
        for manager in managers:
            if manager['email'] == 'danitza.marentes@aiesec.net' or manager['email'] == 'oscar.serrato@aiesec.net':
                ep['calculated_program'] = 'GCDP'
                break
            elif manager['email'] == 'leonardo.turriago@aiesec.net':
                ep['calculated_program'] = 'GIP'
                break
    return eps
                
def count_applications(applications):
    """
    This module receives a raw applications json from the expaApi module, and extracts all unique applicants, and counts their GV and GIP applications to show them in an interface
    """
    eps = {}
    for application in applications['items']:
        person = application['person']
        try:
            ep = eps[person['id']]
        except KeyError: #Si no existe un EP con esa llave dentro del diccionario es que es nuevo
            ep = {
                'full_name':person['full_name'],
                'gv_apps':0,
                'gt_apps':0,
                'ge_apps':0,
                }
        if application['opportunity']['programmes'][0]['id']==1:
            ep['gv_apps'] += 1
        elif application['opportunity']['programmes'][0]['id']==2:
            ep['gt_apps'] += 1 
        elif application['opportunity']['programmes'][0]['id']==5:
            ep['ge_apps'] += 1 
        eps[person['id']] = ep
    return eps

def count_contacted(eps):
    print eps
    members = {}
    for ep in eps['items']:
        contacter = ep['contacted_by']
        print contacter
        try:
            member = members[contacter['id']]
        except KeyError: #Si no existe un EP con esa llave dentro del diccionario es que es nuevo
            member = {
                'full_name':contacter['full_name'],
                'contacted_number':0,
                }
        member['contacted_number'] += 1
        members[contacter['id']] = member
    return members
