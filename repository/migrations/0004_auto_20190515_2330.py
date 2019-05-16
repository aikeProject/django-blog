# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-05-15 15:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_auto_20190515_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='static/avatar', verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='nickname',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='昵称'),
        ),
    ]