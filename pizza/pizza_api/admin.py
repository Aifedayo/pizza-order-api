from django.contrib import admin
from .models import Pizza, Order, CustomerAddress, Customer


admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Pizza)
admin.site.register(CustomerAddress)
