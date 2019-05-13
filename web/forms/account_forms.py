#!/usr/bin/env python
# -*- coding:utf-8 -*-


from django.core.exceptions import ValidationError
from django import forms
from django.forms import fields
from .base import BaseForm


class LoginForm(BaseForm, forms.Form):
    username = fields.CharField()
