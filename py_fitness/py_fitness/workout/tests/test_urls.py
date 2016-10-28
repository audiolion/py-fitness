from django.core.urlresolvers import reverse, resolve
from django.utils import timezone

from test_plus.test import TestCase

from ..models import Exercise, Set, Workout

class TestWorkoutURLs(TestCase):
    """Test URL patterns for workout app."""

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
        self.today = timezone.now()
        self.year = self.today.strftime("%Y")
        self.month = self.today.strftime("%m")

    def test_workout_detail_reverse(self):
        self.assertEqual(
            reverse('wrk:workout_detail', kwargs={'year': self.year, 'month': self.month, 'pk': self.workout.pk}),
            '/workouts/{}/{}/{}/'.format(self.year, self.month, self.workout.pk)
        )

    def test_workout_detail_resolve(self):
        self.assertEqual(
            resolve('/workouts/2016/10/2/').view_name,
            'wrk:workout_detail'
        )

    def test_exercise_detail_reverse(self):
        self.assertEqual(
            reverse('wrk:exercise_detail', kwargs={'slug': self.exercise.slug}),
            '/workouts/exercises/{}/'.format(self.exercise.slug)
        )

    def test_exercise_detail_resolve(self):
        self.assertEqual(
            resolve('/workouts/exercises/some-exercise-slug/').view_name,
            'wrk:exercise_detail'
        )
