# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 21:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0004_auto_20161024_1634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workout',
            name='uploads',
        ),
        migrations.DeleteModel(
            name='Attachment',
        ),
    ]
