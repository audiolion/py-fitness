# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^dashboard/$',
        view=views.WorkoutDashboardView.as_view(),
        name='dashboard'
    ),
    url(
        regex=r'^(?P<year>[0-9]{4})/$',
        view=views.WorkoutYearListView.as_view(),
        name='workout_list_year'
    ),
    url(
        regex=r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
        view=views.WorkoutMonthListView.as_view(),
        name='workout_list_month'
    ),
    url(
        regex=r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<pk>[0-9]+)/$',
        view=views.WorkoutDetailView.as_view(),
        name='workout_detail'
    ),
    url(
        regex=r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<pk>[0-9]+)/edit$',
        view=views.WorkoutUpdateView.as_view(),
        name='workout_update'
    ),
    url(
        regex=r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<pk>[0-9]+)/delete$',
        view=views.WorkoutDeleteView.as_view(),
        name='workout_delete'
    ),
    # url(
    #     regex=r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<pk>[0-9]+)/exercise/add$',
    #     view=views.ExerciseCreateView.as_view(),
    #     name='exercise_create'
    # ),
    url(
        regex=r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<pk>[0-9]+)/exercise/(?P<epk>[0-9]+)/edit$',
        view=views.ExerciseUpdateView.as_view(),
        name='exercise_update'
    ),
    url(
        regex=r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<pk>[0-9]+)/exercise/(?P<epk>[0-9]+)/delete$',
        view=views.ExerciseDeleteView.as_view(),
        name='exercise_delete'
    ),
    url(
        regex=r'^exercises/(?P<query>[-\w]+)/$',
        view=views.ExerciseListView.as_view(),
        name='exercise_list'
    ),
]
