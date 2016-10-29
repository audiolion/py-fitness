from rest_framework import serializers

from py_fitness.users.models import User

from .models import Exercise, Set, Workout


class SetSerializer(serializers.ModelSerializer):

     class Meta:
        model = Set
        fields = ('number', 'weight', 'weight_measurement', 'repetitions', 'set_type', 'notes', 'exercise')


class NestedSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Set
        fields = ('number', 'weight', 'weight_measurement', 'repetitions', 'set_type', 'notes')


class ExerciseSerializer(serializers.ModelSerializer):
    sets = NestedSetSerializer(many=True)

    class Meta:
        model = Exercise
        fields = ('name', 'sets', 'notes')

    def create(self, validated_data):
        sets_data = validated_data.pop('sets')
        exercise = Exercise.objects.create(**validated_data)
        for set_data in sets_data:
            Set.objects.create(exercise=exercise, **set_data)
        return exercise


class WorkoutSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Workout
        fields = ('author','date','weight','duration','location','mood','notes','publish_date')


class UserSerializer(serializers.ModelSerializer):
    workouts = serializers.PrimaryKeyRelatedField(many=True, queryset=Workout.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'workouts')
