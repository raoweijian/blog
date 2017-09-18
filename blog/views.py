# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import logging
import urllib
import json
import markdown
import base64
import re

from django.conf import settings
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, render_to_response
from django.template.context import RequestContext
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .apps import BlogConfig
from .models import Comment

from blog.libs import common

logger = logging.getLogger('myblog.blog')

def index(request):
    """文章列表"""
    content_dir = '/'.join([settings.BASE_DIR, BlogConfig.name, BlogConfig.content_dir])
    #ls = os.popen('ls -t %s/*.md' % content_dir).readlines()
    #ls = os.popen("ls -l --time-style '+\\%Y-\\%m-\\%d \\%H:\\%M' %s/*.md" % content_dir).readlines()
    ls = os.popen("ls -t -l --time-style '+%Y-%m-%d %H:%M' " + content_dir + "/*.md").readlines()

    article_list = []
    for line in ls:
        t = re.split('\s+', line.strip(), 7)
        update_time = " ".join((t[5], t[6]))
        title = os.path.basename(t[7]).replace('.md', '')
        article_list.append([title, update_time])

    return render(request, 'index.html', {'article_list': article_list})


def new(request):
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
        #logger.info(comment.id)
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

    return render(request, 'md.html', {'content': line, 'comment_groups': new_groups})


def edit(request, file_name):
    """编辑已有的文章"""
    file_path = '/'.join([settings.BASE_DIR, BlogConfig.name, BlogConfig.content_dir, file_name])
    file_path += '.md'
    if not os.path.exists(file_path):
        return HttpResponseNotFound('<h1>Page not found</h1>')

    with open(file_path, 'r') as fp:
        content = fp.read()

    return render(request, 'edit.html', {'title': file_name, 'content': content})


def delete(request, file_name):
    """删除文章"""
    file_path = '/'.join([settings.BASE_DIR, BlogConfig.name, BlogConfig.content_dir, file_name])
    file_path += '.md'
    if os.path.exists(file_path):
        os.rename(file_path, file_path + '_bak')
    return HttpResponseRedirect('/blog')


@csrf_exempt
def publish(request):
    """发表文章"""
    content = request.POST['content']
    title = request.POST['title']
    ret = common.store_article(content, title)
    new_url = '/blog/content/' + os.path.basename(ret).replace('.md', '')
    return HttpResponse(new_url)


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


@csrf_exempt
def upload_picture(request):
    """上传图片"""
    data = urllib.parse.unquote(request.POST['abc'])
    source_code = data.split('base64,')[1]
    src = common.store_pic(source_code)

    #获取图片缩放后的大小
    full_path = os.path.join(settings.BASE_DIR, src.lstrip('/'))
    logger.info("base_dir is [%s]" % settings.BASE_DIR)
    logger.info("pic path: %s" % full_path)
    size = common.zoom_pic(full_path)

    return HttpResponse(src + " =%dx%d" % (size[0], size[1]))


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/blog')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username = username, password = password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/blog')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/blog')
