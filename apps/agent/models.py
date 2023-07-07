from django.contrib.auth import get_user_model
from django.db import models

from utils.fakers import fake_name

User = get_user_model()


class Agent(models.Model):
    name = models.CharField(max_length=100, default=fake_name)
