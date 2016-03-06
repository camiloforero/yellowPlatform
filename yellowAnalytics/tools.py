from .models import LC

def getLCRankings(programa, metric='RE', lcID = 1395):
    lc = LC.objects.get(expaID = lcID)
    mcID = lc.mc_id
    regionID = lc.mc.region_id
    allLCs = LC.objects.select_related('mc', 'mc__region').all().order_by('-' + programa +metric)
    topGlobal = -1
    topRegion = -1
    topMC = -1
    reMaxGlobal = 100000
    reMaxRegion = 100000
    reMaxMC = 100000
    indexRegion = 0
    indexMC = 0
    for index, lc in enumerate(allLCs):
        re = getattr(lc, programa+metric)
        if lc.mc.region_id == regionID:
            indexRegion += 1
            if re < reMaxRegion:
                reMaxRegion = re
                topRegion = indexRegion
        if lc.mc_id == mcID:
            indexMC += 1
            if re < reMaxMC:
                reMaxMC = re
                topMC = indexMC
        if re < reMaxGlobal:
            reMaxGlobal = re
            topGlobal = index+1
        if lc.expaID == lcID:
            break
    return {
        'global': topGlobal,
        'regional': topRegion,
        'national': topMC
        }
            

