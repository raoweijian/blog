# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-17 20:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20180317_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=100, unique=True, verbose_name='\u6807\u9898'),
        ),
    ]