from django.db import models
from faker import Faker

fake = Faker()


class Agent(models.Model):
    name = models.CharField(max_length=100, default=fake.name)
