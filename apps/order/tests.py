from datetime import timedelta

from django.test import TestCase
from apps.order.models import Order
from freezegun import freeze_time

from apps.vendor.factories import VendorFactory
from django.utils import timezone
from rest_framework.test import APIClient

from apps.vendor.models import Vendor


class CreateOrderTest(TestCase):
    base_api = "/api/v1"
    api_client = APIClient()
    vendor: Vendor = None

    @classmethod
    def setUpTestData(cls):
        cls.vendor = VendorFactory.create(name="test vendor")

    @freeze_time("2012-01-14 12:00:01")
    def test_create_order_logic(self):
        deliver_at = timezone.now() + timedelta(minutes=30)
        order = Order.objects.create(name="test order", vendor=self.vendor, deliver_at=deliver_at)
        self.assertEqual(order.deliver_at, deliver_at)
        self.assertEqual(order.name, "test order")
        self.assertEqual(order.created_at, timezone.now())
        self.assertEqual(order.vendor_id, self.vendor.id)
        self.assertEqual(Order.objects.count(), 1)

    @freeze_time("2012-01-14 12:00:01")
    def test_create_order_api(self):
        order_api = f"{self.base_api}/orders/"
        deliver_at = timezone.now() + timedelta(minutes=30)
        data = {"name": "new order", "vendor": self.vendor.id, "deliver_at": deliver_at, }
        response = self.api_client.post(path=order_api, data=data, format="json")
        self.assertEqual(
            response.status_code,
            201,
            msg=f"Order api creation return status code {response.status_code}"
        )
        response_dict = response.json()
        order_id = response_dict.pop("id")
        expected = {
            "name": "new order",
            "vendor": 1,
            "deliver_at": "2012-01-14T12:30:01Z",
            "created_at": "2012-01-14T12:00:01Z"
        }
        self.assertDictEqual(expected, response_dict)
        self.assertEqual(Order.objects.filter(id=order_id).count(), 1)
