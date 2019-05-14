#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render
from utils.util import u_response
from utils.check_code import create_validate_code
from ..forms.account_forms import LoginForm
from repository import models


# Create your views here.

def register(request):
    """
    注册
    :param request:
    :return:
    """
    pass


def login(request):
    """
    登录接口
    :param request:
    :return: HttpResponse
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
                .values('nid', 'username', 'nickname', 'email', 'avatar', 'blog__nid', 'blog__site').first()
            if user_info:
                result['status'] = True
                request.session['user_info'] = user_info
            else:
                result['message'] = '用户名、密码错误'
        else:
            result['status'] = False
            result['message'] = json.loads(form.errors.as_json())
        return HttpResponse(json.dumps(result))


def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img, code = create_validate_code()
    print('code', code)
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


def logout(request):
    """
    退出登录
    :return:
    """
    pass
