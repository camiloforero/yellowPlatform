# coding=utf-8
from __future__ import unicode_literals

from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_expa.expaApi import ExpaApi
from django_podio.api import PodioApi
from .models import LC, MonthlyGoal, MonthlyAchievement, Office, LogrosPrograma, Program
from . import tools

import json

class GetAndesYearlyPerformance(TemplateView):
    template_name = "analytics/monthlyPerformance.html"
    def get_context_data(self, **kwargs):
        api = ExpaApi()
        context = super(GetAndesYearlyPerformance, self).get_context_data(**kwargs)
        context['programs'] = api.getLCYearlyPerformance(2015)
        return context

class GetColombianEBs(TemplateView):
    template_name = "analytics/contactList.html"
    def get_context_data(self, **kwargs):
        api = ExpaApi()
        context = super(GetColombianEBs, self).get_context_data(**kwargs)
        context['lcs'] = api.getColombiaContactList()
        return context


class GetLCScoreboard(TemplateView):
    template_name = "analytics/scoreboard.html"
    def get_context_data(self, **kwargs):
        api = ExpaApi()
        context = super(GetLCScoreboard, self).get_context_data(**kwargs)
        try:
            office_name = self.kwargs['office_name']
        except KeyError:
            office_name = 'ANDES'
        context['office_name'] = office_name
        office = Office.objects.select_related('superoffice', 'superoffice__superoffice').get(name=office_name.replace('_', ' '))
        officeID = office.expaID
        context['officeID'] = officeID
        products = []
        for product in Program.objects.all():
            products.append(product.name)
        context['products'] = products
        #Prepara la información respecto a los logros del LC a partir de la información dentro de la base de datos
        achieved = {}
        total = 0
        for logro in LogrosPrograma.objects.filter(office=officeID):
            program = logro.program_id
            achieved[program] = logro
            total += achieved[program].realized
        achieved['total'] = {'realized':total}
        context['achieved'] = achieved 
        #Carga de la base de datos los logros planeados
        planned = {}
        total_meta = 0
        for meta in MonthlyGoal.objects.filter(office_id=officeID).values('program').annotate(realized=Sum('realized'), approved=Sum('approved')):
            program = meta['program']
            planned[program] = meta
            meta =  planned[program]['realized']
            if meta is None:
                meta = 0
            total_meta += meta
        planned['total'] = {'realized':total_meta}
        context['planned'] = planned
        #Agrega los rankings
        rankings = {
            'rankings': {
                'approved':tools.getLCRankings('Total', 'approved', lc=office),
                'realized':tools.getLCRankings('Total', 'realized', lc=office)
                }
            }
        context.update(rankings)
        return context

