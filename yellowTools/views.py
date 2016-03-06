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

class GetUncontactedEPs(TemplateView):
    template_name = "tools/eps.html" 
    def get_context_data(self, **kwargs):
        api = expaApi.ExpaApi()
        context = super(GetUncontactedEPs, self).get_context_data(**kwargs)
        eps = api.getUncontactedEPs()['eps']
        context['personas'] = eps 
        return context

class GetIndex(TemplateView):
    template_name = "analytics/index.html"
