from django.db import models
from django.core.validators import RegexValidator

class Order(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', '🆕 Нове'
        PROCESSING = 'processing', '⚙️ В обробці'
        SHIPPED = 'shipped', '📦 Відправлено'
        DONE = 'done', '✅ Виконано'

    class Delivery(models.TextChoices):
        NOVA_POSHTA = 'nova', 'Нова Пошта'
        UKRPOSHTA = 'ukr', 'Укрпошта'

    class Payment(models.TextChoices):
        CARD = 'card', 'Карткою онлайн'
        CASH = 'cash', 'При отриманні'

    phone_validator = RegexValidator(
        regex=r'^\+?\d{9}$',
        message="Телефон повинен бути у форматі +XXXXXXXXXXX"
    )

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
        ordering = ['-created_at']
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

    def __str__(self):
        return f'#{self.pk} — {self.first_name} {self.phone}'


class OrderItem(models.Model):
    order      = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product    = models.ForeignKey("products.Product", on_delete=models.SET_NULL, null=True, blank=True)
    name       = models.CharField(max_length=255)
    price      = models.PositiveIntegerField()
    size       = models.CharField(max_length=10)
    qty        = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Товар у замовленні'
        verbose_name_plural = 'Товари у замовленні'

    def __str__(self):
        return f'{self.name} x{self.qty} ({self.size})'
