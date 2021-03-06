#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from django.http import HttpResponse, JsonResponse
from django.db.models import Max
from django.shortcuts import render, redirect
from django.core import serializers
from django.urls import reverse
from repository import models
from utils.pagination import Pagination


def index(request, *args, **kwargs):
    """
    公共 首页
    :param request:
    :return:
    """

    article_type_list = models.Article.type_choices

    if kwargs:
        # 获取文章列表 按时间排序倒序
        article_list = models.Article.objects \
            .filter(**kwargs) \
            .order_by('-create_time') \
            .values('title', 'summary', 'create_time', 'category__title', 'comment_count')

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
            .values('title', 'summary', 'create_time', 'category__title', 'comment_count')
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

    article_all = models.Article.objects.all()
    #  查看最多的数据
    article_hot = article_all.aggregate(Max('read_count'))
    article_hot_one = models.Article.objects \
        .filter(read_count=article_hot['read_count__max']) \
        .values('title', 'summary', 'create_time').first()

    # 日志总篇数
    article_sum = article_all.count()

    return render(
        request=request,
        template_name='index.html',
        context={
            'article_type_list': article_type_list,
            'article_list': article_list,
            'page_info': page_info,
            'page_count_list': [(i + 1) for i in range(page_info.total_count)],
            'article_comment_list': article_comment_list,
            'article_hot_one': article_hot_one,
            'article_sum': article_sum,
            'article_type_id': int(kwargs['article_type_id']) if kwargs and kwargs['article_type_id'] else 0
        }
    )


def home(request, site):
    """
    个人主页
    :param request:
    :param site:
    :return:
    """

    if site:
        blog = models.Blog.objects.filter(site=site).select_related('user').first()
        # 没有这个博客 跳转到首页
        if not blog:
            return redirect('/')

        # 登录之后
        if request.session['user_info'] and (not blog.site):
            return redirect('/createBlog')

        # 标签
        tag_list = models.Tag.objects.filter(blog=blog)
        # 个人博客分类
        category_list = models.Category.objects.filter(blog=blog)
        # Article 文章
        article_list = models.Article.objects.filter(blog=blog)
        date_list = models.Article.objects.raw(
            'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')

        page_info = Pagination(
            current_page=request.GET.get('page'),
            data_count=article_list.count(), per_page_count=5,
            pager_num=5
        )
        article_list = article_list[page_info.start:page_info.end]
        return render(request=request, template_name='home.html', context={
            'tag_list': tag_list,
            'category_list': category_list,
            'article_list': article_list,
            'site': site,
            'page_info': page_info,
            'blog': blog,
            'date_list': date_list
        })
    else:
        return redirect('/')


def filter_home(request, site, condition, val):
    print('site', site)
    print('condition', condition)
    print('val', val)
    if site:
        blog = models.Blog.objects.filter(site=site).select_related('user').first()
        print('blog', blog)
        if not blog:
            return redirect('/')
        tag_list = models.Tag.objects.filter(blog=blog)
        category_list = models.Category.objects.filter(blog=blog)
        date_list = models.Article.objects.raw(
            'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')

        if condition == 'tag':
            article_list = models.Article.objects.filter(tags=val, blog=blog).all()
            print('article_list tag', article_list)
        elif condition == 'category':
            article_list = models.Article.objects.filter(category_id=val, blog=blog).all()
            print('article_list category', article_list)
        elif condition == 'date':
            article_list = models.Article.objects.filter(blog=blog).extra(
                where=['strftime("%%Y-%%m",create_time)=%s'], params=[val, ]).all()
            print('article_list date', article_list)
        else:
            article_list = []

        page_info = Pagination(
            current_page=request.GET.get('page'),
            data_count=article_list.count() if article_list else 0,
            per_page_count=5,
            pager_num=5
        )
        article_list = article_list[page_info.start:page_info.end]
        return render(request=request, template_name='home.html', context={
            'tag_list': tag_list,
            'category_list': category_list,
            'article_list': article_list,
            'date_list': date_list,
            'site': site,
            'page_info': page_info,
            'blog': blog,
            'condition': condition,
            'val_nid': int(val) if val.find('-') == -1 else val
        })
    else:
        return redirect('/')


def not_found(request):
    from django.shortcuts import render_to_response
    return render_to_response(template_name='404.html', status=404)
