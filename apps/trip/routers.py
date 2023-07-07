from rest_framework import routers

from apps.trip.views import TripViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'trips', TripViewSet, basename='trip')