class GetAreaScoreboard(TemplateView):
    template_name = "analytics/area_scoreboard.html"
    def get_context_data(self, **kwargs):
        context = super(GetAreaScoreboard, self).get_context_data(**kwargs)
        api = ExpaApi()
        office_name = self.kwargs['office_name']
        context['office_name'] = office_name
        office = Office.objects.select_related('superoffice', 'superoffice__superoffice').get(name=office_name.replace('_', ' '))
        officeID = office.expaID
        program = self.kwargs['programa']
        context['officeID'] = officeID
        context['program'] = program
        #Prepara la información respecto a los logros del LC a partir de la información dentro de la base de datos
        achieved = {}
        for logro in LogrosPrograma.objects.filter(office=officeID, program_id=program):
            achieved = logro
        context['achieved'] = achieved 
        #Carga de la base de datos los logros planeados
        planned = {}
        for meta in MonthlyGoal.objects.filter(office_id=officeID, program_id=program).values('program').annotate(realized=Sum('realized'), approved=Sum('approved')):
            planned = meta
        context['planned'] = planned
        #context['performance'] = api.getProgramWeeklyPerformance(programa)
        #columns = zip(context['performance']['weekly']['MA'], context['performance']['weekly']['RE'])
        #Creates the JSON data to be used by Google Charts
        #chartList = [['Semana', 'Matches', 'Realizaciones']]
        #for index, week in enumerate(columns):
        #    chartList.append(['Semana %i' % index, columns[index][0], columns[index][1]])
        #context['weeklyJSON'] = json.dumps(chartList)
        
        #Finds the top for LATAM and inside own country
        rankings = {
            'rankings': {
                'approved':tools.getLCRankings(program, 'approved', lc=office),
                'realized':tools.getLCRankings(program, 'realized', lc=office),
                }
            }
        context.update(rankings)
        #These analytics are related to the fulfillment of the current monthly goal
        context['planned_monthly'] = MonthlyGoal.objects.filter(office=officeID, program=program.upper()).order_by('year', 'month')
        context['achieved_monthly'] = MonthlyAchievement.objects.filter(office=officeID, program=program.upper()).order_by('month')
        #This data is related to the planned and achieved goals during the current month
        current_month = {}
        current_month_number, current_year_number = map(int, datetime.now().strftime("%m,%Y").split(','))
        try:
            current_month['planned'] = MonthlyGoal.objects.get(office=officeID, program=program.upper(), month=current_month_number)
        except MonthlyGoal.DoesNotExist: 
            current_month['planned'] = "Falta llenar metas en PODIO"
        current_month['achieved'] = api.getMonthStats(current_month_number, current_year_number, program.upper(), officeID)
        context['current_month'] = current_month
        #context['monthly_achievements'] = api.getProgramMonthlyPerformance(programa, 1395)
        #These analytics are related to the achievements durint a past period of time
        context['achieved_past_week'] = api.get_past_stats(7, program, officeID)

        if program[0].lower() == 'o': #Specific analytics for OGX
            #Context data for total uncontacted EPs
            try:
                context['uncontacted'] = api.getUncontactedEPs(officeID)['total']
            except ValueError as e:
                print e #TODO: Logging?
                context['uncontacted'] = "EXPA Error"
            #Context data for Weekly registered/contacted and contacted/interviewed analytics
            try:
                weekRegisteredEPs = api.getWeekRegistered(officeID)
                weekRegisteredContacted = 0.0
                for ep in weekRegisteredEPs['eps']:
                    if ep['contacted_at']:
                        weekRegisteredContacted += 1
                try:
                    contacted_rate = weekRegisteredContacted/weekRegisteredEPs['total']
                except ZeroDivisionError:
                    contacted_rate = 0
                context['weekRegisteredAnalytics'] = {
                    'total':weekRegisteredEPs['total'],
                    'nContacted':weekRegisteredContacted,
                    'rate':contacted_rate*100,
                    'gap':weekRegisteredContacted - weekRegisteredEPs['total']
                }
            except ValueError as e:
                context['weekRegisteredAnalytics'] = {
                    'total':'EXPA Error',
                    'nContacted':'EXPA Error',
                    'rate':'EXPA Error',
                    'gap':'EXPA Error',
                }
 
            try:
                weekContactedEPs = api.getWeekContacted(officeID)
                weekContactedInterviewed = 0.0
                for ep in weekContactedEPs['eps']:
                    if ep['interviewed']:
                        weekContactedInterviewed += 1
                try:
                    interviewed_rate = weekContactedInterviewed/weekContactedEPs['total']
                except ZeroDivisionError:
                    interviewed_rate = 0
                context['weekContactedAnalytics'] = {
                    'total':weekContactedEPs['total'],
                    'nContacted':weekContactedInterviewed,
                    'rate':interviewed_rate*100,
                    'gap':weekContactedInterviewed - weekContactedEPs['total']
                }
            except ValueError as e:#TODO: Mover a la EXPA API
                context['weekContactedAnalytics'] = {
                    'total':'EXPA Error',
                    'nContacted':'EXPA Error',
                    'rate':'EXPA Error',
                    'gap':'EXPA Error',
                }

        else:
            print program[0]
        return context

