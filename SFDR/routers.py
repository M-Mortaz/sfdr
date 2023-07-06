from rest_framework import routers

from apps.agent.routers import router_v1 as agent_router_v1
from apps.order.routers import router_v1 as order_router_v1
from apps.user.routers import router_v1 as user_router_v1
from apps.vendor.routers import router_v1 as vendor_router_v1

app_router_v1 = routers.DefaultRouter()
app_router_v1.registry.extend(user_router_v1.registry)
app_router_v1.registry.extend(order_router_v1.registry)
app_router_v1.registry.extend(vendor_router_v1.registry)
app_router_v1.registry.extend(agent_router_v1.registry)
