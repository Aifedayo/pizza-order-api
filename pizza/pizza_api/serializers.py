from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Order, Pizza, Customer, CustomerAddress


class CustomerSerilizer(serializers.ModelSerilizer):
    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name')
        read_only_fields = ('id',)

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):