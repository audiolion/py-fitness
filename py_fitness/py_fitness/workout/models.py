from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from hashids import Hashids

from py_fitness.core.behaviors import Authorable, Editorable, Publishable, Timestampable


class Workout(Authorable, Timestampable, Publishable, models.Model):
    title = models.CharField(max_length=254, blank=True)
    date = models.DateTimeField()
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    duration = models.DurationField(null=True, blank=True)
    mood = models.CharField(max_length=254, blank=True)
    location = models.CharField(max_length=254, blank=True)
    notes = models.TextField(blank=True)
    finished = models.BooleanField(default=False, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return "{}'s workout on {}".format(self.author.name, self.date.strftime("%m-%d-%Y"))

    def get_absolute_url(self):
        return reverse("workout:workout_detail", kwargs={"pk": self.pk,
                                                     "year": self.date.strftime("%Y"),
                                                     "month": self.date.strftime("%m")})


class Exercise(models.Model):
    name = models.CharField(max_length=80, default='')
    slug = models.SlugField(unique=True, max_length=140)
    notes = models.CharField(max_length=254, blank=True)
    workout = models.ForeignKey(Workout, blank=True, null=True, related_name='exercises')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def _slugify(self, code, name):
        hashids = Hashids(
            min_length=8,
            salt=name + timezone.now().time().isoformat()
        )
        return slugify(name) + "-" + hashids.encode(int(code))

    def save(self, *args, **kwargs):
        if not self.id:
            code = sum([ord(c) for c in self.name])
            self.slug = self._slugify(code, self.name)
        super(Exercise, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("api:exercise_detail", kwargs={"slug": self.slug})


class Set(models.Model):
    DROP = 'd'
    NEGATIVE = 'n'
    POSITIVE = 'p'
    SUPER = 's'
    NORMAL = 'r'

    TYPE_CHOICES = (
        (DROP, 'Drop'),
        (NEGATIVE, 'Negative'),
        (POSITIVE, 'Positive'),
        (SUPER, 'Super'),
        (NORMAL, 'Regular'),
    )

    KILOGRAMS = 'k'
    POUNDS = 'l'

    WEIGHT_MEASUREMENT_CHOICES = (
        (KILOGRAMS, 'kg'),
        (POUNDS, 'lbs'),
    )

    number = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=8, decimal_places=2)
    weight_measurement = models.CharField(
        max_length=1,
        choices=WEIGHT_MEASUREMENT_CHOICES,
        default=POUNDS
    )
    repetitions = models.PositiveIntegerField()
    set_type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        default=NORMAL
    )
    notes = models.CharField(max_length=254, blank=True)
    exercise = models.ForeignKey(Exercise, related_name='sets')

    class Meta:
        ordering = ('number',)

    def __str__(self):
        return "Set {} - {} - {} reps at {} {}".format(
            self.number, self.get_set_type_display(), self.repetitions,
            self.weight, self.get_weight_measurement_display())

    def get_absolute_url(self):
        return reverse("api:set_detail", kwargs={"slug": self.exercise.slug, "pk": self.pk})
