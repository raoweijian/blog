#coding=utf8
from __future__ import unicode_literals

import logging
import urllib
import zipfile
import re

from django.conf import settings
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, render_to_response
from django.template.context import RequestContext
from django.urls import reverse
from django.core.management import call_command
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import StreamingHttpResponse

from .apps import BlogConfig

from blog.libs import common
from .models import Article

logger = logging.getLogger('myblog.blog')

def index(request):
    """文章列表"""
    article_list = []
    for article in Article.objects.order_by("-last_modify_time"):
        title = article.title
        update_time = article.last_modify_time.strftime("%Y-%m-%d %H:%M")
        article_list.append([title, update_time])

    return render(request, 'index.html', {'article_list': article_list})


def new(request):
    """编辑器"""
    return render(request, 'edit.html', {"title": "", "content": ""})


def content(request, title):
    """全文页面"""
    if settings.DATABASES['default']['PORT'] == '4050':
        title = urllib.unquote(str(title))
    else:
        title = urllib.unquote(title)
    article = Article.objects.get(title = title)

    return render(request, 'md.html', {'content': article.content})


def edit(request, title):
    """编辑已有的文章"""
    if settings.DATABASES['default']['PORT'] == '4050':
        title = urllib.unquote(str(title))
    else:
        title = urllib.unquote(title)
    article = Article.objects.get(title = title)

    return render(request, 'edit.html', {'title': title, 'content': article.content})


def delete(request, title):
    """删除文章"""
    if settings.DATABASES['default']['PORT'] == '4050':
        title = urllib.unquote(str(title))
    else:
        title = urllib.unquote(title)

    article = Article.objects.get(title = title)
    article.delete()
    return HttpResponseRedirect('/')


@csrf_exempt
def publish(request):
    """发表文章"""
    content = request.POST['content']
    title = request.POST['title']
    article = Article.objects.filter(title = title).first()

    #如果标题改了，没有了，就重新插入一个
    if article is None:
        logger.info("重新插入: %s" % title)
        article = Article(title =  title, content = content)
    else:
        article.content = content
    article.save()

    new_url = '/content/' + title
    return HttpResponse(new_url)


@csrf_exempt
def submit_comment(request):
    #获取评论内容、用户名以及引用的id
    request_url = request.POST['current_url']
    article_name = request_url.split('/')[-1]
    article_name = urllib.parse.unquote(article_name).rstrip('#') + ".md"

    #找到引用的那一条数据
    group_id = None
    comment_id = None
    if 'comment_id' in request.POST:
        ref_comment_id = request.POST['comment_id']
        #logger.info("ref_comment_id: %s", ref_comment_id)
        comment_id = int(ref_comment_id.split('_')[1])
        refered = Comment.objects.get(id = comment_id)
        group_id = refered.group
    else:
        comments = Comment.objects.order_by('-group')
        if len(comments) == 0:
            group_id = 1
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
    data = urllib.unquote(request.POST['abc'])
    source_code = data.split('base64,')[1]
    src = common.get_pic_src(source_code)

    return HttpResponse(src)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username = username, password = password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def migrate(request):
    call_command("migrate")
    return HttpResponse("migrate done")


"""
从 zip 文件导入
"""
def _import(request):
    if not request.user.is_authenticated():
        logger.error("未登录用户不允许上传!")
        return HttpResponseRedirect('/')

    if request.method == "POST":
        file_name = common.save_upload_file(request.FILES['file'])
        azip = zipfile.ZipFile(file_name)
        for title in azip.namelist():
            content = azip.read(title)
            title = re.sub('\.md$', '', title)
            article = Article.objects.filter(title = title).first()
            if article is None:
                article = Article(title = title, content = content)
            else:
                article.content = content
            article.save()
    return HttpResponseRedirect('/')


"""
导出所有内容
"""
def export(request):
    zip_file_name = "export.zip"
    azip = zipfile.ZipFile(zip_file_name, 'w')
    for article in Article.objects.all():
        file_name = "%s.md" % article.title
        azip.writestr(file_name, article.content.encode("utf8"), compress_type = zipfile.ZIP_DEFLATED)
    azip.close()
    file_obj = open(zip_file_name, 'rb')
    response = StreamingHttpResponse(file_obj)

    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="export.zip"'
    return response
