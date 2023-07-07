from factory.django import DjangoModelFactory

from apps.order.models import Order
import factory

from apps.vendor.factories import VendorFactory


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    vendor = factory.SubFactory(VendorFactory)
