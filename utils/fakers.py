import random
from datetime import timedelta

from faker import Faker
from django.utils import timezone
fake = Faker()


def fake_name() -> str:
    return fake.name()


def fake_delivery_time() -> int:
    return timezone.now() + timedelta(minutes=random.randint(0, 10))
