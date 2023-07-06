from rest_framework import routers

from apps.user.views import UserAPIViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'', UserAPIViewSet, basename='user-info')
