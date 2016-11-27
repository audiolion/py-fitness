from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Workout, Exercise, Set


class WorkoutForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WorkoutForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Start Workout'))

    class Meta:
        model = Workout
        fields = ["date","location","mood","weight","notes"]
