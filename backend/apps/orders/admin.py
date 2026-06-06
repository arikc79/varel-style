from django.contrib import admin
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from django.template.response import TemplateResponse
from django.utils import timezone
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model  = OrderItem
    extra  = 0
    fields = ['product', 'name', 'size', 'color', 'qty', 'price']
    readonly_fields = ['product', 'name', 'size', 'color', 'qty', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display    = ['id', 'first_name', 'last_name', 'phone', 'total', 'delivery_type', 'payment_type', 'status', 'created_at']
    list_filter     = ['status', 'delivery_type', 'payment_type']
    search_fields   = ['=id','first_name', 'last_name', 'phone', 'email']
    list_editable   = ['status']
    readonly_fields = ['first_name', 'last_name', 'phone', 'email', 'total', 'created_at']
    inlines         = [OrderItemInline]
    fieldsets = (
        ('Клієнт',    {'fields': ('first_name', 'last_name', 'phone', 'email')}),
        ('Доставка',  {'fields': ('delivery_type', 'city', 'branch')}),
        ('Оплата',    {'fields': ('payment_type', 'total')}),
        ('Статус',    {'fields': ('status', 'created_at')}),
    )


class SalesDashboard(Order):
    class Meta:
        proxy = True
        verbose_name        = 'Статистика продажів'
        verbose_name_plural = '📊 Статистика продажів'


@admin.register(SalesDashboard)
class SalesDashboardAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):    return False
    def has_delete_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None): return False

    def changelist_view(self, request, extra_context=None):
        now = timezone.now()

        all_orders      = Order.objects.all()
        done_orders     = all_orders.filter(status='done')
        new_orders      = all_orders.filter(status='new')
        processing      = all_orders.filter(status='processing')

        total_revenue   = done_orders.aggregate(s=Sum('total'))['s'] or 0
        total_done      = done_orders.count()
        total_orders    = all_orders.count()

        # Виручка по місяцях (останні 6)
        six_months_ago = now - timezone.timedelta(days=180)
        monthly = (
            done_orders
            .filter(created_at__gte=six_months_ago)
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(revenue=Sum('total'), count=Count('id'))
            .order_by('month')
        )

        # Топ-5 товарів
        from apps.orders.models import OrderItem
        top_products = (
            OrderItem.objects
            .filter(order__status='done')
            .values('name')
            .annotate(qty=Sum('qty'), revenue=Sum('total'))
            .order_by('-qty')[:5]
        )

        context = {
            **self.admin_site.each_context(request),
            'title': 'Статистика продажів',
            'total_revenue':  total_revenue,
            'total_done':     total_done,
            'total_orders':   total_orders,
            'new_orders':     new_orders.count(),
            'processing':     processing.count(),
            'monthly':        monthly,
            'top_products':   top_products,
        }
        return TemplateResponse(request, 'admin/sales_dashboard.html', context)
