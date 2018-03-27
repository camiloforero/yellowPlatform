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
    url(r'^$', cache_page(1*60*1)(views.GetIndex.as_view()), name='index'),
    url(r'^(?i)(?P<office_name>\w+)/scoreboard/$', cache_page(1*60*1)(views.GetLCScoreboard.as_view()), name='office_scoreboard'),
    url(r'^(?i)(?P<office_name>\w+)/scoreboard/(?P<programa>[io]g(v|et|e|t))/$', cache_page(60*1)(views.GetAreaScoreboard.as_view()), name='area_scoreboard'),
    url(r'^(?i)(?P<office_name>\w+)/ranking/$', cache_page(60)(views.GetRankingIndex.as_view()), name='ranking_index'),
    url(r'^(?i)(?P<office_name>\w+)/ranking/(?P<programa>([io]g(v|et|e|t))|total)/(?P<ranking>\w+)/(?P<metric>\w+)/$', cache_page(60)(views.GetRanking.as_view()), name='ranking'),
    url(r'^(?i)(?P<area>\w+)/rankings/(?P<programa>([io]g(v|et|e|t))|total)/(?P<depth>\w+)/(?P<metric>\w+)/$', cache_page(60)(views.GetRanking_v2.as_view()), name='ranking_v2'),
    url(r'^(?i)(?P<programa>([io]g(v|et))|total)/ranking/(?P<ranking>\w+)/(?P<metric>\w\w)/$', cache_page(60)(views.GetRanking.as_view()), name='ranking2'),
    url(r'^ebsColombia/$', cache_page(60*60*24*7)(views.GetColombianEBs.as_view()), name='colombian_ebs'),
    url(r'^performance/2015/$', cache_page(60*60*24*30)(views.GetAndesYearlyPerformance.as_view()), name='yearly_performance'),
    url(r'^(?i)(?P<programa>[io]g(v|et|e|t))/$', cache_page(60*1)(views.GetAreaScoreboard.as_view()), name='area_scoreboard2'),
    url(r'^ranking/index/$', cache_page(60)(views.GetRankingIndex.as_view()), name='ranking_index2'),
    url(r'^performance/semanal/$', cache_page(60*60*12)(views.GetLCWeeklyGoals.as_view()), name='weekly_performance'),
    url(r'^(?i)ANDES/scoreboard/IM/$', cache_page(60)(views.GetIMScoreboard.as_view()), name='im_scoreboard'),
    ]
