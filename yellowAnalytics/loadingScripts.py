#coding:utf-8
from __future__ import unicode_literals
import calendar
from datetime import datetime
from django.db import IntegrityError
from yellowAnalytics.models import LC, MC, Region, MonthlyGoal, Program, Office, LogrosPrograma, MonthlyAchievement
from django_expa import expaApi
from django_podio import api, tools

def loadRegions():
    api = expaApi.ExpaApi()
    regions = api.getRegions()
    for region in regions:
        rgn = Region(nombre=region['name'], expaID=region['id'])
        rgn.save()

def load_regions_v2():
    AI = Office.objects.update_or_create(name='AIESEC INTERNATIONAL', expaID=1626, office_type='AI', superoffice_id=None)
    api = expaApi.ExpaApi()
    load_suboffices(1626, 'Region', api)

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

def load_suboffices(officeID, suboffice_type, api):
    """
    Loads all suboffices of the office with the given officeID, and gives them the appropriate office_type (region, MC or LC)
    """
    suboffices = api.getSuboffices(officeID)
    for so in suboffices:
        print "Loading %s %s(%s)" % (suboffice_type, so['name'], so['id'])
        try:
            values = {
                'name':so['name'],
                'office_type':suboffice_type,
                'superoffice_id':officeID,
            }
            item, created = Office.objects.update_or_create(expaID=so['id'], defaults=values)
        except IntegrityError as e:
            print e
            superoffice = Office.objects.get(expaID=officeID)
            values['name'] = so['name'] + '_' + superoffice.name
            item, created = Office.objects.update_or_create(expaID=so['id'], defaults=values)
            print item.name
        if suboffice_type=="Region":
            sub_suboffice_type = "MC"
        elif suboffice_type=="MC":
            sub_suboffice_type = "LC"
        elif suboffice_type=="LC":
            continue
        else:
            raise Exception("Unknown office type")
        load_suboffices(so['id'], sub_suboffice_type, api)

def refresh_rankings_v2():
    print "Refreshing the EXPA rankings"
    api = expaApi.ExpaApi(fail_attempts=5)
    mcs = Office.objects.filter(office_type="MC").order_by('expaID')
    programs = Program.objects.all()
    for mc in mcs:
        print "Cargando datos del MC %s" % mc.name
        for program in programs:
            print "Cargando %s" % program.name
            #Loads the performance in the given program for the given MC
            try:
                performance = api.getCountryCurrentYearStats(program.name, mc.expaID)
                for officeID, values in performance.iteritems():
                #Recorre todas las oficinas y sus logros para el programa dado
                    #print "Office ID: %s" % officeID
                    #print values
                    #Si los logros de este programa ya existen, se actualizan en la base de datos. Si no existen (sucede cuando algún comité del mundo acaba de abrir un nuevo programa) se crean unos nuevos
                    try:
                        logros, created = LogrosPrograma.objects.update_or_create(program=program, office_id=officeID, defaults=values)
                    except IntegrityError as e:
                    #Esto quiere decir que probablemente intentó cargar un LC que todavía no existe. Esto pasa cuando se crean nuevos LCs desde la última vez que se actualizó en ranking.
                        print e
                        load_suboffices(mc.expaID, "LC", api)
                        logros, created = LogrosPrograma.objects.update_or_create(program=program, office_id=officeID, defaults=values)
            except expaApi.APIUnavailableException as e:
                print "Error cargando el país actual, continuando..."
                break

