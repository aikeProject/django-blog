#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.http import HttpResponse
from django.shortcuts import render
from utils.util import u_response
from ..forms.account_forms import LoginForm


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
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            result['message'] = 'True'
        else:
            result['message'] = 'False'
            result['data'] = json.loads(form.errors.as_json())
            pass
        return HttpResponse(json.dumps(result))
