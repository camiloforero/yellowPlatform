# coding=utf-8
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_expa.expaApi import ExpaApi
from .models import LC
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
        programs = ['ogcdp', 'igcdp', 'ogip', 'igip']
        achieved = {}
        total = 0
        for program in programs:
            achieved[program] = api.getCurrentYearStats(program)
            total += achieved[program]['RE']
        achieved['total'] = {'RE':total}
        context['achieved'] = achieved 
        rankings = {
            'rankings': {
                'MA':tools.getLCRankings('total', 'MA'),
                'RE':tools.getLCRankings('total', 'RE')
                }
            }
        context.update(rankings)
        return context

class GetAreaScoreboard(TemplateView):
    template_name = "analytics/area_scoreboard.html"
    def get_context_data(self, **kwargs):
        api = ExpaApi()
        programa = self.kwargs['programa']
        context = super(GetAreaScoreboard, self).get_context_data(**kwargs)
        context['performance'] = api.getProgramWeeklyPerformance(programa)
        context['program'] = programa 
        #Creates the JSON data to be used by Google Charts
        chartList = [['Semana', 'Matches', 'Realizaciones']]
        columns = zip(context['performance']['weekly']['MA'], context['performance']['weekly']['RE'])
        for index, week in enumerate(columns):
            chartList.append(['Semana %i' % index, columns[index][0], columns[index][1]])
        context['weeklyJSON'] = json.dumps(chartList)
        
        #Finds the top for LATAM and inside own country
        rankings = {
            'rankings': {
                'MA':tools.getLCRankings(programa, 'MA'),
                'RE':tools.getLCRankings(programa, 'RE')
                }
            }
        context.update(rankings)

        if programa[0] == 'o': #Specific analytics for OGX
            #Context data for total uncontacted EPs
            context['uncontacted'] = api.getUncontactedEPs()['total']
            #Context data for Weekly registered/contacted and contacted/interviewed analytics
            weekRegisteredEPs = api.getWeekRegistered()
            weekRegisteredContacted = 0
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
            weekContactedEPs = api.getWeekContacted()
            weekContactedInterviewed = 0
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
        else:
            print programa[0]



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

class GetRanking(ListView):
    model = LC
    context_object_name = 'lcs'
    template_name = "analytics/ranking.html"
    def get_queryset(self):
        queryFilter = {}
        if self.kwargs['ranking'] == 'global':
            pass
        elif self.kwargs['ranking'] == 'regional':
            queryFilter['mc__region'] = 1627
        elif self.kwargs['ranking'] == 'national':
            queryFilter['mc_id'] = 1551
        else: 
            raise Http404('Ranking inválido')
        return LC.objects.select_related('mc').filter(**queryFilter).order_by('-' + self.kwargs['programa']+self.kwargs['metric'])
    def get_context_data(self, **kwargs):
        context = super(GetRanking, self).get_context_data(**kwargs)
        context['programa'] = self.kwargs['programa']
        context['ranking'] = self.kwargs['ranking']
        return context
