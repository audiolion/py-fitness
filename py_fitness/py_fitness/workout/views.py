from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.utils import timezone
from django.views.generic import View, DetailView, UpdateView, DeleteView, CreateView

from py_fitness.users.models import User

from .forms import WorkoutForm, ExerciseForm, SetFormSet, SetFormSetHelper
from .models import Workout, Exercise, Set


class WorkoutDashboardView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        workout_form = WorkoutForm()
        workouts = request.user.workout_workout_author.filter(date__month__gte=timezone.now().month-1).order_by('-date')
        return render(request, "pages/dashboard.html", context={"form": workout_form, "workouts": workouts})

    def post(self, request, *args, **kwargs):
        workout_form = WorkoutForm(request.POST)
        if workout_form.is_valid():
            workout = workout_form.save(commit=False)
            workout.author = request.user
            workout.save()
            return HttpResponseRedirect(workout.get_absolute_url())
        else:
            return render(request, 'pages/dashboard.html', context={"form": workout_form})


class WorkoutDetailView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        workout = Workout.objects.select_related('author').get(pk=pk)
        exercises = workout.exercises.all()
        form = ExerciseForm()
        if not workout.finished:
            time = timezone.now() - workout.created
        return render(request, 'workout/workout_detail.html', context={ 'workout': workout,
                                                                        'exercises': exercises,
                                                                        'form': form,
                                                                        'time': time})

    def post(self, request, *args, **kwargs):
        exercise_form = ExerciseForm(request.POST)
        workout = Workout.objects.get(pk=kwargs.get('pk'))
        if exercise_form.is_valid():
            exercise = exercise_form.save(commit=False)
            exercise.workout = workout
            exercise.save()
            return HttpResponseRedirect(reverse('workout:exercise_update', kwargs={ 'year': workout.date.year,
                                                                                    'month': workout.date.month,
                                                                                    'pk': workout.pk,
                                                                                    'epk': exercise.pk}))
        return render(request, 'workout/workout_detail.html', context={'workout': workout, 'form': exercise_form})


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
    success_url = reverse_lazy('workout:workout_list')


class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    model = Workout
    template_name = "workout/workout_delete.html"
    success_url = reverse_lazy('workout:workout_list')


class ExerciseUpdateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        exercise = Exercise.objects.get(pk=kwargs.get('epk'))
        formset = SetFormSet(instance=exercise)
        return render(request, "workout/exercise_form.html",
            context={"formset": formset, "exercise": exercise, "helper": SetFormSetHelper()})

    def post(self, request, *args, **kwargs):
        exercise = Exercise.objects.get(pk=kwargs.get('epk'))
        formset = SetFormSet(request.POST, request.FILES, instance=exercise)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(
                reverse('workout:workout_detail', kwargs={
                    'year': exercise.workout.date.year,
                    'month': exercise.workout.date.month,
                    'pk': exercise.workout.pk}
                )
            )
        return render(request, "workout/exercise_form.html",
            context={"formset": formset, "exercise": exercise, "helper": SetFormSetHelper()})
