# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import logging
import urllib
import json
import markdown

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse

from .apps import BlogConfig

from .models import Comment

logger = logging.getLogger('myblog.blog')

# Create your views here.

def index(request):
    content_dir = '/'.join([settings.BASE_DIR, BlogConfig.name, BlogConfig.content_dir])
    ls = os.popen('ls %s' % content_dir).readlines()
    ls = map(lambda x: x.strip().replace('.md', ''), [y for y in ls])
    return render(request, 'index.html', {'article_list': ls})


def content(request, file_name):
    """全文页面"""
    #解析markdown内容
    file_path = '/'.join([settings.BASE_DIR, BlogConfig.name, BlogConfig.content_dir, file_name])
    file_path += '.md'
    with open(file_path, 'r') as fp:
        line = fp.read()
    html = markdown.markdown(line, ['codehilite'])

    #获取评论
    try:
        comments = Comment.objects.filter(article_name = "%s.md" % file_name).order_by('ctime')
    except Comment.DoesNotExist:
        comments = []

    #整理评论关系
    groups = {}
    for comment in comments:
        group_id = comment.group
        if group_id not in groups:
            groups[group_id] = []

        append = {}
        append['user_name'] = comment.user_name
        append['content'] = comment.content
        append['id'] = comment.id
        if comment.ref is None:
            append['ref_user'] = None
        else:
            ref = Comment.objects.get(id = comment.ref)
            append['ref_user'] = ref.user_name
        groups[group_id].append(append)

    return render(request, 'md.html', {'content': html, 'comments': groups})
