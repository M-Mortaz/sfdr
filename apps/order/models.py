from django.db import models

from faker import Faker

fake = Faker()


class Order(models.Model):
    name = models.CharField(max_length=100, default=fake.name)
    vendor = models.ForeignKey("vendor.Vendor", on_delete=models.SET_NULL, null=True, related_name="orders")
    delivery_time = models.PositiveBigIntegerField(help_text="Preparation and shipping time")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderDelayReport(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="delay_reports")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
