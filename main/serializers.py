from django.contrib.auth import authenticate
from django.forms import ValidationError
from .models import User
from rest_framework import serializers


from rest_framework import serializers
from .models import User, Mentor, Mentee, Service, Availability, SessionRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = '__all__'

class MenteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentee
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'

class SessionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionRequest
        fields = '__all__'