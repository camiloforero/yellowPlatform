# coding=utf-8
from __future__ import unicode_literals

from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_expa.expaApi import ExpaApi, APIUnavailableException
from django_podio.api import PodioApi
from .models import LC, MonthlyGoal, MonthlyAchievement, Office, LogrosPrograma, Program
from yellowCrons.models import Member
from . import tools

import json

class RewardsScoreboard(TemplateView):
    template_name = "mc_analytics/rewards_scoreboard.html"
    def get_context_data(self, **kwargs):
        context = super(RewardsScoreboard, self).get_context_data(**kwargs)
        #ex_api = ExpaApi('camilo.forero@aiesec.net')
        p_api = PodioApi(19156174)
        teams = []
        team_leaders = Member.objects.filter(is_active=True).order_by('-extra_points')
        performance = {}
        for team_leader in team_leaders:
            performance[team_leader.podio_id] = {
                'contacted': 0,
                'applied': 0,
                'approved': 0,
            }
            
        gbm_date = '2018-04-06'
        recent_items = p_api.get_filtered_items({
            'last_edit_on':{'from':gbm_date}
        })
        for item in recent_items:
            if 151795765 not in item['values']:
                continue
            tl_id = item['values'][151795765]['value']['user_id']
            if tl_id in performance:
                if 151950042 in item['values']:
                    registration_date =  item['values'][151950042]['value']['start_date']
                status = item['values'][151795769]['value']
                status_number = status.split(' - ')[0]
                if status_number != 0: #if uncontacted, ignores everything
                    if registration_date >= gbm_date:
                        performance[tl_id]['contacted'] += 1
                    elif 159724899 in item['values']:
                        contacted_date = item['values'][159724899]['value']['start_date']
                        if contacted_date >= gbm_date:
                            performance[tl_id]['contacted'] += 1
                    if 158519539 in item['values']:
                        application_date = item['values'][158519539]['value']['start_date']
                        if application_date >= gbm_date:
                            performance[tl_id]['applied'] += 1
                    if 159728809 in item['values']:
                        approval_date = item['values'][159728809]['value']['start_date']
                        if approval_date >= gbm_date:
                            performance[tl_id]['approved'] += 1
                
            
        for tl in team_leaders:
            approved = performance[tl.podio_id]['approved']
            applied = performance[tl.podio_id]['applied']
            contacted = performance[tl.podio_id]['contacted']
            data = {
                'name': tl.team_name,
                'picture': tl.team_picture,
                'approvals': approved,
                'approvals_pts': approved * 35,
                'applicants': applied,
                'applicants_pts': applied * 5,
                'contacted': contacted,
                'contacted_pts': contacted,
                'total': approved*35 + applied*5 + contacted,
            }
            teams.append(data)
        context['teams'] = teams
        return context

class GetBangladeshScoreboard(TemplateView):
    template_name = "mc_analytics/area_scoreboard.html"
    def get_context_data(self, **kwargs):
        context = super(GetBangladeshScoreboard, self).get_context_data(**kwargs)
        api = ExpaApi('camilo.forero@aiesec.net')
        office_id = 2010
        context['office_id'] = office_id
        office = Office.objects.select_related('superoffice').get(expaID=office_id)
        office_name = office.name
        program = 'ogv'
        context['office_name'] = office_name
        context['program'] = program
        #Prepara la información respecto a los logros del LC a partir de la información dentro de la base de datos
        achieved = {}
        
        #TODO: En esta parte voy a crear el diccionario para el scoreboard del MC de una manera super folclórica, pero con el objetivo de mejorar más tade obviamente
        year_metrics = [] #Here I will save all metrics in a format understandable by the scoreboard
        measurements = ['applicants', 'accepted', 'realized', 'completed']
        logros = api.getCurrentMCYearStats('ogv', office_id)
        planned = {
            'applicants': 785, 
            'accepted': 314,
            'approved': 157,
            'realized': 125,
            'completed': 100,

        }
        for measurement in measurements:
            measurement_data = {
                'planned': planned[measurement],
                'executed': logros[measurement],
                'gap': planned[measurement] - logros[measurement],
                'name': measurement,
            }
            year_metrics.append(measurement_data)
        context['year_metrics'] = year_metrics
        wig_measure = 'approved'
        wig = {
            'planned': planned[wig_measure],
            'executed': logros[wig_measure],
            'gap': planned[wig_measure] - logros[wig_measure],
            'name': wig_measure,
        }
        context['wig'] = wig
        context['finance'] = {
            'planned':500000,
            'executed':300000,
        }


        quarter_achievements = api.get_stats(office_id, program, '2018-04-01', datetime.now().strftime('%Y-%m-%d'))
        context['quarter_execution'] = quarter_achievements
        context['month_execution'] = quarter_achievements
        #context['achieved_last_week'] = api.get_past_stats(7, program, office_id)
        context['countdown'] = (datetime.strptime('2018-08-01', '%Y-%m-%d') - datetime.now()).days
        
        #TM scoreboard: See how many members are on each stage of performance
        vd_api = PodioApi(19600457)
        individual_performance = {}
        approvals = vd_api.get_filtered_items({
            157141796:{'from':'2018-04-01'}
        })
        for customer in approvals:
            ep_manager = customer['values'][157144216]['value']['name']            
            if ep_manager in individual_performance:
                individual_performance[ep_manager] += 1
            else:
                individual_performance[ep_manager] = 1

        aggregation = {
            '1':0,
            '2':0,
            '3':0,
            '4':0,
        }
        for manager, approvals in individual_performance.items():
            if approvals == 1:
                aggregation['1'] += 1
            elif approvals == 2:
                aggregation['2'] += 2
            elif approvals == 3:
                aggregation['3'] += 3
            elif approvals >= 4:
                aggregation['4'] += 4

        context['tm_performance'] = aggregation



        return context


