from django.db import transaction
from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OrderItem
        fields = ['product_id', 'name', 'price', 'size', 'color', 'qty']

class OrderSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'first_name', 'last_name', 'phone', 'email',
            'delivery_type', 'city', 'branch', 'payment_type',
            'total', 'status', 'items', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']

    def validate_phone(self, value):
        # Accept user-friendly phone formats and normalize to +XXXXXXXXXX.
        raw = str(value or '').strip()
        digits = ''.join(ch for ch in raw if ch.isdigit())
        if len(digits) < 10 or len(digits) > 15:
            raise serializers.ValidationError('Телефон має містити від 10 до 15 цифр.')
        return f'+{digits}'

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        order_items = [
            OrderItem(order=order, **item) for item in items_data
        ]
        OrderItem.objects.bulk_create(order_items)
        return order