class GetLCWeeklyGoals(TemplateView):
    template_name = "analytics/weeklyPerformance.html"
    def get_context_data(self, **kwargs):
        api = ExpaApi()
        context = super(GetLCWeeklyGoals, self).get_context_data(**kwargs)
        context['performance'] = api.getLCWeeklyPerformance()
        return context

class GetIndex(TemplateView):
    template_name = "analytics/index.html"
    def get_context_data(self, **kwargs):
        api = ExpaApi()
        context = super(GetIndex, self).get_context_data(**kwargs)
        context['lcs'] = Office.objects.filter(superoffice_id=1551).order_by('name')
        return context

class GetRankingIndex(TemplateView):
    template_name = "analytics/ranking_index.html"
    def get_context_data(self, **kwargs):
        context = super(GetRankingIndex, self).get_context_data(**kwargs)
        office_name = self.kwargs['office_name']
        context['office_name'] = office_name
        office = Office.objects.select_related('superoffice', 'superoffice__superoffice').get(name=office_name.replace('_', ' '))
        officeID = office.expaID
        programs = []
        for program in Program.objects.all():
            programs.append(program.name)
        #Se agregan todos los programas en la base de datos. Esto permite que estos se puedan modificar desde la interfaz
        programs.append('Total') #Se agrega también una representación de los rankings generales
        rankings = { program:{'approved':tools.getLCRankings(program,'approved', office), 'realized':tools.getLCRankings(program, 'realized', office)} for program in programs}
        context['all_rankings'] = rankings
        return context


class GetRanking(ListView):
    context_object_name = 'lcs'
    template_name = "analytics/ranking.html"
    def get_queryset(self):
        office_name = self.kwargs['office_name']
        office = Office.objects.select_related('superoffice', 'superoffice__superoffice').get(name=office_name.replace('_', ' '))
        officeID = office.expaID
        queryFilter = {"office__office_type":office.office_type}  #Crea un diccionario donde se guardarán todos los filtros de la query
        #Agrega filtros que restringen los logros que se sacan de la base de datos a sólo los de la misma región o los del mismo LC. No se hace nada si es global, y se lanza una excepción si se pide otra cosa
        if self.kwargs['ranking'] == 'global':
            pass
        elif self.kwargs['ranking'] == 'regional':
            queryFilter['office__superoffice__superoffice_id'] = office.superoffice.superoffice_id
        elif self.kwargs['ranking'] == 'national':
            queryFilter['office__superoffice_id'] = office.superoffice_id
        else: 
            raise Http404('Ranking inválido')
        #Filtra solo los LogrosPrograma que hacen parte del programa especificado, al menos que busque a Total, caso en el cual no se agrega el filtro, mostrando entonces los logros de los 4 programas
        if self.kwargs['programa'].lower()!='total':
            queryFilter['program__name__iexact'] = self.kwargs['programa']
            return LogrosPrograma.objects.select_related('office__superoffice').filter(**queryFilter).values('office__name', 'office__superoffice__name', 'approved', 'realized').order_by('-' + self.kwargs['metric'])
        else: #Si es total
            return LogrosPrograma.objects.select_related('office__superoffice').filter(**queryFilter).values('office__name', 'office__superoffice__name').annotate(approved=Sum('approved'), realized=Sum('realized')).order_by('-' + self.kwargs['metric'])
    def get_context_data(self, **kwargs):
        context = super(GetRanking, self).get_context_data(**kwargs)
        context['programa'] = self.kwargs['programa']
        context['ranking'] = self.kwargs['ranking']
        return context


