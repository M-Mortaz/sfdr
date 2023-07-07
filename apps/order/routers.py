from rest_framework import routers

from apps.order.views import OrderViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'orders', OrderViewSet, basename='orders')
