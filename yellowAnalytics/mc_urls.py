# coding=utf-8
from __future__ import unicode_literals
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

from . import views, mc_views

urlpatterns = [
    url(r'^rewards/$', cache_page(1*5*60)(mc_views.RewardsScoreboard.as_view()), name='rewards_scoreboard'),
    url(r'^teams/', cache_page(1*60*1)(mc_views.GetTeamsScoreboard.as_view()), name='office_scoreboard'),
    url(r'^bangladesh/$', cache_page(60*0)(mc_views.GetBangladeshScoreboard.as_view()), name='bangladesh_main'),
    url(r'^(?i)(?P<area>\w+)/rankings/(?P<programa>([io]g(v|et|e|t))|total)/(?P<depth>\w+)/(?P<metric>\w+)/$', cache_page(60)(views.GetRanking_v2.as_view()), name='ranking_v2'),
    url(r'^(?i)(?P<programa>([io]g(v|et))|total)/ranking/(?P<ranking>\w+)/(?P<metric>\w\w)/$', cache_page(60)(views.GetRanking.as_view()), name='ranking2'),
    ]
