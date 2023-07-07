from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.trip.models import Trip
from apps.trip.serializers import TripSerializer


class TripViewSet(viewsets.ModelViewSet):
    serializer_class = TripSerializer
    queryset = Trip.objects.all()
    permission_classes = [AllowAny]
