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
            reverse('api:workout_detail', kwargs={'year': self.year, 'month': self.month, 'pk': self.workout.pk}),
            '/api/workouts/{}/{}/{}/'.format(self.year, self.month, self.workout.pk)
        )

    def test_workout_detail_resolve(self):
        self.assertEqual(
            resolve('/api/workouts/2016/10/2/').view_name,
            'api:workout_detail'
        )

    def test_exercise_detail_reverse(self):
        self.assertEqual(
            reverse('api:exercise_detail', kwargs={'slug': self.exercise.slug}),
            '/api/exercises/{}/'.format(self.exercise.slug)
        )

    def test_exercise_detail_resolve(self):
        self.assertEqual(
            resolve('/api/exercises/some-exercise-slug/').view_name,
            'api:exercise_detail'
        )
