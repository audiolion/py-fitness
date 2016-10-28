# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<pk>[0-9]+)/$',
        view=views.WorkoutDetail.as_view(),
        name='workout_detail'
    ),
    url(
        regex=r'^exercises/(?P<slug>[-\w]+)/$',
        view=views.ExerciseDetail.as_view(),
        name='exercise_detail'
    ),
    url(
        regex=r'^api/exercises/$',
        view=views.ApiExerciseList.as_view(),
        name='api_exercise_list'
    ),
    url(
        regex=r'^api/exercises/(?P<slug>[-\w]+)/$',
        view=views.ApiExerciseDetail.as_view(),
        name='api_exercise_detail'
    ),
    url(
        regex=r'^api/exercises/(?P<slug>[-\w]+)/sets/$',
        view=views.ApiSetList.as_view(),
        name='api_set_list'
    ),
    url(
        regex=r'^api/exercises/(?P<slug>[-\w]+)/sets/(?P<pk>[0-9]+)/$',
        view=views.ApiSetDetail.as_view(),
        name='api_set_detail'
    )
]
