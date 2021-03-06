# coding=utf-8
from __future__ import unicode_literals
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    #url(r'^personas/(?P<pk>\d+)/registrar$', views.registrar, name='registrar'),
    #url(r'^feedback/$', views.feedback, name='feedback'),
    url(r'^(?i)(?P<office_name>\w+)/uncontacted/$', cache_page(60*5)(views.GetUncontactedEPs.as_view()), name='uncontactedEPs'),
    url(r'^(?i)(?P<office_name>\w+)/search_tool/$', cache_page(60*60*24)(views.GetMatchableEPs.as_view()), name='search_tool'),
    url(r'^(?i)(?P<office_name>\w+)/application_count/$', cache_page(0*60*24)(views.CountApplications.as_view()), name='application_count'),
    url(r'^(?i)(?P<office_name>\w+)/contacted_ranking/$', cache_page(0*60*24)(views.ContactedRanking.as_view()), name='contacted_ranking'),
    url(r'^(?i)(?P<office_name>\w+)/stats/(?P<interaction>\w+)/(?P<program>[io]g(v|et|t|e))/(?P<year>\d+)/(?P<month>\d+)/$', cache_page(0*60*24)(views.GetEPs.as_view()), name='realized_eps'),
    url(r'^$', cache_page(1*60*1)(views.GetIndex.as_view()), name='index'),
    url(r'^ebs/(?P<mc>\w+)/$', cache_page(60*60*24*7)(views.GetEBs.as_view()), name='ebs'),
    url(r'^uncontacted/$', cache_page(60*5)(views.GetUncontactedEPs.as_view()), name='uncontactedEPs'),
    url(r'^search_tool/$', cache_page(60*60*24)(views.GetMatchableEPs.as_view()), name='search_tool'),
    url(r'^application_count/$', cache_page(0*60*24)(views.CountApplications.as_view()), name='application_count'),
    url(r'^contacted_ranking/$', cache_page(0*60*24)(views.ContactedRanking.as_view()), name='contacted_ranking'),
    url(r'^realized/(?P<program>[io]g(v|ip))/(?P<month>\w+)/$', cache_page(0*60*24)(views.GetRealizedEPs.as_view()), name='realized_eps'),
    ]
