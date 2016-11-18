from django import forms

from .models import Workout, Exercise, Set


class WorkoutForm(forms.ModelForm):

    class Meta:
        model = Workout
        fields = ["date","location","mood","weight","notes"]
