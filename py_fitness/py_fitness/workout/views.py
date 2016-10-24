from django.shortcuts import render
from django.views.generic import View, DetailView

from .models import Workout


class WorkoutDetail(DetailView):
    model = Workout