from django.contrib import admin
from django.db.models import Sum, Count, Q, F, ExpressionWrapper, IntegerField
from django.db.models.functions import TruncMonth
from django.template.response import TemplateResponse
from django.utils import timezone
from .models import Customer, Order, OrderItem

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
            .annotate(line_total=F('price') * F('qty'))
            .values('name')
            .annotate(qty=Sum('qty'), revenue=Sum('line_total'))
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


def send_promo_email(modeladmin, request, queryset):
    import os, resend
    api_key = os.getenv('RESEND_API_KEY')
    if not api_key:
        modeladmin.message_user(request, '❌ RESEND_API_KEY не задано', level='error')
        return
    recipients = list(queryset.exclude(email='').values_list('email', flat=True))
    if not recipients:
        modeladmin.message_user(request, '⚠️ Немає клієнтів з email', level='warning')
        return
    resend.api_key = api_key
    sent = 0
    for email in recipients:
        try:
            resend.Emails.send({
                'from': 'VAREL Style <onboarding@resend.dev>',
                'to':   [email],
                'subject': '🎁 Акція від VAREL Style',
                'text': 'Привіт! У нас є спеціальна пропозиція для вас. Заходьте на сайт: https://varel-style.onrender.com',
            })
            sent += 1
        except Exception:
            pass
    modeladmin.message_user(request, f'✅ Відправлено {sent} з {len(recipients)} листів')

send_promo_email.short_description = '📧 Надіслати акцію на email'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display    = ['first_name', 'phone', 'email', 'total_orders', 'total_spent_display', 'last_order_at']
    search_fields   = ['phone', 'first_name', 'email']
    readonly_fields = ['phone', 'first_name', 'email', 'total_orders', 'total_spent', 'created_at', 'last_order_at']
    ordering        = ['-last_order_at']
    actions         = [send_promo_email]

    def has_add_permission(self, request):    return False
    def has_delete_permission(self, request, obj=None): return False

    @admin.display(description='Витрачено ₴', ordering='total_spent')
    def total_spent_display(self, obj):
        return f'{obj.total_spent} ₴'
