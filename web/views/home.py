#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from repository import models
from utils.pagination import Pagination
from utils.util import u_response


def index(request, *args, **kwargs):
    """
    首页
    :param request:
    :return:
    """

    article_type_list = models.Article.type_choices
    print('--article_type_list--', article_type_list)
    if kwargs['article_type_id']:
        article_type_id = int(kwargs['article_type_id'])
        base_url = reverse('index', kwargs=kwargs)
    else:
        article_type_id = None
        base_url = '/'

    article_count = models.Article.objects.filter(**kwargs).count()
    page_info = Pagination(current_page=request.GET.get('p'), data_count=article_count)
    article_list = models.Article.objects.filter(**kwargs).values('title', 'summary', 'create_time').order_by('-nid')[
                   page_info.start:page_info.end]
    page_str = page_info.page_str(base_url=base_url)

    result = u_response()
    result['status'] = True
    # result['data'] = json.dumps(list(article_list))
    result['data'] = list(article_list)

    # return HttpResponse(result)
    return JsonResponse(result)
