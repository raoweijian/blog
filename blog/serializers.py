#coding=utf8
from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article  # 定义关联的 Model
        fields = ('title', 'content', 'last_modify_time')  # 指定返回的 fields
