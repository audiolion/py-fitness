from django.utils import timezone
from test_plus.test import TestCase
from ..models import Workout

import datetime


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
            'Jace Beleren\'s workout on {}'.format(datetime.datetime.now().strftime("%m-%d-%Y"))  # This is the default username for self.make_user()
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.workout.get_absolute_url(),
            '/workouts/{}/{}/{}/'.format(self.workout.date.strftime("%Y"), self.workout.date.strftime("%m"), self.workout.pk)
        )