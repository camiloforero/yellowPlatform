from django.db import IntegrityError
from yellowAnalytics.models import LC, MC, Region
from django_expa import expaApi

def loadRegions():
    api = expaApi.ExpaApi()
    regions = api.getRegions()
    for region in regions:
        rgn = Region(nombre=region['name'], expaID=region['id'])
        rgn.save()

def loadMCs(region):
    api = expaApi.ExpaApi()
    mcs = api.getMCs(region)
    for mc in mcs:
        item = MC(nombre=mc['name'], expaID=mc['id'], region=Region.objects.get(expaID=region))
        item.save()

def loadLCs(mc):
    api = expaApi.ExpaApi()
    lcs = api.getSuboffices(mc)
    for lc in lcs:
        item = LC(nombre=lc['name'], expaID=lc['id'], mc=MC.objects.get(expaID=mc))
        try:
            item.save()
        except IntegrityError as e:
            print e
            item.nombre += '_' + item.mc.nombre
            print item.nombre


def loadRegionLCs(region):
    region = Region.objects.get(expaID=region)
    for mc in region.mcs.all():
        loadLCs(mc.expaID)

def loadMCPerformance(mc):
    programs = ['ogcdp', 'igcdp', 'ogip', 'igip']
    metrics = ['MA', 'RE']
    api = expaApi.ExpaApi()
    allProgramsPerformance = {}
    for program in programs:
        performance = api.getCountryCurrentYearStats(program, mc)
        allProgramsPerformance[program] = performance
    
    mc = MC.objects.get(expaID = mc)
    for lc in mc.lcs.all():
        for program in programs:
            programPerformance = allProgramsPerformance[program]
            for metric in metrics:
                try:
                    setattr(lc, program+metric, programPerformance[lc.expaID][metric])
                except KeyError as e:
                    print e
                    print lc.nombre
                    print lc.mc.nombre
                    print program
        lc.save() 
        

def loadRegionPeformance(region):
    region = Region.objects.get(expaID=region)
    for mc in region.mcs.all():
        loadMCPerformance(mc.expaID)