def load_monthly_stats():
    print "Refreshing the monthly goals"
    api = expaApi.ExpaApi()
    mcs = Office.objects.filter(office_type="MC", expaID=1551)
    programs = Program.objects.all()
    current_year, end_month = datetime.today().strftime('%Y-%m').split('-')
    for mes in range(1, int(end_month)):
        for mc in mcs:
            print "Cargando datos del MC %s" % mc.name
            for program in programs:
                start_date = '%s-%s-01' % (current_year, mes)
                end_date = '%s-%s-%s' % (current_year, mes, calendar.monthrange(int(current_year), mes)[1])
                print "Cargando %s, entre %s y %s" % (program.name, start_date, end_date)
                #Loads the performance in the given program for the given MC
                performance = api.getCountryStats(program.name, mc.expaID, start_date, end_date)
                for officeID, values in performance.iteritems():
                #Recorre todas las oficinas y sus logros para el programa dado
                    #print "Office ID: %s" % officeID
                    #print values
                    #Si los logros de este programa ya existen, se actualizan en la base de datos. Si no existen (sucede cuando algún comité del mundo acaba de abrir un nuevo programa) se crean unos nuevos
                    try:
                        logros, created = MonthlyAchievement.objects.update_or_create(program=program, office_id=officeID, month=mes, defaults=values)
                    except IntegrityError as e:
                    #Esto quiere decir que probablemente intentó cargar un LC que todavía no existe. Esto pasa cuando se crean nuevos LCs desde la última vez que se actualizó en ranking.
                        print e
                        load_suboffices(mc.expaID, "LC", api)
                        logros, created = MonthlyAchievement.objects.update_or_create(program=program, office_id=officeID, month=mes, defaults=values)
#########PODIO Loaders###########
#Los scripts que cargan datos de o a PODIO relacionados con las metas
def load_colombia_lcs():
    podioApi = api.PodioApi(16759329)
    lcs = Office.objects.filter(superoffice_id=1551)
    for lc in lcs:
        podioApi.create_item({'fields':{130504166: lc.name, 130513591: unicode(lc.expaID)}})


def load_lc_goals():
    """
    Este método carga todas las metas mensuales presentes en el espacio de PODIO asociado a esta funcionalidad
    """
    #Un diccionario que asocia los field_ids de la aplicación con un mes
    month_dict = {
        130505516:(1, 2016),
        130505517:(2, 2016),
        130505518:(3, 2016),
        130505519:(4, 2016),
        130505520:(5, 2016),
        130505521:(6, 2016),
        130505522:(7, 2016),
        130505523:(8, 2016),
        130505524:(9, 2016),
        130505525:(10, 2016),
        130505526:(11, 2016),
        130505527:(12, 2016),
        130652156:(1, 2017),
    }
    podioApi = api.PodioApi(16759334)
    items = podioApi.get_filtered_items({})
    for item in items:
        #Se crea un diccionario que luego entra como parámetro a la creación de las metas.
        create_dict = {
            'program_id':item['values'][130504336]['value'], #Para obtener el valor del programa del item de PODIO
            'office_id':item['values'][130504335]['value']['values'][130513591]['value'], #Para obtener el ID del LC del related item "LC"
        }
        month_goals = tools.dictSwitch(item['values'], month_dict, ignore_unknown=True)
        #Recorre todos los meses en el diccionario y crea un objeto de tipo MonthlyGoal para cada uno de ellos
        for date, goals in month_goals.iteritems():
            create_dict['month'] = date[0]
            create_dict['year'] = date[1]
            create_dict['defaults']= {
                item['values'][130507913]['value'].lower():goals['value'].split('.')[0]#Obtiene la meta, eliminando decimales, y la asigna al approved o al realized según sea el caso
            }
            print create_dict
            MonthlyGoal.objects.update_or_create(**create_dict)

def load_lc_achievements():
    """
    This method loads a country's LCs achievements in all four programs
    """
    pass

######OBSOLETE
######CONTINUE AT YOUR OWN PERIL
######ABANDON HOPE ALL YE WHO ENTER HERE

def loadEverything():
    for region in Region.objects.all():
        print "Loading %s" % region.nombre
        loadMCs(region.expaID)
        loadRegionLCs(region.expaID)

def loadMCPerformance(mcID, api):
    mc = MC.objects.get(expaID = mcID)
    print "Cargando datos de %s" % mc.nombre
    programs = ['ogcdp', 'igcdp', 'ogip', 'igip']
    metrics = ['MA', 'RE']
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
        

def loadRegionPerformance(region, api):
    """
    Loads the performance of all LCs inside a region.
    """
    region = Region.objects.get(expaID=region)
    for mc in region.mcs.all():
        loadMCPerformance(mc.expaID, api)

def loadWorldPerformance():
    """
    Loads the performance of all LCs of the world.
    """
    api = expaApi.ExpaApi()
    for region in Region.objects.all():
        loadRegionPerformance(region.expaID, api)

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
