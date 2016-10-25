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
]
