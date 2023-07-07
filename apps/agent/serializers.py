from rest_framework import serializers

from apps.agent.models import Agent


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ("name", "id")
