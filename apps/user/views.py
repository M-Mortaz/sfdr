import logging

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from apps.user.serializers import UserSerializer

logger = logging.getLogger(__name__)
User = get_user_model()


class UserAPIViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
