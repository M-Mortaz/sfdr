from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.agent.models import Agent
from apps.agent.serializers import AgentSerializer


class AgentViewSet(viewsets.ModelViewSet):
    serializer_class = AgentSerializer
    queryset = Agent.objects.all()
    permission_classes = [AllowAny]
