from rest_framework import routers

from apps.vendor.views import VendorViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'vendors', VendorViewSet, basename='vendor')
