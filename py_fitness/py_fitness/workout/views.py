from datetime import datetime, timedelta
from collections import OrderedDict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Count, Avg, Min, Max
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.utils import timezone
from django.views.generic import View, ListView, DetailView, UpdateView, DeleteView, CreateView

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import FixedTicker, Label
from bokeh.models.ranges import Range1d
from bokeh.models.widgets import Dropdown

from py_fitness.users.models import User
from py_fitness.core.utils import weeks_between

from .forms import WorkoutForm, WorkoutUpdateForm, ExerciseForm, SetFormSet, SetFormSetHelper
from .models import Workout, Exercise, Set


def bokeh_avg_workouts_per_day(user):
    DAY_OF_WEEK = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0
    }
    data = user.workout_workout_author.extra({'day': 'extract(dow from date)'}).values('day').annotate(count=Count('id')).values('day', 'count')

    x_factors = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    plot = figure(title="Average Workouts per Day", height=1000, width=1000, responsive=True, x_range=x_factors, y_range=Range1d(start=0, end=1))
    plot.title.align = "center"
    plot.xaxis[0].axis_label = "Day of Week"
    plot.yaxis[0].axis_label = "Number of Workouts"

    if not data:
        plot.yaxis.bounds = (0,1)
        plot.yaxis[0].ticker=FixedTicker(ticks=[x*0.1 for x in range(0, 11)])
        plot.line(x_factors, [0,0,0,0,0,0,0], line_width=2)
        notice = Label(x=80, y=150, x_units='screen', y_units='screen',
            text="No data yet. Record a workout!", render_mode='css',
            background_fill_color='white', background_fill_alpha=1.0)
        plot.add_layout(notice)
    else:
        workout_range = user.workout_workout_author.aggregate(min=Min('date'), max=Max('date'))
        weeks = weeks_between(workout_range['min'], workout_range['max'])

        for item in data:
            DAY_OF_WEEK[item['day']] += 1
        plot.line(x_factors, [i/weeks for i in DAY_OF_WEEK.values()], line_width=2)

    script, chart = components(plot, CDN)
    return (script, chart)


def get_one_rep_max(weight, reps):
    return float(weight) / (1.0278 - (0.0278 * reps))


def bokeh_exercise_1rm_weight_over_time(user, exercise):
    data = Exercise.objects.filter(workout__author=user).filter(name__search=exercise).values('workout__date', 'sets__weight', 'sets__repetitions')

    plot = figure(title="{} 1RM Over Time (Brzycki Method)".format(exercise), height=600, width=600, responsive=True, x_axis_type="datetime")
    plot.title.align = "center"
    plot.xaxis[0].axis_label = "Date"
    plot.yaxis[0].axis_label = "Weight (lbs/kg)"

    dates_data = {}
    for item in data:
        date = item['workout__date'].date()
        if date in dates_data:
            weight = item.get('sets__weight', None)
            reps = item.get('sets__repetitions', None)
            if weight is not None and reps is not None:
                one_rep_max = get_one_rep_max(weight, reps)
                if dates_data[date] < one_rep_max:
                    dates_data[date] = one_rep_max
        else:
            weight = item.get('sets__weight', None)
            reps = item.get('sets__repetitions', None)
            if weight is not None and reps is not None:
                one_rep_max = get_one_rep_max(weight, reps)
                dates_data[date] = one_rep_max

    if not dates_data:
        today = timezone.now().date()
        plot.line([today - timedelta(days=7), today], [0,0], line_width=2)
        notice = Label(x=70, y=150, x_units='screen', y_units='screen',
            text="No data yet. Add an exercise!", render_mode='css',
            background_fill_color='white', background_fill_alpha=1.0)
        plot.add_layout(notice)
    else:
        ordered_dates = OrderedDict(sorted(dates_data.items()))
        dates = list(ordered_dates.keys())
        weights = list(ordered_dates.values())

        plot.line(dates, weights, line_width=2)
        plot.circle(dates, weights, fill_color="white", size=8)

    script, chart = components(plot, CDN)
    return (script, chart)


