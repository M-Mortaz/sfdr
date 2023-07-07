from factory.django import DjangoModelFactory

from apps.vendor.models import Vendor
import factory


class VendorFactory(DjangoModelFactory):
    class Meta:
        model = Vendor

    name = factory.Faker("last_name")
