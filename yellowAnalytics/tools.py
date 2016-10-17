from .models import Office, LogrosPrograma
from django.db.models import Sum

def getLCRankings(programa, metric, lc):
    lcID = lc.expaID
    mcID = lc.superoffice_id
    regionID = lc.superoffice.superoffice_id
    if programa.lower() == 'total':
        logros = LogrosPrograma.objects.values('office_id', 'office__superoffice_id', 'office__superoffice__superoffice_id').filter(office__office_type="LC").annotate(approved=Sum('approved'), realized=Sum('realized')).order_by('-' + metric)
    else:
        logros = LogrosPrograma.objects.values('approved', 'realized', 'office_id', 'office__superoffice_id', 'office__superoffice__superoffice_id').filter(program__name__iexact=programa, office__office_type="LC").order_by('-' + metric)
    #allLCs = Office.objects.select_related('superoffice', 'superoffice__superoffice').all().order_by('-' + programa +metric)
    topGlobal = -1
    topRegion = -1
    topMC = -1
    reMaxGlobal = 100000
    reMaxRegion = 100000
    reMaxMC = 100000
    indexRegion = 0
    indexMC = 0
    for index, lc in enumerate(logros):
        try:
            re = lc[metric]
            lc_office = lc['office_id']
        except AttributeError as e:
            print e
            print lc
            re = lc[metric]
            lc_office = Office.objects.get(expaID=lc['office_id'])
            print re
        if lc['office__superoffice__superoffice_id'] == regionID:
            indexRegion += 1
            if re < reMaxRegion:
                reMaxRegion = re
                topRegion = indexRegion
        if lc['office__superoffice_id'] == mcID:
            indexMC += 1
            if re < reMaxMC:
                reMaxMC = re
                topMC = indexMC
        if re < reMaxGlobal:
            reMaxGlobal = re
            topGlobal = index+1
        if lc['office_id'] == lcID:
            break
    return [
        ('global', topGlobal),
        ('regional', topRegion),
        ('national', topMC),
        ]
            

