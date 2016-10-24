from django.core.urlresolvers import reverse
from django.db import models

from py_fitness.core.behaviors import Authorable, Editorable, Publishable, Timestampable


class Exercise(models.Model):
    pass


class Workout(Authorable, Editorable, Timestampable, Publishable, models.Model):
    date = models.DateTimeField()
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    duration = models.DurationField(null=True, blank=True)
    mood = models.CharField(max_length=254, blank=True)
    location = models.CharField(max_length=254, blank=True)
    notes = models.TextField(blank=True)
    exercises = models.ForeignKey(Exercise, blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return "{}'s workout on {}".format(self.author.name, self.date.strftime("%m-%d-%Y"))

    def get_absolute_url(self):
        return reverse("wrk:workout_detail", kwargs={"pk": self.pk,
                                                     "year": self.date.strftime("%Y"),
                                                     "month": self.date.strftime("%m")})