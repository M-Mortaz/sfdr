from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.vendor.models import Vendor
from apps.vendor.serializers import VendorSerializer


class VendorViewSet(viewsets.ModelViewSet):
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()
    permission_classes = [AllowAny]
