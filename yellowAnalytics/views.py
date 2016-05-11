# coding=utf-8
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_expa.expaApi import ExpaApi
from .models import LC, MonthlyGoal
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
            officeID = self.kwargs['officeID']
        except KeyError:
            officeID = 1395
        programs = ['ogcdp', 'igcdp', 'ogip', 'igip']
        achieved = {}
        total = 0
        for program in programs:
            try:
                achieved[program] = api.getCurrentYearStats(program, officeID=officeID)
                total += achieved[program]['RE']
            except ValueError:
                achieved[program] = {'RE':"Expa Error", 'MA':'Expa Error'}
        achieved['total'] = {'RE':total}
        context['achieved'] = achieved 
        rankings = {
            'rankings': {
                'MA':tools.getLCRankings('total', 'MA', lcID=officeID),
                'RE':tools.getLCRankings('total', 'RE', lcID=officeID)
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
        context['program'] = programa 
        context['performance'] = api.getProgramWeeklyPerformance(programa)
        columns = zip(context['performance']['weekly']['MA'], context['performance']['weekly']['RE'])
        #Creates the JSON data to be used by Google Charts
        chartList = [['Semana', 'Matches', 'Realizaciones']]
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
        #These analytics are related to the fulfillment of the current monthly goal
        context['monthly_goals'] = MonthlyGoal.objects.filter(office=1395, program=programa.upper())
        context['monthly_achievements'] = api.getProgramMonthlyPerformance(programa, 1395)

        if programa[0] == 'o': #Specific analytics for OGX
            #Context data for total uncontacted EPs
            context['uncontacted'] = api.getUncontactedEPs(1395)['total']
            #Context data for Weekly registered/contacted and contacted/interviewed analytics
            weekRegisteredEPs = api.getWeekRegistered(1395)
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
            weekContactedEPs = api.getWeekContacted(1395)
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

class GetRankingIndex(TemplateView):
    template_name = "analytics/ranking_index.html"
    def get_context_data(self, **kwargs):
        try:
            officeID = int(self.kwargs['officeID'])
        except KeyError:
            officeID = 1395
        api = ExpaApi()
        context = super(GetRankingIndex, self).get_context_data(**kwargs)
        programs = ['total', 'igcdp', 'ogcdp', 'igip', 'ogip']
        rankings = { program:{'MA':tools.getLCRankings(program,'MA', officeID), 'RE':tools.getLCRankings(program, 'RE', officeID)} for program in programs}
        context['all_rankings'] = rankings
        return context


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
