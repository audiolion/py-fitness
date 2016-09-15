# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-15 04:33
from __future__ import unicode_literals

from decimal import Decimal
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
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('notes', models.CharField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_number', models.IntegerField(blank=True, null=True)),
                ('weight', models.DecimalField(decimal_places=3, default=Decimal('0.000'), max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Repetition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('half', models.BooleanField(default=False, help_text="Half-rep, only went through half of the range of motion, usually occurs when muscle failure isn't reached for the bottom half of range of motion.")),
                ('negative', models.BooleanField(default=False, help_text='Negative rep, started at top of positive range of motion, typically formed at the end of a set for absolute muscle failure.')),
                ('positive', models.BooleanField(default=False, help_text='Positive rep, did not resist weight on the negative portion of rep, typically done in plyometric workouts.')),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workout_workout_author', to=settings.AUTH_USER_MODEL)),
                ('editor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workout_workout_editor', to=settings.AUTH_USER_MODEL)),
                ('exercises', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout.Exercise')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('authored', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='exerciseset',
            name='repititions',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout.Repetition'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='exercise_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout.ExerciseSet'),
        ),
    ]
