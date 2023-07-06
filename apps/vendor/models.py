from django.db import models

from utils.fakers import fake_name


class Vendor(models.Model):
    name = models.CharField(max_length=100, default=fake_name)
