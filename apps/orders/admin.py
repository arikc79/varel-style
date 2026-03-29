from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model  = OrderItem
    extra  = 0
    fields = ['name', 'size', 'qty', 'price']
    readonly_fields = ['name', 'size', 'qty', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display    = ['id', 'first_name', 'last_name', 'phone', 'total', 'delivery_type', 'payment_type', 'status', 'created_at']
    list_filter     = ['status', 'delivery_type', 'payment_type']
    search_fields   = ['first_name', 'last_name', 'phone', 'email']
    list_editable   = ['status']
    readonly_fields = ['created_at']
    inlines         = [OrderItemInline]
    fieldsets = (
        ('Клієнт',    {'fields': ('first_name', 'last_name', 'phone', 'email')}),
        ('Доставка',  {'fields': ('delivery_type', 'city', 'branch')}),
        ('Оплата',    {'fields': ('payment_type', 'total')}),
        ('Статус',    {'fields': ('status', 'created_at')}),
    )
