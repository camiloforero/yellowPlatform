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
    url(r'^$', cache_page(1*60*1)(views.GetLCScoreboard.as_view()), name='lc_scoreboard'),
    url(r'^(?P<officeID>\d+)/scoreboard/$', cache_page(1*60*1)(views.GetLCScoreboard.as_view()), name='office_scoreboard'),
    url(r'^ebsColombia/$', cache_page(60*60*24*7)(views.GetColombianEBs.as_view()), name='colombian_ebs'),
    url(r'^performance/2015/$', cache_page(60*60*24*30)(views.GetAndesYearlyPerformance.as_view()), name='yearly_performance'),
    url(r'^(?P<programa>\w+)/$', cache_page(60*1)(views.GetAreaScoreboard.as_view()), name='area_scoreboard'),
    url(r'^ranking/index/$', cache_page(60)(views.GetRankingIndex.as_view()), name='ranking_index2'),
    url(r'^(?P<officeID>\d+)/ranking/$', cache_page(60)(views.GetRankingIndex.as_view()), name='ranking_index'),
    url(r'^(?P<programa>\w+)/ranking/(?P<ranking>\w+)/(?P<metric>\w\w)/$', cache_page(60)(views.GetRanking.as_view()), name='ranking'),
    url(r'^performance/semanal/$', cache_page(60*60*12)(views.GetLCWeeklyGoals.as_view()), name='weekly_performance'),
    ]
