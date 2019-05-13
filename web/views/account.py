#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import render
from utils.util import u_response


# Create your views here.

def login(request):
    """
    登录接口
    :param request:
    :return:
    """

    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        result = u_response()
