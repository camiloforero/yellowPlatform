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
    url(r'^$', views.GetIndex.as_view(), name='index'),
    url(r'^ebsColombia/$', cache_page(60*60*24*7)(views.GetColombianEBs.as_view()), name='colombian_ebs'),
    url(r'^performance/2015/$', cache_page(60*60*24*30)(views.GetAndesYearlyPerformance.as_view()), name='yearly_performance'),
    url(r'^ranking/LATAM/(?P<programa>\w+)/$', cache_page(10)(views.GetRankingLATAM.as_view()), name='ranking_latam'),
    url(r'^scoreboard$', cache_page(0*60*12)(views.GetLCScoreboard.as_view()), name='scoreboard'),
    url(r'^performance/semanal/$', cache_page(60*60*12)(views.GetLCWeeklyGoals.as_view()), name='weekly_performance'),
    ]
