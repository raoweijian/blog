# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField("标题", max_length = 100, unique = True)
    content = models.TextField("内容")
    last_modify_time = models.DateTimeField("最后修改时间", auto_now = True)
