#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from .views import account, home

urlpatterns = [
    url(r'^login$', account.login),
    url(r'^register$', account.register),
    url(r'^logout$', account.logout),
    url(r'^checkCode$', account.check_code),
    url(r'^all/(?P<article_type_id>\d+)?$', home.index, name='index')
]
