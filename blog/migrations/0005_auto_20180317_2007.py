# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-17 20:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20180316_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=100, verbose_name='\u6807\u9898'),
        ),
    ]
