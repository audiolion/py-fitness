from django import forms
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Layout, MultiField, Fieldset, Submit, Button

from .models import Workout, Exercise, Set


class WorkoutForm(forms.ModelForm):
    notes = forms.CharField(required=False, widget=forms.Textarea())
    title = forms.CharField(required=False, help_text="ex/ P90x Day 3 - Back & Biceps")
    def __init__(self, *args, **kwargs):
        super(WorkoutForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Start Workout'))

    class Meta:
        model = Workout
        fields = ["title", "date", "location", "mood", "weight", "notes"]


class ExerciseForm(forms.ModelForm):
    notes = forms.CharField(required=False, widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        super(ExerciseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Add Exercise', css_class='btn btn-primary btn-block'))

    class Meta:
        model = Exercise
        fields = ["name", "notes"]



class SetFormSetHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(SetFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.template_pack = 'bootstrap3'
        self.layout = Layout(
            Div(
                Div(
                    Div(
                        'number',
                    ),
                    Div(
                        Div(
                            'weight', css_class='col-xs-6',
                        ),
                        Div(
                            'weight_measurement', css_class='col-xs-6', label="Measurement",
                        ),
                        css_class='row',
                    ),
                    Div(
                        Div(
                            'repetitions', css_class='col-xs-6',
                        ),
                        Div(
                            'set_type', css_class='col-xs-6',
                        ),
                        css_class='row',
                    ),
                    Div(
                        'notes', css_class='textarea',
                    ),
                ),
                css_class='box', style="margin-bottom: 1em"
            ),
        )
        self.render_required_fields = True
        self.add_input(Submit("submit", "Save", css_class="btn-lg btn-primary"))

class SetForm(forms.ModelForm):
    weight_measurement = forms.ChoiceField(label="Unit", choices=Set.WEIGHT_MEASUREMENT_CHOICES, initial=Set.POUNDS)
    notes = forms.CharField(required=False, widget=forms.Textarea())
    number = forms.IntegerField(label="Set Number", min_value=1)

    class Meta:
        model = Set
        fields = ["number", "weight", "weight_measurement", "repetitions", "set_type", "notes"]


SetFormSet = inlineformset_factory(Exercise, Set, form=SetForm, extra=0)
