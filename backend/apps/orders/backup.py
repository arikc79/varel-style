import os

import resend
from django.core import serializers
from django.utils import timezone

from .models import Customer, Order, OrderItem


def build_backup_json():
    """Серіалізує Customer/Order/OrderItem в один JSON-дамп (для dumpdata/loaddata)."""
    objects = list(Customer.objects.all()) + list(Order.objects.all()) + list(OrderItem.objects.all())
    return serializers.serialize('json', objects, indent=2)


def send_backup_email():
    """Надсилає JSON-дамп Customer/Order/OrderItem на NOTIFY_EMAIL через Resend.

    Render Free видаляє PostgreSQL раз на ~30 днів, а диск ефемерний —
    тому бекап одразу відправляється, а не зберігається локально.
    """
    api_key   = os.getenv('RESEND_API_KEY')
    recipient = os.getenv('NOTIFY_EMAIL')
    if not api_key or not recipient:
        print('[BACKUP] RESEND_API_KEY або NOTIFY_EMAIL не задано — пропускаємо')
        return False

    today = timezone.now()
    data = build_backup_json()
    filename = f'varel_backup_{today:%Y-%m-%d}.json'

    resend.api_key = api_key
    resend.Emails.send({
        'from': 'VAREL Style <onboarding@resend.dev>',
        'to': [recipient],
        'subject': f'🗄 Бекап бази VAREL Style — {today:%Y-%m-%d}',
        'text': (
            f'Автоматичний бекап Customer/Order/OrderItem у вкладенні.\n\n'
            f'Клієнтів: {Customer.objects.count()}\n'
            f'Замовлень: {Order.objects.count()}\n\n'
            f'Відновлення: python manage.py loaddata {filename}'
        ),
        'attachments': [{
            'filename': filename,
            'content': list(data.encode('utf-8')),
        }],
    })
    print(f'[BACKUP] Відправлено {filename} на {recipient}')
    return True
