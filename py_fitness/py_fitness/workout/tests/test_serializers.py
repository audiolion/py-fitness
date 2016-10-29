from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from test_plus.test import TestCase

from ..models import Exercise, Set, Workout


class ExerciseTests(APITestCase, TestCase):
    def setUp(self):
        self.user = self.make_user(username='test_oaf1163', password='mystikal6')
        self.user2 = self.make_user(username='brolaf', password='bromacia!')
        self.client = APIClient()
        self.client.login(username='test_oaf1163', password='mystikal6')
        self.workout = Workout.objects.create(author=self.user, date=timezone.now())
        self.exercise = Exercise.objects.create(name='bench press', workout=self.workout)
        self.set = Set.objects.create(number=1, weight=35.2, repetitions=10, exercise=self.exercise)

    def test_create_exercise(self):
        url = reverse('api:exercise_list')
        data = {
            'id': 20,
            'name': 'Reverse Grip Dumbbell Flies',
            'notes': '',
            'sets': [{
                'number': 1,
                'weight': 35,
                'weight_measurement': Set.POUNDS,
                'repetitions': 10,
                'set_type': Set.NORMAL,
            },
            {
                'number': 2,
                'weight': 45,
                'weight_measurement': Set.POUNDS,
                'repetitions': 10,
                'set_type': Set.NORMAL
            },
            {
                'number': 3,
                'weight': 55,
                'weight_measurement': Set.POUNDS,
                'repetitions': 8,
                'set_type': Set.NORMAL
            },
            {
                'number': 3,
                'weight': 55,
                'weight_measurement': Set.POUNDS,
                'repetitions': 3,
                'set_type': Set.NEGATIVE
            }]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exercise.objects.count(), 2)
        self.assertEqual(Set.objects.count(), 5)
        self.assertEqual(Exercise.objects.get(id=6).name, 'Reverse Grip Dumbbell Flies')

    def test_update_exercise(self):
        url = reverse('api:exercise_detail', kwargs={'slug': self.exercise.slug})

        data = {
            'name': 'Close-grip Bench Press'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Exercise.objects.get(pk=self.exercise.pk).name, 'Close-grip Bench Press')

    def test_update_not_allowed_exercise(self):
        url = reverse('api:exercise_detail', kwargs={'slug': self.exercise.slug})

        data = {
            'name': 'Close-grip Bro Press'
        }
        self.client.logout()
        self.client.login(username='brolaf', password='bromacia!')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Exercise.objects.get(pk=self.exercise.pk).name, 'bench press')

    def test_delete_exercise(self):
        url = reverse('api:exercise_detail', kwargs={'slug': self.exercise.slug})

        data = {
            'pk': self.exercise.pk
        }
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Exercise.objects.count(), 0)
        self.assertEqual(Set.objects.count(), 0)


class SetTests(APITestCase, TestCase):
    def setUp(self):
        self.user = self.make_user(username='test_oaf1163', password='mystikal6')
        self.client = APIClient()
        self.client.login(username='test_oaf1163', password='mystikal6')
        self.workout = Workout.objects.create(author=self.user, date=timezone.now())
        self.exercise = Exercise.objects.create(name='Benchers dress', workout=self.workout)
        self.set = Set.objects.create(number=2, weight=55, repetitions=8, exercise=self.exercise)

    def test_create_set(self):
        url = reverse('api:set_list', kwargs={'slug': self.exercise.slug})

        data = {
            'number': 1,
            'weight': 35,
            'weight_measurement': Set.POUNDS,
            'repetitions': 10,
            'set_type': Set.NORMAL,
            'exercise': self.exercise.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exercise.objects.count(), 1)
        self.assertEqual(Set.objects.count(), 2)
        self.assertEqual(Set.objects.filter(exercise=self.exercise.pk)[0].weight, 35)

    def test_update_set(self):
        url = reverse('api:set_detail', kwargs={'slug': self.exercise.slug, 'pk': self.set.pk})

        data = {
            'number': 1,
            'weight': 55,
            'weight_measurement': Set.POUNDS,
            'repetitions': 10,
            'set_type': Set.NORMAL,
            'exercise': self.exercise.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Set.objects.filter(exercise=self.exercise.pk)[0].number, 1)
        self.assertEqual(Set.objects.filter(exercise=self.exercise.pk)[0].repetitions, 10)

    def test_delete_set(self):
        url = reverse('api:set_detail', kwargs={'pk': self.set.pk, 'slug': self.exercise.slug})

        data = {
            'pk': self.set.pk
        }
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Exercise.objects.count(), 1)
        self.assertEqual(Set.objects.count(), 0)
