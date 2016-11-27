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
        view=views.WorkoutUpdateView.as_view(),
        name='workout_delete'
    ),
    # url(
    #     regex=r'^workouts/$',
    #     view=views.ApiWorkoutList.as_view(),
    #     name='workout_list'
    # ),
    # url(
    #     regex=r'^workouts/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<pk>[0-9]+)/$',
    #     view=views.ApiWorkoutDetail.as_view(),
    #     name='workout_detail'
    # ),
    # url(
    #     regex=r'^exercises/$',
    #     view=views.ApiExerciseList.as_view(),
    #     name='exercise_list'
    # ),
    # url(
    #     regex=r'^exercises/(?P<slug>[-\w]+)/$',
    #     view=views.ApiExerciseDetail.as_view(),
    #     name='exercise_detail'
    # ),
    # url(
    #     regex=r'^exercises/(?P<slug>[-\w]+)/sets/$',
    #     view=views.ApiSetList.as_view(),
    #     name='set_list'
    # ),
    # url(
    #     regex=r'^exercises/(?P<slug>[-\w]+)/sets/(?P<pk>[0-9]+)/$',
    #     view=views.ApiSetDetail.as_view(),
    #     name='set_detail'
    # ),
    # url(
    #     regex=r'^users/$',
    #     view=views.ApiUserList.as_view(),
    #     name='user_view'
    # ),
    # url(
    #     regex=r'^users/(?P<pk>[0-9]+)/$',
    #     view=views.ApiUserDetail.as_view(),
    #     name='user_detail'
    # ),
]
