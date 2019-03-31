from django.contrib.auth.models import User
from .models import Check
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class CheckSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Check
        fields = ('id', 'venue', 'timestamp', 'location_id', 'location', 'slot_time', 'open_seats', 'taken_seats', 'is_full')

class LocationListSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=255)