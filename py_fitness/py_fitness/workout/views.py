from django.http import Http404
from django.shortcuts import render
from django.views.generic import View, DetailView

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics

from .models import Workout, Exercise, Set
from .serializers import ExerciseSerializer, SetSerializer

class WorkoutDetail(APIView):
    model = Workout


class ExerciseDetail(DetailView):
    model = Exercise


class ApiExerciseList(APIView):

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


class ApiExerciseDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    def get_object(self, slug):
        try:
            return Exercise.objects.get(slug=slug)
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
    queryset = Set.objects.all()
    serializer_class = SetSerializer


class ApiSetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Set.objects.all()
    serializer_class = SetSerializer
