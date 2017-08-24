# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import logging
import urllib
import json
import urllib
import markdown

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .apps import BlogConfig

from .models import Comment

logger = logging.getLogger('myblog.blog')

# Create your views here.

def index(request):
    """文章列表"""
    content_dir = '/'.join([settings.BASE_DIR, BlogConfig.name, BlogConfig.content_dir])
    ls = os.popen('ls %s' % content_dir).readlines()
    ls = map(lambda x: x.strip().replace('.md', ''), [y for y in ls])
    return render(request, 'index.html', {'article_list': ls})


def edit(request):
    """编辑器"""
    return render(request, 'edit.html')


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
        logger.info(comment.id)
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
    new_groups = []

    for group_id in sorted(groups.keys()):
        new_groups.append(groups[group_id])

    return render(request, 'md.html', {'content': html, 'comment_groups': new_groups})


@csrf_exempt
def submit_comment(request):
    """
    用户提交评论
    """
    #获取评论内容、用户名以及引用的id
    request_url = request.POST['current_url']
    article_name = request_url.split('/')[-1]
    article_name = urllib.parse.unquote(article_name).rstrip('#') + ".md"

    #找到引用的那一条数据
    comment_id = None
    if 'comment_id' in request.POST:
        ref_comment_id = request.POST['comment_id']
        #logger.info("ref_comment_id: %s", ref_comment_id)
        comment_id = int(ref_comment_id.split('_')[1])
        refered = Comment.objects.get(id = comment_id)
        group_id = refered.group
    else:
        comment = Comment.objects.order_by('-group')[0]
        group_id = comment.group + 1

    #创建新数据
    new_comment = Comment(
        article_name = article_name,
        user_name = request.POST['user_name'],
        content = request.POST['content'],
        ref = comment_id,
        group = group_id
    )
    new_comment.save()
    return HttpResponse("comment_" + str(new_comment.id))
