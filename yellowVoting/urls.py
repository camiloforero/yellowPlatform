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
    url(r'^(?P<Q>\w+)/votar/$', views.votingView, name='votacion'),
    url(r'^(?P<Q>\w+)/resultados/$', views.GetVotingResults.as_view(), name='resultados'),
    url(r'^(?P<Q>\w+)/votantes/$', views.GetVoterVotes.as_view(), name='resultados'),
    ]
