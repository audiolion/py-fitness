from django.utils import timezone
from test_plus.test import TestCase
from ..models import Workout, Exercise, Set

import datetime


class TestSet(TestCase):

    def setUp(self):
        name = 'Reverse Grip Dumbbell Lateral Raises'
        self.user = self.make_user(username='test_oaf1163')
        self.user.name = 'Sun Tzu'
        self.workout = Workout.objects.create(
            author=self.user,
            date=timezone.now()
        )
        self.exercise = Exercise.objects.create(
            name=name,
        )
        self.set = Set.objects.create(
            number=1,
            weight=100.50,
            repetitions=12,
            exercise=self.exercise
        )

    def test__str__(self):
        self.assertEqual(
            self.set.__str__(),
            'Set 1 - Regular - 12 reps at 100.5 lbs'
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.set.get_absolute_url(),
            '/api/exercises/' + self.set.exercise.slug + '/' + 'sets/' + str(self.set.pk) + '/'
        )


class TestExercise(TestCase):

    def setUp(self):
        name = 'Reverse Grip Dumbbell Lateral Raises'
        self.user = self.make_user(username='test_oaf1163')
        self.user.name = 'Sun Tzu'
        self.workout = Workout.objects.create(
            author=self.user,
            date=timezone.now()
        )
        self.exercise = Exercise.objects.create(
            name=name,
        )

    def test__str__(self):
        exercise_name = 'Reverse Grip Dumbbell Lateral Raises'
        self.assertEqual(
            self.exercise.__str__(),
            exercise_name
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.exercise.get_absolute_url(),
            '/api/exercises/' + self.exercise.slug + '/'
        )


class TestWorkout(TestCase):

    def setUp(self):
        self.user = self.make_user(username='test_oaf1163')
        self.user.name = 'Jace Beleren'
        self.workout = Workout.objects.create(
            author=self.user,
            date=timezone.now()
        )

    def test__str__(self):
        self.assertEqual(
            self.workout.__str__(),
            'Jace Beleren\'s workout on {}'.format(timezone.now().strftime("%m-%d-%Y"))
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.workout.get_absolute_url(),
            '/api/workouts/{}/{}/{}/'.format(
                self.workout.date.strftime("%Y"),
                self.workout.date.strftime("%m"),
                self.workout.pk
            )
        )
