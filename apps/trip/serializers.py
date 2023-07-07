from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.trip.models import Trip

User = get_user_model()


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ("status", "order", "id")
