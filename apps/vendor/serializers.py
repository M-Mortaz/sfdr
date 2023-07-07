from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.vendor.models import Vendor

User = get_user_model()


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ("name", "id")
