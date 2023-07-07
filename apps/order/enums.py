from django.db import models


class DelayResponseCodeEnum(models.IntegerChoices):
    SHIPMENT_TIME_UPDATED = 1
    REPORT_SUBMITTED = 2
    ALREADY_SUBMITTED = 3
