from rest_framework import routers

from apps.agent.views import AgentViewSet

router_v1 = routers.DefaultRouter()  # NoQA
router_v1.register(r'agents', AgentViewSet, basename='agent')
