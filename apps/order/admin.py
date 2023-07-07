from django.contrib import admin

from apps.order.models import Order, OrderDelayReport


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderDelayReport)
class OrderDelayReportAdmin(admin.ModelAdmin):
    pass
