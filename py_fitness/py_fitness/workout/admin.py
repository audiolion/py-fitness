# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin

import nested_admin

from .models import Workout, Exercise, Set


class SetInline(nested_admin.NestedStackedInline):
    model = Set
    sortable_field_name = "number"


class ExerciseInline(nested_admin.NestedStackedInline):
    model = Exercise
    sortable_field_name = "name"
    inlines = [SetInline]


class WorkoutAdmin(nested_admin.NestedModelAdmin):
    inlines = [ExerciseInline,]

admin.site.register(Workout, WorkoutAdmin)
