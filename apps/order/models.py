from django.db import models

from apps.order.exc import NotValidStateError
from utils.fakers import fake_name, fake_delivery_time


class Order(models.Model):
    name = models.CharField(max_length=100, default=fake_name)
    vendor = models.ForeignKey("vendor.Vendor", on_delete=models.SET_NULL, null=True, related_name="orders")
    deliver_at = models.DateTimeField(default=fake_delivery_time, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)


class DelayReportAction(models.IntegerChoices):
    SHIPPING_TIME_UPDATED = 1
    INSERTED_INTO_QUEUE = 2
    REJECTED = 3


class DelayReportState(models.IntegerChoices):
    NOT_NEED_TO_ACTION = 0
    WAITING_FOR_AGENT = 1
    ASSIGNED_TO_VENDOR = 2
    CHECKED = 3


class OrderDelayReportManager(models.Manager):
    def create(self, **kwargs):
        action = kwargs["action"]
        if action == DelayReportAction.INSERTED_INTO_QUEUE:
            kwargs["state"] = DelayReportState.WAITING_FOR_AGENT
        elif action in [DelayReportAction.SHIPPING_TIME_UPDATED, DelayReportAction.REJECTED]:
            kwargs["state"] = DelayReportState.NOT_NEED_TO_ACTION
        else:
            raise NotValidStateError
        return super().create(**kwargs)


class OrderDelayReport(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="delay_reports")
    action = models.PositiveSmallIntegerField(db_index=True, choices=DelayReportAction.choices)
    delay = models.PositiveIntegerField(default=0)
    vendor = models.ForeignKey("vendor.Vendor", on_delete=models.CASCADE, related_name="delays")
    agent = models.ForeignKey("agent.Agent", null=True, on_delete=models.SET_NULL)
    assigned_at = models.DateTimeField(null=True)
    state = models.PositiveSmallIntegerField(
        default=DelayReportState.NOT_NEED_TO_ACTION,
        choices=DelayReportState.choices,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = OrderDelayReportManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("agent", "state"),
                condition=models.Q(
                    state=DelayReportState.ASSIGNED_TO_VENDOR,
                    agent_id__isnull=False
                ),
                name="unique_assigned_delay_report_to_one_agent",
                violation_error_message="Agent already has an assigned delay report!")
        ]
