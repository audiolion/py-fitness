from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions

from py_fitness.users.models import User

from .forms import WorkoutForm
from .models import Workout, Exercise, Set
from .permissions import WorkoutIsOwnerOrReadOnly, ExerciseIsOwnerOrReadOnly, SetIsOwnerOrReadOnly, UserIsOwnerOrReadOnly
from .serializers import ExerciseSerializer, SetSerializer, UserSerializer, WorkoutSerializer


class ApiUserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, UserIsOwnerOrReadOnly)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ApiUserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, UserIsOwnerOrReadOnly)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ApiWorkoutList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, WorkoutIsOwnerOrReadOnly)
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ApiWorkoutDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, WorkoutIsOwnerOrReadOnly)
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer


class ApiExerciseList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, ExerciseIsOwnerOrReadOnly)

    def get(self, request, format=None):
        exercises = Exercise.objects.all()
        serializer = ExerciseSerializer(exercises, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ExerciseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiExerciseDetail(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, ExerciseIsOwnerOrReadOnly)

    def get_object(self, slug):

        try:
            obj = Exercise.objects.get(slug=slug)
            self.check_object_permissions(self.request, obj)
            return obj
        except Exercise.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        exercise = self.get_object(slug)
        serializer = ExerciseSerializer(exercise)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        exercise = self.get_object(slug)
        serializer = ExerciseSerializer(exercise, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        exercise = self.get_object(slug)
        exercise.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApiSetList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, SetIsOwnerOrReadOnly)
    queryset = Set.objects.all()
    serializer_class = SetSerializer


class ApiSetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, SetIsOwnerOrReadOnly)
    queryset = Set.objects.all()
    serializer_class = SetSerializer
