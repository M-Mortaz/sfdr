from django.db import models


class TripState(models.IntegerChoices):
    ASSIGNED = 1
    AT_VENDOR = 2
    PICKED = 3
    DELIVERED = 4


class Trip(models.Model):
    status = models.PositiveSmallIntegerField(choices=TripState.choices, db_index=True)
    order = models.OneToOneField("order.Order", on_delete=models.CASCADE, related_name="trip")
