# coding=utf-8
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_expa import expaApi, tools
from yellowAnalytics.models import MC

import json

class GetEBs(TemplateView):
    template_name = "tools/contactList.html" 
    def get_context_data(self, **kwargs):
        country = self.kwargs['mc']
        mcID = MC.objects.get(nombre__iexact=country).expaID
        api = expaApi.ExpaApi()
        context = super(GetEBs, self).get_context_data(**kwargs)
        context['lcs'] = api.getCountryEBs(mcID)
        return context

class GetMatchableEPs(TemplateView):
    """
    This view gets all EPs of AIESEC Andes that are interviewed and in Open or In progress status, along with some of their contact data, so that the current or other LCs know who they are and contact them.
    """
    template_name = "tools/eps.html" 
    def get_context_data(self, **kwargs):
        api = expaApi.ExpaApi()
        context = super(GetMatchableEPs, self).get_context_data(**kwargs)
        eps = api.get_matchable_EPs(1395)['eps']
        context['personas'] = eps 
        context['header'] = 'AIESEC Andes EP Search Tool'
        return context

class GetUncontactedEPs(TemplateView):
    template_name = "tools/eps.html" 
    def get_context_data(self, **kwargs):
        api = expaApi.ExpaApi()
        context = super(GetUncontactedEPs, self).get_context_data(**kwargs)
        eps = api.getUncontactedEPs(1395)['eps']
        context['personas'] = eps 
        context['header'] = 'Uncontacted EPs'
        return context

class GetRealizedEPs(TemplateView):
    template_name = "tools/applications.html" 
    def get_context_data(self, **kwargs):
        context = super(GetRealizedEPs, self).get_context_data(**kwargs)
        path = '/var/www/yellowPlatform/%s_%s.json' % (self.kwargs['month'], self.kwargs['program'])
        with open(path) as data_file:
            data = json.load(data_file)
        context['applications'] = data['data'] 
        context['header'] = 'Realized EPs'
        return context

class GetIndex(TemplateView):
    template_name = "analytics/index.html"
