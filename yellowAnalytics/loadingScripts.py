#coding:utf-8
from __future__ import unicode_literals
from django.db import IntegrityError
from yellowAnalytics.models import LC, MC, Region, MonthlyGoal, Program, Office
from django_expa import expaApi

def loadRegions():
    api = expaApi.ExpaApi()
    regions = api.getRegions()
    for region in regions:
        rgn = Region(nombre=region['name'], expaID=region['id'])
        rgn.save()

def load_regions_v2():
    AI = Office.objects.create(name='AIESEC INTERNATIONAL', expaID=1626, office_type='AI', superoffice_id=None)
    AI.save()
    load_suboffices(1626, 'Region')

def loadMCs(regionID):
    api = expaApi.ExpaApi()
    mcs = api.getMCs(regionID)
    for mc in mcs:
        item = MC(nombre=mc['name'], expaID=mc['id'], region=Region.objects.get(expaID=regionID))
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


def loadRegionLCs(regionID):
    region = Region.objects.get(expaID=regionID)
    for mc in region.mcs.all():
        print "Loading MC %s" % mc.nombre
        loadLCs(mc.expaID)

def load_suboffices(officeID, office_type):
    api = expaApi.ExpaApi()
    suboffices = api.getSuboffices(officeID)
    for so in suboffices:
        print "Loading %s %s" % (office_type, so['id'])
        item = Office.objects.create(name=so['name'], expaID=so['id'], office_type=office_type, superoffice_id=officeID)
        try:
            item.save()
        except IntegrityError as e:
            print e
            item.nombre += '_' + item.mc.nombre
            print item.nombre

def loadEverything():
    for region in Region.objects.all():
        print "Loading %s" % region.nombre
        loadMCs(region.expaID)
        loadRegionLCs(region.expaID)

def loadMCPerformance(mcID):
    mc = MC.objects.get(expaID = mcID)
    print "Cargando datos de %s" % mc.nombre
    programs = ['ogcdp', 'igcdp', 'ogip', 'igip']
    metrics = ['MA', 'RE']
    api = expaApi.ExpaApi()
    allProgramsPerformance = {}
    for program in programs:
        print "cargando %s" % program
        performance = api.getCountryCurrentYearStats(program, mcID)
        allProgramsPerformance[program] = performance
    
    for lc in mc.lcs.all():
        for program in programs:
            programPerformance = allProgramsPerformance[program]
            for metric in metrics:
                try:
                    setattr(lc, program+metric, programPerformance[lc.expaID][metric])
                except KeyError as e:
                    break
        lc.save() 
        

def loadRegionPerformance(region=1627):
    """
    Loads the performance of all LCs inside a region.
    """
    region = Region.objects.get(expaID=region)
    for mc in region.mcs.all():
        loadMCPerformance(mc.expaID)

def loadWorldPerformance():
    """
    Loads the performance of all LCs of the world.
    """
    for region in Region.objects.all():
        loadRegionPerformance(region.expaID)

def loadMonthlyGoals(officeID):
    from django_gdocs import gdocsApi
    
    api = gdocsApi.GdocsApi('/var/www/yellowPlatform/google_private_key.json')
    ss = api.gc.open_by_key('1tWh28LGIN1SrAY4iZ-sCIm3Qss-yEKuNsF7XcIrNFUI')
    for program in Program.objects.all():
        sheet = ss.worksheet(str(program))
        goalList = sheet.get_all_values()
        for i in range(len(goalList[0])):
            if i != 0:
                try:
                    goal = MonthlyGoal.objects.create(month=i, MA=int(goalList[1][i]), RE=int(goalList[2][i]), program=program, office_id = officeID)
                    goal.office_id = officeID
                    goal.save()
                except ValueError as e:
                    print 'Hubo un error en %s, revisa que el gdoc esté bien' % program
                    print e
                    break
