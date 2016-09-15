from __future__ import unicode_literals

from django.db import models

from core.behaviors import Authorable, Editorable, Permalinkable, Timestampable
from core.querysets import AuthorableQuerySet

from decimal import Decimal


class Repetition(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=10, unique=True)
    half = models.BooleanField(default=False, help_text="Half-rep, only went through half of the range of motion, usually occurs when muscle failure isn't reached for the bottom half of range of motion.")
    negative = models.BooleanField(default=False, help_text="Negative rep, started at top of positive range of motion, typically formed at the end of a set for absolute muscle failure.")
    positive = models.BooleanField(default=False, help_text="Positive rep, did not resist weight on the negative portion of rep, typically done in plyometric workouts.")

    def __str__(self):
        return self.name


class ExerciseSet(models.Model):
    set_number = models.IntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=8, decimal_places=3, default=Decimal('0.000'))
    repititions = models.ForeignKey(Repetition)

    def __str__(self):
        return "set " + str(self.set_number)


class Exercise(models.Model):
    name = models.CharField(max_length=254)
    exercise_set = models.ForeignKey(ExerciseSet)
    notes = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Workout(Authorable, Editorable, Timestampable, Permalinkable):
    exercises = models.ForeignKey(Exercise)
    objects = models.Manager
    authored = AuthorableQuerySet.as_manager()

    def __str__(self):
        return self.created.strftime("%Y-%m-%d-%I-%M-%p")