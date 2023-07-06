from django.db import models


class TripState(models.IntegerChoices):
    ASSIGNED = 1
    AT_VENDOR = 2
    PICKED = 3
    DELIVERED = 4


class Trip(models.Model):
    status = models.SmallIntegerField(choices=TripState.choices, db_index=True)