class GetTeamsScoreboard(TemplateView):
    template_name = "mc_analytics/team_scoreboard.html"
    def get_context_data(self, **kwargs):
        context = super(GetTeamsScoreboard, self).get_context_data(**kwargs)
        api = ExpaApi('camilo.forero@aiesec.net')
        office_id = 2010
        context['office_id'] = office_id
        office = Office.objects.select_related('superoffice').get(expaID=office_id)
        office_name = office.name
        program = 'ogv'
        context['office_name'] = office_name
        context['program'] = program
        #Prepara la información respecto a los logros del LC a partir de la información dentro de la base de datos
        achieved = {}
        
        #TODO: En esta parte voy a crear el diccionario para el scoreboard del MC de una manera super folclórica, pero con el objetivo de mejorar más tade obviamente
        year_metrics = [] #Here I will save all metrics in a format understandable by the scoreboard
        year_metrics_dict={}
        measurements = ['applicants', 'accepted', 'realized', 'completed']
        logros = api.get_stats(office_id, 'ogv', '2018-04-01')
        planned = {
            'applicants': 500, 
            'accepted': 200,
            'approved': 100,
            'realized': 90,
            'completed': 82,

        }
        team_planned = {
            'applicants': 125, 
            'accepted': 50,
            'approved': 25,
            'realized': 23,
            'completed': 21,

        }
        for measurement in measurements:
            measurement_data = {
                'planned': planned[measurement],
                'executed': logros[measurement],
                'gap': planned[measurement] - logros[measurement],
                'name': measurement,
            }
            year_metrics.append(measurement_data)
            year_metrics_dict[measurement] = measurement_data
        context['year_metrics'] = year_metrics
        wig_measure = 'approved'
        wig = {
            'planned': planned[wig_measure],
            'executed': logros[wig_measure],
            'gap': planned[wig_measure] - logros[wig_measure],
            'name': wig_measure,
        }
        context['wig'] = wig
        all_metrics = {'all': year_metrics_dict}
        all_metrics['all'][wig_measure] = wig


        quarter_achievements = api.get_stats(office_id, program, '2018-04-01', datetime.now().strftime('%Y-%m-%d'))
        context['quarter_execution'] = quarter_achievements
        context['month_execution'] = quarter_achievements
        #context['achieved_last_week'] = api.get_past_stats(7, program, office_id)
        context['countdown'] = (datetime.strptime('2018-08-01', '%Y-%m-%d') - datetime.now()).days

        cons_api = PodioApi(19156174)
        vd_api = PodioApi(19156174)
        team_leaders = Member.objects.filter(is_active=True).order_by('-extra_points')
        context['teams'] = team_leaders
        performance = {}
        for team_leader in team_leaders:
            performance[team_leader.podio_id] = {
                'applicants': 0,
                'accepted': 0,
                'approved': 0,
                'realized': 0,
                'completed': 0,
            }
            
        recent_items = cons_api.get_items_by_view(37897730)
        start_date = '2018-04-01'
        for item in recent_items:
            if 151795765 not in item['values']:
                continue
            tl_id = item['values'][151795765]['value']['user_id']
            if tl_id in performance:
                if 151950042 in item['values']:
                    registration_date =  item['values'][151950042]['value']['start_date']
                status = item['values'][151795769]['value']
                status_number = status.split(' - ')[0]
                if status_number != 0: #if uncontacted, ignores everything
                    if 159724899 in item['values']:
                        contacted_date = item['values'][159724899]['value']['start_date']
                        if contacted_date >= start_date:
                            pass
                    #        performance[tl_id]['contacted'] += 1
                    if 158519539 in item['values']:
                        application_date = item['values'][158519539]['value']['start_date']
                        if application_date >= start_date:
                            performance[tl_id]['applicants'] += 1
                    if 169759824 in item['values']:
                        acceptance_date = item['values'][169759824]['value']['start_date']
                        if acceptance_date >= start_date:
                            performance[tl_id]['accepted'] += 1
                    if 159728809 in item['values']:
                        approval_date = item['values'][159728809]['value']['start_date']
                        if approval_date >= start_date:
                            performance[tl_id]['approved'] += 1
        team_performance = {}
        measurements.append(wig_measure)
        for tl in team_leaders:
            data = {}
            for measurement in measurements:
                measurement_data = {
                    'planned': team_planned[measurement],
                    'executed': performance[tl.podio_id][measurement],
                    'gap': team_planned[measurement] - performance[tl.podio_id][measurement]
                }
                data[measurement] = measurement_data
            team_performance[tl.podio_id] = data

        all_metrics.update(team_performance)
        context['metrics_json'] = json.dumps(all_metrics)
            
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
