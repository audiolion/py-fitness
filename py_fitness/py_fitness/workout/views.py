from django.shortcuts import render
from django.views.generic import View, DetailView

from .models import Workout, Exercise, Set


class WorkoutDetail(DetailView):
    model = Workout


class ExerciseDetail(DetailView):
    model = Exercise