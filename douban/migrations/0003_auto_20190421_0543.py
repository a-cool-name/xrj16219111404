# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-04-21 05:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('douban', '0002_movie_info2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='info2',
            field=models.CharField(default=True, max_length=256),
        ),
    ]
