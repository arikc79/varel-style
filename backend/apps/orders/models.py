from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class Customer(models.Model):
    phone         = models.CharField(max_length=20, unique=True, verbose_name='Телефон')
    first_name    = models.CharField(max_length=100, verbose_name='Ім\'я')
    email         = models.EmailField(blank=True, verbose_name='Email')
    total_orders  = models.PositiveIntegerField(default=0, verbose_name='Замовлень')
    total_spent   = models.PositiveIntegerField(default=0, verbose_name='Витрачено ₴')
    created_at    = models.DateTimeField(auto_now_add=True, verbose_name='Перше замовлення')
    last_order_at = models.DateTimeField(null=True, blank=True, verbose_name='Останнє замовлення')

    class Meta:
        ordering            = ['-last_order_at']
        verbose_name        = 'Клієнт'
        verbose_name_plural = 'Клієнти'

    def __str__(self):
        return f'{self.first_name} {self.phone}'


class Order(models.Model):
    class Status(models.TextChoices):
        NEW        = 'new',        '🆕 Нове'
        PROCESSING = 'processing', '⚙️ В обробці'
        SHIPPED    = 'shipped',    '📦 Відправлено'
        DONE       = 'done',       '✅ Виконано'

    class Delivery(models.TextChoices):
        NOVA_POSHTA = 'nova', 'Нова Пошта'
        UKRPOSHTA   = 'ukr',  'Укрпошта'

    class Payment(models.TextChoices):
        CARD = 'card', 'Карткою онлайн'
        CASH = 'cash', 'При отриманні'

    phone_validator = RegexValidator(
        regex=r'^\+?\d{10,15}$',
        message="Телефон повинен бути у форматі +XXXXXXXXXXX"
    )

    customer      = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='orders', verbose_name='Клієнт')
    first_name    = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100, blank=True)
    phone         = models.CharField(max_length=20, validators=[phone_validator])
    email         = models.EmailField(blank=True)
    delivery_type = models.CharField(max_length=10, choices=Delivery)
    city          = models.CharField(max_length=100, blank=True)
    branch        = models.CharField(max_length=255, blank=True)
    payment_type  = models.CharField(max_length=10, choices=Payment)
    total         = models.PositiveIntegerField()
    status        = models.CharField(max_length=20, choices=Status, default=Status.NEW)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering            = ['-created_at']
        verbose_name        = 'Замовлення'
        verbose_name_plural = 'Замовлення'

    def __str__(self):
        return f'#{self.pk} — {self.first_name} {self.phone}'

    def save(self, *args, **kwargs):
        if self.pk:
            old_status = Order.objects.filter(pk=self.pk).values_list('status', flat=True).first()
            if old_status != self.Status.SHIPPED and self.status == self.Status.SHIPPED:
                self._deduct_stock()
        super().save(*args, **kwargs)

    def _deduct_stock(self):
        from apps.products.models import ProductSizeStock
        for item in self.items.all():
            if not item.product_id:
                continue
            stock = ProductSizeStock.objects.filter(
                product_id=item.product_id,
                size=item.size,
            ).first()
            if stock:
                stock.quantity = max(0, stock.quantity - item.qty)
                stock.save()


class OrderItem(models.Model):
    order   = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey("products.Product", on_delete=models.SET_NULL, null=True, blank=True)
    name    = models.CharField(max_length=255)
    price   = models.PositiveIntegerField()
    size    = models.CharField(max_length=10)
    color   = models.CharField(max_length=50, default='Без кольору')
    qty     = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name        = 'Товар у замовленні'
        verbose_name_plural = 'Товари у замовленні'

    def __str__(self):
        return f'{self.name} x{self.qty} ({self.size}, {self.color})'
