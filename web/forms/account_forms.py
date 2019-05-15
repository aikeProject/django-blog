#!/usr/bin/env python
# -*- coding:utf-8 -*-


from django.core.exceptions import ValidationError
from django import forms
from django.forms import fields
from .base import BaseForm


class LoginForm(BaseForm, forms.Form):
    username = fields.CharField(
        min_length=6,
        max_length=20,
        error_messages={
            'required': '用户名不能为空',
            'min_length': '用户名长度不小于6字符',
            'max_length': '用户名长度不大于32字符'
        }
    )

    password = fields.RegexField(
        regex='^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        min_length=12,
        max_length=32,
        error_messages={
            'required': '密码不能为空',
            'invalid': '密码必须包含数字，字母、特殊字符',
            'min_length': '用户名长度不小于12字符',
            'max_length': '用户名长度不大于32字符'
        }
    )

    # 过期时间
    rmb = fields.IntegerField(required=False)

    check_code = fields.CharField(
        max_length=4,
        error_messages={'required': '验证码错误', 'max_length': '验证码错误'}
    )

    def clean_check_code(self):
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误', code='invalid')


class RegisterForm(BaseForm, forms.Form):
    username = fields.CharField(
        min_length=6,
        max_length=20,
        error_messages={
            'required': '用户名不能为空',
            'min_length': '用户名长度不小于6字符',
            'max_length': '用户名长度不大于32字符'
        }
    )

    password = fields.RegexField(
        regex='^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        min_length=12,
        max_length=32,
        error_messages={
            'required': '密码不能为空',
            'invalid': '密码必须包含数字，字母、特殊字符',
            'min_length': '用户名长度不小于12字符',
            'max_length': '用户名长度不大于32字符'
        }
    )

    confirm_password = fields.RegexField(
        regex='^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        min_length=12,
        max_length=32,
        error_messages={
            'required': '密码不能为空',
            'invalid': '密码必须包含数字，字母、特殊字符',
            'min_length': '用户名长度不小于12字符',
            'max_length': '用户名长度不大于32字符'
        }
    )

    check_code = fields.CharField(
        max_length=4,
        error_messages={'required': '验证码错误', 'max_length': '验证码错误'}
    )

    def clean_check_code(self):
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误', code='invalid')

    def clean(self):
        if 'password' in self.cleaned_data and 'confirm_password' in self.cleaned_data:
            v1 = self.cleaned_data['password']
            v2 = self.cleaned_data['confirm_password']
            if v1 == v2:
                pass
            else:
                from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
                raise ValidationError('密码输入不一致')
