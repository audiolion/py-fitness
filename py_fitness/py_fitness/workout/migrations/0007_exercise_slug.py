# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-25 01:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0006_auto_20161024_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='slug',
            field=models.SlugField(default='unknown', max_length=140, unique=True),
            preserve_default=False,
        ),
    ]
