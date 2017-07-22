# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import urllib
import json
import markdown

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse

from .apps import BlogConfig

# Create your views here.

def index(request):
    content_dir = '/'.join([settings.BASE_DIR, BlogConfig.name, BlogConfig.content_dir])
    ls = os.popen('ls %s' % content_dir).readlines()
    ls = map(lambda x: x.strip(), [y for y in ls])
    ls = map(lambda x: x.replace('.md', ''), [y for y in ls])
    return render(request, 'index.html', {'article_list': ls})


def content(request, file_name):
    file_path = '/'.join([settings.BASE_DIR, BlogConfig.name, BlogConfig.content_dir, file_name])
    file_path += '.md'

    with open(file_path, 'r') as fp:
        line = fp.read()
    html = markdown.markdown(line)
    return render(request, 'md.html', {'content': html})
