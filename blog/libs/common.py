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
    access_key = ''
    secret_key = ''
    bucket_name = ''
    site = ""

    q = Auth(access_key, secret_key)

    key = file_name
    token = q.upload_token(bucket_name, key, 3600)

    ret, info = put_file(token, key, file_name)

    if ret["key"] == key:
        return site + key
    else:
        logger.error("上传图片失败: %s" % info)
        raise


def zoom_pic(filename, max_width = 550):
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
