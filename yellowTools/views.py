# coding=utf-8
from __future__ import unicode_literals
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_expa import expaApi, tools
from yellowAnalytics.models import Office

from . import tools

import calendar
import json

class GetEBs(TemplateView):
    template_name = "tools/contactList.html" 
    def get_context_data(self, **kwargs):
        country = self.kwargs['mc'].replace("_", " ")
        mc = Office.objects.get(name__iexact=country)
        #se revisa si la oficina actual ya tiene los datos de contacto de su EB
        context = super(GetEBs, self).get_context_data(**kwargs)
        context['lcs'] = mc.suboffices.all()
        print mc.suboffices
        return context

class GetMatchableEPs(TemplateView):
    """
    This view gets all EPs of AIESEC Andes that are interviewed and in Open or In progress status, along with some of their contact data, so that the current or other LCs know who they are and contact them.
    """
    template_name = "tools/eps.html" 
    def get_context_data(self, **kwargs):
        api = expaApi.ExpaApi()
        context = super(GetMatchableEPs, self).get_context_data(**kwargs)
        try:
            office_name = self.kwargs['office_name']
        except KeyError:
            office_name = 'ANDES'
        office = Office.objects.get(name=office_name.replace('_', ' '))
        officeID = office.expaID
        context['office_name'] = office_name
        eps = api.get_matchable_EPs(officeID)['eps']
        print eps
        print "TEST"
        eps = tools.set_program(eps)
        context['personas'] = eps 
        context['header'] = 'AIESEC %s EP Search Tool' % office_name
        return context

class GetUncontactedEPs(TemplateView):
    template_name = "tools/eps.html" 
    def get_context_data(self, **kwargs):
        api = expaApi.ExpaApi()
        context = super(GetUncontactedEPs, self).get_context_data(**kwargs)
        try:
            office_name = self.kwargs['office_name']
        except KeyError:
            office_name = 'ANDES'
        context['office_name'] = office_name
        office = Office.objects.select_related('superoffice', 'superoffice__superoffice').get(name=office_name.replace('_', ' '))
        officeID = office.expaID
        eps = api.getUncontactedEPs(officeID)['eps']
        eps = tools.set_program(eps)
        context['personas'] = eps 
        context['header'] = 'Uncontacted EPs'
        return context

class GetEPs(TemplateView):
    template_name = "tools/applications.html" 
    def get_context_data(self, **kwargs):
        api = expaApi.ExpaApi()
        context = super(GetEPs, self).get_context_data(**kwargs)
        try:
            office_name = self.kwargs['office_name']
        except KeyError:
            office_name = 'ANDES'
        context['office_name'] = office_name
        office = Office.objects.select_related('superoffice', 'superoffice__superoffice').get(name=office_name.replace('_', ' '))
        officeID = office.expaID
        start_date = '%s-%s-01' % (self.kwargs['year'], self.kwargs['month'])
        end_date =  '%s-%s-%s' % (self.kwargs['year'], self.kwargs['month'], calendar.monthrange(int(self.kwargs['year']), int(self.kwargs['month']))[1])
        context['applications'] = api.get_interactions(self.kwargs['interaction'], officeID, self.kwargs['program'], start_date, end_date)['items']
        context['header'] = '%s EPs' % self.kwargs['interaction']
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

class CountApplications(TemplateView):
    """
    This view counts all applications of all AIESEC Andes EPs during the past week. If an EP does not appear, then he hasn't applied for anything at all
    """
    template_name = "tools/application_count.html" 
    def get_context_data(self, **kwargs):
        api = expaApi.ExpaApi()
        context = super(CountApplications, self).get_context_data(**kwargs)
        try:
            office_name = self.kwargs['office_name']
        except KeyError:
            office_name = 'ANDES'
        context['office_name'] = office_name
        office = Office.objects.select_related('superoffice', 'superoffice__superoffice').get(name=office_name.replace('_', ' '))
        officeID = office.expaID
        applications = api.get_past_interactions('applied', 7, officeID, today=True)
        eps = tools.count_applications(applications)
        context['personas'] = eps 
        context['header'] = 'Aplicaciones a oportunidades en AIESEC %s' % office_name
        return context

class ContactedRanking(TemplateView):
    """
    This view counts all applications of all AIESEC Andes EPs during the past week. If an EP does not appear, then he hasn't applied for anything at all
    """
    template_name = "tools/contacted_ranking.html" 
    def get_context_data(self, **kwargs):
        api = expaApi.ExpaApi()
        context = super(ContactedRanking, self).get_context_data(**kwargs)
        try:
            office_name = self.kwargs['office_name']
        except KeyError:
            office_name = 'ANDES'
        context['office_name'] = office_name
        office = Office.objects.select_related('superoffice', 'superoffice__superoffice').get(name=office_name.replace('_', ' '))
        officeID = office.expaID
        cnt_eps = api.get_past_interactions('contacted', 0, officeID, today=True)
        eps = tools.count_contacted(cnt_eps)
        context['personas'] = eps 
        context['header'] = 'Conteo de contactados por persona en AIESEC Andes'
        return context

