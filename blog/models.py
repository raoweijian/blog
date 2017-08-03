# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.db import models

# Create your models here.

class Comment(models.Model):
    article_name = models.CharField(max_length = 255, null = False, blank = False)
    user_name = models.CharField(max_length = 255, null = False, blank = False)
    content = models.CharField(max_length = 1024, null = False, blank = False)
    ref = models.IntegerField(null = True, blank = True)
    group = models.IntegerField(null = False, blank = False, default = 0)
    ctime = models.DateTimeField('date published', auto_now_add = True, blank = False, null = False)
