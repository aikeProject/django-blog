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

    # password = fields.CharField()

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
