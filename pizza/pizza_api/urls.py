from rest_framework import routers
from .views import OrderViewSet, CustomerViewSet, PizzaViewSet, CustomerAddressViewSet

from django.urls import path, include

router = routers.SimpleRouter()
router.register('customers/(?P<customer_id>\d+)/orders', OrderViewSet, basename='customer_orders')
router.register('customers/(?P<customer_id>\d+)/addresses', CustomerAddressViewSet, basename='customer_addresses')
router.register('customers', CustomerViewSet, basename='customers')
router.register('pizzas', PizzaViewSet, basename='pizzas')

urlpatterns = [
    path('', include(router.urls)),
]
