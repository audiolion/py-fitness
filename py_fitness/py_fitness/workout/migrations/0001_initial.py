# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 20:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish_date', models.DateTimeField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('date', models.DateTimeField()),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('duration', models.DurationField(blank=True)),
                ('mood', models.CharField(blank=True, max_length=254)),
                ('location', models.CharField(blank=True, max_length=254)),
                ('notes', models.TextField(blank=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workout_workout_author', to=settings.AUTH_USER_MODEL)),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workout_workout_editor', to=settings.AUTH_USER_MODEL)),
                ('exercises', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout.Exercise')),
                ('uploads', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout.Attachment')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('authors', django.db.models.manager.Manager()),
            ],
        ),
    ]