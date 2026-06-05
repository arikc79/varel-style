from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, F, ExpressionWrapper, IntegerField, Count, Q
from .forms import CategoryAdminForm, ProductAdminForm
from .models import Category, Product, ProductImage, ProductSizeStock


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form          = CategoryAdminForm
    list_display  = ['name', 'order', 'product_count']
    list_editable = ['order']
    search_fields = ['name']
    fields        = ['name', 'order']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_product_count=Count('products', filter=Q(products__stock__gt=0)))

    def product_count(self, obj):
        return getattr(obj, '_product_count', 0)
    product_count.short_description = 'Товарів'


class SizeStockInline(admin.TabularInline):
    model   = ProductSizeStock
    extra   = 0
    fields  = ['size', 'quantity']
    ordering = ['size']


class ProductImageInline(admin.TabularInline):
    model            = ProductImage
    extra            = 0
    max_num          = 4
    can_delete       = True
    show_change_link = True
    fields           = ['image', 'order', 'preview']
    readonly_fields  = ['preview']

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:80px;width:80px;object-fit:cover;border-radius:6px;" />',
                obj.image.url,
            )
        return '—'
    preview.short_description = "Прев'ю"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form            = ProductAdminForm
    list_display    = ['id', 'main_photo', 'name', 'category', 'price', 'cost_price', 'old_price', 'stock_display', 'badge', 'revenue_display', 'cost_display', 'margin_display', 'created_at']
    list_filter     = ['category', 'badge']
    list_select_related = ['category']
    search_fields   = ['name', 'description']
    list_editable   = ['price', 'cost_price']
    readonly_fields = ['created_at', 'stock_display', 'revenue_display', 'cost_display', 'margin_display']
    inlines         = [SizeStockInline, ProductImageInline]
    fieldsets = (
        ('Основне',   {'fields': ('name', 'category', 'emoji', 'badge')}),
        ('Ціна',      {'fields': ('price', 'old_price', 'cost_price')}),
        ('Підрахунок',{'fields': ('stock_display', 'revenue_display', 'cost_display', 'margin_display')}),
        ('Опис',      {'fields': ('description', 'sizes', 'colors', 'details')}),
        ('Дати',      {'fields': ('created_at',)}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('images', 'size_stocks')

    def stock_display(self, obj):
        stocks = obj.size_stocks.all()
        if not stocks:
            return '—'
        return ', '.join(f'{s.size}: {s.quantity}' for s in stocks)
    stock_display.short_description = 'Залишки по розмірах'

    def main_photo(self, obj):
        images = obj.images.all()
        if images:
            return format_html('<img src="{}" style="height:48px;width:48px;object-fit:cover;border-radius:6px;" />', images[0].image.url)
        return '—'
    main_photo.short_description = 'Фото'

    def revenue_display(self, obj):
        total = obj.total_stock
        if not obj.price or not total:
            return '—'
        return f'{total * obj.price:,} ₴'.replace(',', ' ')
    revenue_display.short_description = 'Виручка (шт × ціна)'

    def cost_display(self, obj):
        total = obj.total_stock
        if not obj.cost_price or not total:
            return '—'
        return f'{total * obj.cost_price:,} ₴'.replace(',', ' ')
    cost_display.short_description = 'Собівартість (шт × закупка)'

    def margin_display(self, obj):
        if not obj.cost_price or not obj.price:
            return '—'
        margin = obj.price - obj.cost_price
        pct = round(margin / obj.price * 100)
        color = '#2ecc71' if margin >= 0 else '#e74c3c'
        return format_html('<span style="color:{}">{} ₴ ({}%)</span>', color, f'{margin:,}'.replace(',', ' '), pct)
    margin_display.short_description = 'Маржа (ціна − закупка)'

    def changelist_view(self, request, extra_context=None):
        from .models import ProductSizeStock
        totals_qs = ProductSizeStock.objects.aggregate(total_stock=Sum('quantity'))
        qs = self.get_queryset(request)
        rev  = sum((p.total_stock * p.price) for p in qs if p.price)
        cost = sum((p.total_stock * p.cost_price) for p in qs if p.cost_price)
        totals = {
            'total_stock':   totals_qs['total_stock'] or 0,
            'total_revenue': rev,
            'total_cost':    cost,
        }
        extra_context = extra_context or {}
        extra_context['totals'] = {
            'stock':   totals['total_stock'],
            'revenue': f"{totals['total_revenue']:,}".replace(',', ' ') + ' ₴',
            'cost':    f"{totals['total_cost']:,}".replace(',', ' ') + ' ₴',
        }
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display  = ['id', 'preview', 'product', 'order']
    list_filter   = ['product__category']
    list_select_related = ['product']
    search_fields = ['product__name']

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;width:60px;object-fit:cover;border-radius:6px;" />', obj.image.url)
        return '—'
    preview.short_description = "Прев'ю"
