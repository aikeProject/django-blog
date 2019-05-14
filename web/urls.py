#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from .views import account

urlpatterns = [
    url(r'^login$', account.login),
]