def bokeh_exercise_avg_weight_over_time(user, exercise):
    data = Exercise.objects.filter(workout__author=user).filter(name__search=exercise).values('workout__date', 'sets__weight')

    plot = figure(title="Average {} Weight Over Time".format(exercise), height=600, width=600, responsive=True, x_axis_type="datetime")
    plot.title.align = "center"
    plot.xaxis[0].axis_label = "Date"
    plot.yaxis[0].axis_label = "Weight (lbs/kg)"

    dates_data = {}
    for item in data:
        date = item['workout__date'].date()
        if date in dates_data:
            weight = item.get('sets__weight', None)
            if weight is not None:
                dates_data[date].append(weight)
        else:
            weight = item.get('sets__weight', None)
            if weight is not None:
                dates_data[date] = [weight]

    if not dates_data:
        today = timezone.now()
        plot.line([today - timedelta(days=7), today], [0,0], line_width=2)
        notice = Label(x=70, y=150, x_units='screen', y_units='screen',
            text="No data yet. Add an exercise!", render_mode='css',
            background_fill_color='white', background_fill_alpha=1.0)
        plot.add_layout(notice)
    else:
        for key, value in dates_data.items():
            dates_data[key] = sum(dates_data[key]) / len(dates_data[key])

        ordered_dates = OrderedDict(sorted(dates_data.items()))
        dates = list(ordered_dates.keys())
        weights = list(ordered_dates.values())

        plot.line(dates, weights, line_width=2)
        plot.circle(dates, weights, fill_color="white", size=8)

    script, chart = components(plot, CDN)
    return (script, chart)


def bokeh_exercise_max_weight_over_time(user, exercise):
    data = Exercise.objects.filter(workout__author=user).filter(name__search=exercise).values('workout__date', 'sets__weight')

    plot = figure(title="Highest {} Weight Over Time".format(exercise), height=600, width=600, responsive=True, x_axis_type="datetime")
    plot.title.align = "center"
    plot.xaxis[0].axis_label = "Date"
    plot.yaxis[0].axis_label = "Weight (lbs/kg)"

    dates_data = {}
    for item in data:
        date = item['workout__date'].date()
        if date in dates_data:
            weight = item.get('sets__weight', None)
            if weight is not None and weight > dates_data[date]:
                dates_data[date] = weight
        else:
            weight = item.get('sets__weight', None)
            if weight is not None:
                dates_data[date] = weight

    if not dates_data:
        today = timezone.now()
        plot.line([today - timedelta(days=7), today], [0,0], line_width=2)
        notice = Label(x=70, y=150, x_units='screen', y_units='screen',
            text="No data yet. Add an exercise!", render_mode='css',
            background_fill_color='white', background_fill_alpha=1.0)
        plot.add_layout(notice)
    else:
        ordered_dates = OrderedDict(sorted(dates_data.items()))
        dates = list(ordered_dates.keys())
        weights = list(ordered_dates.values())

        plot.line(dates, weights, line_width=2)
        plot.circle(dates, weights, fill_color="white", size=8)

    script, chart = components(plot, CDN)
    return (script, chart)


def bokeh_weight_over_time(user):
    data = user.workout_workout_author.all().values('date', 'weight')

    plot = figure(title="Weight Over Time", height=600, width=600, responsive=True, x_axis_type="datetime")
    plot.title.align = "center"
    plot.xaxis[0].axis_label = "Date"
    plot.yaxis[0].axis_label = "Weight (lbs/kg)"

    if not data:
        today = timezone.now()
        plot.line([today - timedelta(days=7), today], [0,0], line_width=2)
        notice = Label(x=70, y=150, x_units='screen', y_units='screen',
            text="No data yet. Record your weight in a workout!", render_mode='css',
            background_fill_color='white', background_fill_alpha=1.0)
        plot.add_layout(notice)
    else:
        dates = []
        weight = []
        for item in data:
            dates.append(item['date'])
            if item.get('weight', None) is not None:
                weight.append(item['weight'])

        plot.line(dates, weight, line_width=2)
        plot.circle(dates, weight, fill_color="white", size=8)

    script, chart = components(plot, CDN)
    return (script, chart)


