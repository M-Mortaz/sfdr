from rest_framework import serializers

from apps.order.models import OrderDelayReport, Order


class OrderDelayReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDelayReport
        fields = (
            "id",
            "order",
            "action",
            "delay",
            "vendor",
            "agent",
            "assigned_at",
            "state",
            "created_at"
        )
        read_only_fields = (
            "order",
            "action",
            "delay",
            "vendor",
            "agent",
            "assigned_at",
            "state",
            "created_at"
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "name", "vendor", "deliver_at", "created_at")
        read_only_fields = ("created_at",)


class ReportOrderResponseSerializer(serializers.Serializer):
    order = OrderSerializer(many=False)
    report = OrderDelayReportSerializer(many=False)
    code = serializers.IntegerField()
    message = serializers.CharField()

    def create(self, validated_data):
        raise NotImplemented  # NoQA

    def update(self, instance, validated_data):
        raise NotImplemented  # NoQA