class GetRanking_v2(ListView):
    """
    This one is different from the previous one because instead of the target LC, it uses the area we want rankings of (a country, a region, or the world) and the kind of offices we want to appear there (lcs, mcs or regions) in order to create the rankings
    area: which area we want to restrict the ranking. It should be a country, a region, or AI
    depth: whether we want to see LCs, MCs or regions inside the area
    """
    context_object_name = 'lcs'
    template_name = "analytics/ranking.html"
    def get_queryset(self):
        values = {
            'AI': 0,
            'Region': 1,
            'MC': 2,
            'LC': 3,
        }
        area_name = self.kwargs['area']
        area = Office.objects.select_related('superoffice', 'superoffice__superoffice').get(name=area_name.replace('_', ' '))
        area_id = area.expaID
        area_type = area.office_type
        queryFilter = {"office__office_type":area_type}  #Crea un diccionario donde se guardarán todos los filtros de la query
        queryFilter = {"office__office_type":self.kwargs['depth']}  #Crea un diccionario donde se guardarán todos los filtros de la query
        #Agrega filtros que restringen los logros que se sacan de la base de datos a sólo los de la misma región o los del mismo LC. No se hace nada si es global, y se lanza una excepción si se pide otra cosa
        loop_length = values[self.kwargs['depth']] - values[area_type] 
        debug = ''
        debug += ''
        if loop_length <= 0:
            raise Http404('Invalid ranking combination')
        else:
            depth_filter = 'office%s__superoffice_id' # This param means how many suboffices up will the final query go to find the right area.
            addon = '' # represents __superoffice added
            for i in range(loop_length - 1):
                addon += '__superoffice'
            queryFilter[depth_filter % addon] = area_id
        #Filtra solo los LogrosPrograma que hacen parte del programa especificado, al menos que busque a Total, caso en el cual no se agrega el filtro, mostrando entonces los logros de los 4 programas
        if self.kwargs['programa'].lower()!='total': # If not asking for total rankings, will filter by program
            queryFilter['program__name__iexact'] = self.kwargs['programa']
            return LogrosPrograma.objects.select_related('office__superoffice').filter(**queryFilter).values('office__name', 'office__superoffice__name', 'approved', 'realized').order_by('-' + self.kwargs['metric'])
        else: #Si es total
            return LogrosPrograma.objects.select_related('office__superoffice').filter(**queryFilter).values('office__name', 'office__superoffice__name').annotate(approved=Sum('approved'), realized=Sum('realized')).order_by('-' + self.kwargs['metric'])
    def get_context_data(self, **kwargs):
        context = super(GetRanking_v2, self).get_context_data(**kwargs)
        context['programa'] = self.kwargs['programa']
        context['ranking'] = self.kwargs['area']
        context['metric'] = self.kwargs['metric']
        return context


#========== Scoreboards por área ============

class GetIMScoreboard(TemplateView):
    template_name = "analytics/custom_scoreboards/IM.html"
    def get_context_data(self, **kwargs):
        context = super(GetIMScoreboard, self).get_context_data(**kwargs)
        podioApi = PodioApi('15280717')
        #Obtiene todos los ítems de la aplicación de base de datos
        items = podioApi.get_filtered_items(None)
        #Hace un conteo por área de los miembros con correo AIESECo
        total = {
            "total":0,
            "aiesec_mail": 0,
            "career_plan": 0,
            }
        total_area = {}
        for item in items:
            #Primero cuenta el total total, y el total por áreas
            total['total'] += 1
            area = item['values'][124721552]['value']['values'][122424946]['value']
            try:
                total_area[area]['total'] += 1
            except KeyError:
                total_area[area] = {'total': 1}
            #Ahora cuenta quienes tienen correo aiesec.net o aiesecandes.org
            email = item['values'][117701824]['value']
            if "@aiesec.net" in email or "aiesecandes.org" in email:
                total["aiesec_mail"] += 1
                try:
                    total_area[area]['aiesec_mail'] += 1
                except KeyError:
                    total_area[area]['aiesec_mail'] = 1
            #Revisa si llenó el plan carrera
            try:
                test = item['values'][129153378]['value']
                total["career_plan"] += 1
                try:
                    total_area[area]['career_plan'] += 1
                except KeyError:
                    total_area[area]['career_plan'] = 1
            except KeyError:
                pass
        context['total'] = total
        context['total_area'] = total_area
        print total
        print total_area
        return context
