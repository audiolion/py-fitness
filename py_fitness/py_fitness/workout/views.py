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


class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    model = Workout
    form_class = WorkoutForm
    template_name = "workout/workout_list.html"
    success_url = reverse_lazy('api:workout_list')


class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    model = Workout
    template_name = "workout/workout_delete.html"
    success_url = reverse_lazy('api:workout_list')
