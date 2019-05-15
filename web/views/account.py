#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from io import BytesIO
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from utils.util import u_response
from utils.check_code import create_validate_code
from ..forms.account_forms import LoginForm, RegisterForm
from repository import models


# Create your views here.

def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request=request, template_name='register.html')
    else:
        form = RegisterForm(request=request, data=request.POST)
        result = u_response()
        if form.is_valid():
            models.UserInfo.objects.create(
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['email']
            )
            result['status'] = True
            result['message'] = '注册成功'
        else:
            result['status'] = False
            result['message'] = json.loads(form.errors.as_json())

    return JsonResponse(result)


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
                if form.cleaned_data.get('rmb'):
                    request.session.set_expiry(60 * 60 * 24 * 30)
            else:
                result['message'] = '用户名、密码错误'
        else:
            result['status'] = False
            result['message'] = json.loads(form.errors.as_json())
        return JsonResponse(result)


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
    request.session.clear()
    return redirect('/')
