from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ('new',        '🆕 Нове'),
        ('processing', '⚙️ В обробці'),
        ('shipped',    '📦 Відправлено'),
        ('done',       '✅ Виконано'),
    ]
    DELIVERY_CHOICES = [
        ('nova', 'Нова Пошта'),
        ('ukr',  'Укрпошта'),
    ]
    PAYMENT_CHOICES = [
        ('card', 'Карткою онлайн'),
        ('cash', 'При отриманні'),
    ]

    first_name    = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100, blank=True)
    phone         = models.CharField(max_length=20)
    email         = models.EmailField(blank=True)
    delivery_type = models.CharField(max_length=10, choices=DELIVERY_CHOICES)
    city          = models.CharField(max_length=100, blank=True)
    branch        = models.CharField(max_length=255, blank=True)
    payment_type  = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    total         = models.PositiveIntegerField()
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

    def __str__(self):
        return f'#{self.pk} — {self.first_name} {self.phone}'


class OrderItem(models.Model):
    order      = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_id = models.PositiveIntegerField()
    name       = models.CharField(max_length=255)
    price      = models.PositiveIntegerField()
    size       = models.CharField(max_length=10)
    qty        = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.name} x{self.qty} ({self.size})'
