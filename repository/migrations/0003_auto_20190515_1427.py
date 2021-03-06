# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-05-15 06:27
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0002_auto_20190512_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='back', to='repository.Comment', verbose_name='回复评论'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.ImageField(upload_to='static/avatar', verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='password',
            field=models.CharField(max_length=64, validators=[django.core.validators.RegexValidator(message='密码必须包含数字，字母、特殊字符', regex='^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\\%\\^\\&\\*\\(\\)])[0-9a-zA-Z!@#$\\%\\^\\&\\*\\(\\)]{8,32}$')], verbose_name='密码'),
        ),
    ]
