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

    if kwargs['article_type_id']:
        article_type_id = int(kwargs['article_type_id'])
        base_url = reverse('index', kwargs=kwargs)
    else:
        article_type_id = None
        base_url = '/'

    if kwargs['article_type_id']:
        article_list = models.Article.objects \
            .filter(**kwargs) \
            .order_by('-nid') \
            .values('title', 'summary', 'create_time')

        article_count = article_list.count()
        page_info = Pagination(
            current_page=request.GET.get('page'),
            data_count=article_count, per_page_count=5,
            pager_num=5
        )
        article_list = article_list[page_info.start:page_info.end]
    else:
        article_list = models.Article.objects \
            .all() \
            .order_by('-nid') \
            .values('title', 'summary', 'create_time')
        article_count = article_list.count()
        page_info = Pagination(
            current_page=request.GET.get('page'),
            data_count=article_count, per_page_count=5,
            pager_num=5
        )
        article_list = article_list[page_info.start:page_info.end]

    page_str = page_info.page_str(base_url=base_url)

    result = u_response()
    result['status'] = True
    # result['data'] = json.dumps(list(article_list))
    result['data'] = {
        'list': list(article_list),
        'page': page_info.current_page,
        'pageSize': page_info.pager_num,
        'totalCount': page_info.data_count
    }

    # return HttpResponse(result)
    # return JsonResponse(result)
    return render(request=request, template_name='index.html')
