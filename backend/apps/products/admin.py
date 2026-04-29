from django.contrib import admin
from django.utils.html import format_html
from .forms import CategoryAdminForm, ProductAdminForm
from .models import Category, Product, ProductImage
from django.db.models import Count, Q

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form          = CategoryAdminForm
    list_display  = ['emoji', 'name', 'order', 'product_count']
    list_editable = ['order']
    search_fields = ['name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Анотуємо кількість прямо в запиті
        return qs.annotate(
            _product_count=Count('products', filter=Q(products__in_stock=True))
        )

    def product_count(self, obj):
        # Беремо вже пораховане значення
        return getattr(obj, '_product_count', 0)

    product_count.short_description = 'Товарів'


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
                '<img src="{}" style="height:80px;width:80px;object-fit:cover;border-radius:6px;border:1px solid #333;" />',
                obj.image.url,
            )
        return '—'
    preview.short_description = "Прев'ю"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form            = ProductAdminForm
    list_display    = ['id', 'main_photo', 'name', 'category', 'price', 'old_price', 'badge', 'in_stock', 'created_at']
    list_filter     = ['category', 'in_stock', 'badge']
    list_select_related = ['category']
    search_fields   = ['name', 'description']
    list_editable   = ['price', 'in_stock']
    readonly_fields = ['created_at']
    inlines         = [ProductImageInline]
    fieldsets = (
        ('Основне', {'fields': ('name', 'category', 'emoji', 'badge', 'in_stock')}),
        ('Ціна',    {'fields': ('price', 'old_price')}),
        ('Опис',    {'fields': ('description', 'sizes', 'colors', 'details')}),
        ('Дати',    {'fields': ('created_at',)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('images')

    def main_photo(self, obj):
        images = obj.images.all()
        if images:
            first = images[0]
            return format_html(
                '<img src="{}" style="height:48px;width:48px;object-fit:cover;border-radius:6px;" />',
                first.image.url,
            )
        return format_html('<span style="font-size:24px">{}</span>', obj.emoji)
    main_photo.short_description = 'Фото'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display  = ['id', 'preview', 'product', 'order']
    list_filter   = ['product__category']
    list_select_related = ['product']
    search_fields = ['product__name']

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px;width:60px;object-fit:cover;border-radius:6px;border:1px solid #333;" />',
                obj.image.url,
            )
        return '—'
    preview.short_description = "Прев'ю"