class WorkoutDashboardView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        workout_form = WorkoutForm()
        workouts = request.user.workout_workout_author.filter(date__month__gte=timezone.now().month-1).order_by('-date')

        avg_workouts_script, avg_workouts_chart = bokeh_avg_workouts_per_day(request.user)
        weight_change_script, weight_change_chart = bokeh_weight_over_time(request.user)

        return render(request, "pages/dashboard.html", context={"form": workout_form,
            "workouts": workouts, "avg_workouts_script": avg_workouts_script,
            "avg_workouts_chart": avg_workouts_chart, "weight_change_script": weight_change_script,
            "weight_change_chart": weight_change_chart})

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
    form_class = WorkoutUpdateForm
    template_name = "workout/workout_form.html"

    def get_success_url(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        pk = self.kwargs.get('pk')
        return reverse_lazy('workout:workout_detail', kwargs={"year": year, "month": month, "pk": pk})


class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    model = Workout
    template_name = "workout/workout_delete.html"
    success_url = reverse_lazy('workout:dashboard')


class ExerciseDetailView(LoginRequiredMixin, DetailView):
    model = Exercise
    template_name = "workout/exercise_detail.html"


class ExerciseListView(LoginRequiredMixin, ListView):
    model = Exercise
    template_name = "workout/exercise_list.html"

    def get_context_data(self, **kwargs):
        context = super(ExerciseDetailView, self).get_context_data(**kwargs)
        query = kwargs.get('query')
        exercise_avg_script, exercise_avg_chart = bokeh_exercise_avg_weight_over_time(self.request.user, query)
        exercise_max_script, exercise_max_chart = bokeh_exercise_max_weight_over_time(self.request.user, query)
        exercise_1rm_script, exercise_1rm_chart = bokeh_exercise_1rm_weight_over_time(self.request.user, query)
        return context

    def get_queryset(self):
        query = self.kwargs.get('query')
        queryset = Exercise.objects.filter(workout__author=self.request.user).filter(name__search=query)
        return queryset


class ExerciseDeleteView(LoginRequiredMixin, DeleteView):
    model = Exercise
    template_name = "workout/exercise_delete.html"
    pk_url_kwarg = "epk"

    def get_success_url(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        pk = self.kwargs.get('pk')
        return reverse_lazy('workout:workout_detail', kwargs={"year": year, "month": month, "pk": pk})


class ExerciseUpdateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        exercise = Exercise.objects.get(pk=kwargs.get('epk'))
        exercises = Exercise.objects.filter(name__search=exercise.name)
        formset = SetFormSet(instance=exercise)

        exercise_avg_script, exercise_avg_chart = bokeh_exercise_avg_weight_over_time(request.user, exercise.name)
        exercise_max_script, exercise_max_chart = bokeh_exercise_max_weight_over_time(request.user, exercise.name)
        exercise_1rm_script, exercise_1rm_chart = bokeh_exercise_1rm_weight_over_time(request.user, exercise.name)

        return render(request, "workout/exercise_form.html",
            context={"formset": formset, "exercise": exercise, "exercises": exercises, "helper": SetFormSetHelper(),
                     "exercise_avg_script": exercise_avg_script, "exercise_avg_chart": exercise_avg_chart,
                     "exercise_max_script": exercise_max_script, "exercise_max_chart": exercise_max_chart,
                     "exercise_1rm_script": exercise_1rm_script, "exercise_1rm_chart": exercise_1rm_chart})

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
