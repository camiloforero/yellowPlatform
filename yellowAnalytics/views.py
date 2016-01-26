# coding=utf-8
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_expa.expaApi import ExpaApi
from .models import LC

class GetAndesYearlyPerformance(TemplateView):
    template_name = "analytics/monthlyPerformance.html"
    def get_context_data(self, **kwargs):
        api = ExpaApi()
        context = super(GetAndesYearlyPerformance, self).get_context_data(**kwargs)
        context['programs'] = api.getLCYearlyPerformance(2015)
        return context

class GetColombianEBs(TemplateView):
    template_name = "django_expa/contactList.html"
    def get_context_data(self, **kwargs):
        api = ExpaApi()
        context = super(GetColombianEBs, self).get_context_data(**kwargs)
        context['lcs'] = api.getColombiaContactList()
        return context

class GetLCScoreboard(TemplateView):
    template_name = "analytics/scoreboard.html"
    def get_context_data(self, **kwargs):
        #api = ExpaApi()
        context = super(GetLCScoreboard, self).get_context_data(**kwargs)
        #context['programs'] = api.getLCWeeklyPerformance()
        return context

class GetLCWeeklyGoals(TemplateView):
    template_name = "analytics/weeklyPerformance.html"
    def get_context_data(self, **kwargs):
        api = ExpaApi()
        context = super(GetLCWeeklyGoals, self).get_context_data(**kwargs)
        context['programs'] = api.getLCWeeklyPerformance()
        return context


class GetIndex(TemplateView):
    template_name = "analytics/index.html"

class GetRankingLATAM(ListView):
    model = LC
    context_object_name = 'lcs'
    template_name = "analytics/ranking.html"
    def get_queryset(self):
        return LC.objects.select_related('mc').filter(mc__region = 1627).order_by('-' + self.kwargs['programa']+'RE')
    def get_context_data(self, **kwargs):
        context = super(GetRankingLATAM, self).get_context_data(**kwargs)
        context['programa'] = self.kwargs['programa']
        return context
