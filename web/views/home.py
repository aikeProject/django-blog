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
    else:
        article_type_id = None

    if kwargs['article_type_id']:
        # 获取文章列表 按时间排序倒序
        article_list = models.Article.objects \
            .filter(**kwargs) \
            .order_by('-create_time') \
            .values('title', 'summary', 'create_time')

        article_count = article_list.count()
        page_info = Pagination(
            current_page=request.GET.get('page'),
            data_count=article_count, per_page_count=5,
            pager_num=5
        )

        # 最新评论文章
        article_comment_list = models.Comment.objects \
                                   .filter(article__article_type_id=kwargs['article_type_id']) \
                                   .order_by('-create_time') \
                                   .values('article__title', 'article__summary', 'article__create_time')[0:10]

        article_list = article_list[page_info.start:page_info.end]
    else:
        article_list = models.Article.objects \
            .all() \
            .order_by('-create_time') \
            .values('title', 'summary', 'create_time')
        article_count = article_list.count()
        page_info = Pagination(
            current_page=request.GET.get('page'),
            data_count=article_count, per_page_count=5,
            pager_num=5
        )

        article_comment_list = models.Comment.objects \
                                   .all() \
                                   .order_by('-create_time') \
                                   .values('article__title', 'article__summary', 'article__create_time')[0:10]

        article_list = article_list[page_info.start:page_info.end]

    return render(
        request=request,
        template_name='index.html',
        context={
            'article_type_list': article_type_list,
            'article_type_id': article_type_id,
            'article_list': article_list,
            'page_info': page_info,
            'page_count_list': [(i + 1) for i in range(page_info.total_count)],
            'article_comment_list': article_comment_list
        }
    )
