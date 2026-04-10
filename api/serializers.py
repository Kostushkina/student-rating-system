from rest_framework import serializers
from .models import Student, Event, Request


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'