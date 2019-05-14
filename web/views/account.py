#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.http import HttpResponse
from django.shortcuts import render
from utils.util import u_response
from ..forms.account_forms import LoginForm
from repository import models


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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_info = models.UserInfo.objects \
                .filter(username=username, password=password) \
                .values('nid', 'username').first()
            if user_info:
                result['status'] = True
                request.session['user_info'] = user_info
            else:
                result['message'] = '用户名、密码错误'
        else:
            result['status'] = False
            result['message'] = json.loads(form.errors.as_json())
        return HttpResponse(json.dumps(result))
