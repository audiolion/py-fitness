from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, DetailView, UpdateView, DeleteView, CreateView

from py_fitness.users.models import User

from .forms import WorkoutForm
from .models import Workout, Exercise, Set


class WorkoutDashboardView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        workout_form = WorkoutForm()
        return render(request, "pages/dashboard.html", context={"form": workout_form})

    def post(self, request, *args, **kwargs):
        workout_form = WorkoutForm(request.POST)
        if workout_form.is_valid():
            workout = workout_form.save(commit=False)
            workout.author = request.user
            workout.save()
            return HttpResponseRedirect(reverse('api:dashboard'))
        else:
            return render(request, 'pages/dashboard.html', context={"form": workout_form})


class WorkoutDetailView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        workout = Workout.objects.get(pk=pk)
        return render(request, 'workout/workout_detail.html', context={'workout': workout})


class WorkoutYearListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        year = kwargs.get('year')
        workouts = request.user.workout_workout_author.filter(date__year=year).order_by('date')
        return render(request, 'workout/workout_list.html', context={'workouts': workouts})


class WorkoutMonthListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        year = kwargs.get('year')
        month = kwargs.get('month')
        workouts = request.user.workout_workout_author.filter(date__year=year).filter(date__month=month).order_by('date')
        return render(request, 'workout/workout_list.html', context={'workouts': workouts})


class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    model = Workout
    form_class = WorkoutForm
    template_name = "workout/workout_list.html"
    success_url = reverse_lazy('api:workout_list')


class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    model = Workout
    template_name = "workout/workout_delete.html"
    success_url = reverse_lazy('api:workout_list')
