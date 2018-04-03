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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .apps import BlogConfig

from blog.libs import common
from .models import Article
from .serializers import ArticleSerializer

logger = logging.getLogger('myblog.blog')


class ArticleViewset(viewsets.ModelViewSet):
    """
    the viewset let us can get data from api url
    like:curl - H 'application/json;indent=4' http://localhost:8080/api/articles/
    of course,we can get some author's article through:
    http://localhost:8080/api/articles/?author=2(author's id)
    Generally,people like to see json data,so when visit by browser,you should add
    ?format=json ,that is,http://localhost:8080/api/articles/?format=json
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('title',)
