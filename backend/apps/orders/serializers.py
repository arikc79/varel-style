from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from .models import Customer, Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OrderItem
        fields = ['product_id', 'name', 'price', 'size', 'color', 'qty']

class OrderSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    email = serializers.EmailField(required=False, allow_blank=True, default='')
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
        OrderItem.objects.bulk_create([
            OrderItem(order=order, **item) for item in items_data
        ])
        self._sync_customer(order)
        return order

    def _sync_customer(self, order):
        customer, created = Customer.objects.get_or_create(
            phone=order.phone,
            defaults={'first_name': order.first_name, 'email': order.email or ''},
        )
        if not created:
            # оновлюємо email якщо тепер вказали
            if order.email and not customer.email:
                customer.email = order.email
        customer.total_orders += 1
        customer.total_spent  += order.total
        customer.last_order_at = timezone.now()
        customer.save()
        order.customer = customer
        order.save(update_fields=['customer'])
