from django.db import models
from django.core.exceptions import ValidationError


class Category(models.Model):
    name  = models.CharField(max_length=100, unique=True, verbose_name='Назва')
    emoji = models.CharField(max_length=10, default='👔', verbose_name='Emoji')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering            = ['order', 'name']
        verbose_name        = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return f'{self.emoji} {self.name}'


class Product(models.Model):
    category    = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='products',
        verbose_name='Категорія',
    )
    name        = models.CharField(max_length=255, verbose_name='Назва')
    price       = models.PositiveIntegerField(verbose_name='Ціна')
    old_price   = models.PositiveIntegerField(null=True, blank=True, verbose_name='Стара ціна')
    description = models.TextField(verbose_name='Опис')
    emoji       = models.CharField(max_length=10, default='👔', verbose_name='Emoji (fallback без фото)')
    sizes       = models.JSONField(default=list, verbose_name='Розміри')
    details     = models.JSONField(default=dict, blank=True,
                                   help_text='{"Склад":"...", "Країна":"...", "Колір":"..."}',
                                   verbose_name='Деталі')
    badge       = models.CharField(max_length=50, blank=True, verbose_name='Бейдж')
    in_stock    = models.BooleanField(default=True, verbose_name='В наявності')
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='Дата додавання')

    class Meta:
        ordering            = ['-created_at']
        verbose_name        = 'Товар'
        verbose_name_plural = 'Товари'

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='images', verbose_name='Товар',
    )
    image = models.ImageField(upload_to='products/', verbose_name='Фото')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок (0 = головне)')

    class Meta:
        ordering            = ['order']
        verbose_name        = 'Фото товару'
        verbose_name_plural = 'Фото товарів'

    def clean(self):
        # Inline у адмінці може валідовувати фото до збереження Product.
        # У такому випадку self.product ще без pk і related filter викликає ValueError.
        if not self.product_id:
            return

        qs = ProductImage.objects.filter(product_id=self.product_id)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.count() >= 4:
            raise ValidationError('Максимум 4 фото на товар.')

    def delete(self, *args, **kwargs):
        image_storage = self.image.storage
        image_path = self.image.name
        super().delete(*args, **kwargs)
        if image_path:
            image_storage.delete(image_path)

    def __str__(self):
        return f'{self.product.name} — фото {self.order + 1}'
