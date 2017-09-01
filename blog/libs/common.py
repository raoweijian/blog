#!/usr/bin/env python
#coding=utf8
# Author: raoweijian - raoweijian331@qq.com
#
# Last modified: 2017-08-31 23:41
#
# Filename: common.py
#
# Description: 

from django.conf import settings
import random
import os
import base64

def store_pic(data):
    """存储图片"""
    #生成文件名
    file_name = rand_name() + ".png"
    full_path = os.path.join(settings.BASE_DIR, "static/images/blog/", file_name)

    imgdata = base64.b64decode(data)
    with open(full_path, 'wb') as fp:
        fp.write(imgdata)

    return os.path.join("/static/images/blog", file_name)


def rand_name(length = 8):
    inds = list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123))
    ret = ""
    for i in range(length):
        num = random.choice(inds)
        ret += chr(num)
    return ret

def store_article(content, title):
    """存储文章"""
    full_path = os.path.join(settings.BASE_DIR, "blog/content", "%s.md" % title)
    with open(full_path, 'w') as fp:
        fp.write(content)
    return full_path
