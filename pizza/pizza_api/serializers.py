from django.db.models.query import InstanceCheckMeta
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Order, Pizza, Customer, CustomerAddress


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'email_address')
        read_only_fields = ('id',)

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email = validated_data.get('email_address', instance.email_address)
        instance.save()
        return instance


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = '__all__'
        read_only_fields = ('id', 'ctime', 'mtime')

    #Field-level Validation
    def validate_address(self, value):
        if value != value.capitalize():
            raise serializers.ValidationError("Address not in capitalize format")
        return value

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['customer'] = instance.customer.full_name()
        return response

    def create(self, validated_data):
        customer_id = self.context['view'].kwargs['customer_id']
        return CustomerAddress.objects.create(customer_id=customer_id, **validated_data)

    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ('id', 'name')
        read_only_fields = ('id',)

    def create(self, validated_data):
        return Pizza.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.pizza_name)
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','customer', 'customer_address', 'pizza', 'size', 'order_status')
        read_only_fields = ('id',)

    # Object-level Validation
    def validate(self, data):
        customer_address = data['customer_address']
        customer_id = int(self.context['view'].kwargs['customer_id'])

        if customer_address.customer_id != customer_id:
            raise ValidationError(detail='Address not Found!')
        return data

    def to_representation(self, instance):
        response = super().to_representation(instance)

        del response['customer_address']
        del response['size']

        response['customer'] = instance.customer.full_name()
        response['address'] = CustomerAddressSerializer(instance.customer_address).data

        response['pizza'] = PizzaSerializer(instance.pizza).data
        response['pizza']['size'] = instance.size
        return response

    def create(self, validated_data):
        customer_id = self.context['view'].kwargs['customer_id']
        return Order.objects.create(customer_id=customer_id, **validated_data)

    def update(self, instance, validated_data):
        instance.customer_address = validated_data.get('customer_address', instance.customer_address)
        instance.pizza = validated_data.get('pizza', instance.pizza)
        instance.size = validated_data.get('size', instance.size)
        instance.order_status = validated_data.get('order_status', instance.order_status)
        instance.save()
        return instance
