#!/usr/bin/env python
#coding=utf8
# Author: raoweijian - raoweijian331@qq.com
#
# Last modified: 2017-08-31 23:41
#
# Filename: common.py
#
# Description:

import random
import os
import logging
import base64
import urllib

from django.conf import settings
from qiniu import Auth, put_file, etag

from PIL import Image

logger = logging.getLogger('myblog.blog')

def get_pic_src(data):
    """存储图片"""
    #先写入本地临时文件
    file_name = rand_name() + ".png"
    logger.debug("file_name: %s" % file_name)

    imgdata = base64.b64decode(data)
    with open(file_name, 'wb') as fp:
        fp.write(imgdata)

    #上传到七牛云
    size = zoom_pic(file_name)
    src = upload_to_qiniu(file_name)

    #删除临时文件
    os.remove(file_name)

    return src + " =%dx%d" % (size[0], size[1])


"""上传图片到七牛云"""
def upload_to_qiniu(file_name):
    access_key = 'zf76R_XB46jVYMbAA8Lb3HhLid-R9nYALrsuJrsS'
    secret_key = 'Q-BxLrFl2uy53bpGwMx2VunTrb7d_tdhvhIzlqZV'
    bucket_name = 'rwj-pic-store'
    site = "http://ovh9b5ele.bkt.clouddn.com/"

    q = Auth(access_key, secret_key)

    key = file_name
    token = q.upload_token(bucket_name, key, 3600)

    ret, info = put_file(token, key, file_name)

    if ret["key"] == key:
        return site + key
    else:
        logger.error("上传图片失败: %s" % info)
        raise


def zoom_pic(filename, max_width = 1100):
    """缩放图片，方便展示"""
    img = Image.open(filename)
    width = img.size[0]
    if width <= max_width:
        return img.size
    else:
        ratio = float(max_width) / width
        height = int(ratio * img.size[1])
        return (max_width, height)


def rand_name(length = 20):
    """随机生成一个字符串"""
    inds = list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123))
    ret = ""
    for i in range(length):
        num = random.choice(inds)
        ret += chr(num)
    return ret


def save_upload_file(file):
    file_name = "import.zip"
    logger.info("upload file name: %s" % str(file))
    with open(file_name, 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    return file_name


"""把url编码的字符串还原"""
def unquote(title):
    # 这里判断端口 4050，是因为我把它部署在了 BAE 上，BAE 提供的数据库端口都是 4050。
    # 另外一个比较蛋疼的问题是，bae 上 title 传进来的时候是 unicode，而我本地部署时，title 是 str，所以处理方式有些不同
    return urllib.parse.unquote(str(title)) if settings.DATABASES['default']['PORT'] == '4050' else urllib.parse.unquote(title)
