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
    url(r'^ebs/(?P<mc>\w+)/$', cache_page(60*60*24*7)(views.GetEBs.as_view()), name='ebs'),
    url(r'^uncontacted/$', cache_page(60*5)(views.GetUncontactedEPs.as_view()), name='uncontactedEPs'),
    ]
