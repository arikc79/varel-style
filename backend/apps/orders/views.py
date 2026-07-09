import hmac
import os
import threading
import requests
import resend  # HTTP API — працює на Render free tier
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .backup import send_backup_email
from .models import Order
from .serializers import OrderSerializer


def send_telegram(text):
    token   = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if not token or not chat_id:
        return
    try:
        requests.post(
            f'https://api.telegram.org/bot{token}/sendMessage',
            json={'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'},
            timeout=5,
        )
    except Exception:
        pass


def send_order_email(order_id):
    api_key   = os.getenv('RESEND_API_KEY')
    recipient = os.getenv('NOTIFY_EMAIL')
    if not api_key or not recipient:
        print('[EMAIL] RESEND_API_KEY або NOTIFY_EMAIL не задано — пропускаємо')
        return
    print(f'[EMAIL] Відправка на {recipient} для замовлення #{order_id}')
    try:
        order = Order.objects.prefetch_related('items').get(pk=order_id)
        items_text = '\n'.join(
            f'  • {i.name} — {i.size}, {i.color} × {i.qty} = {i.price * i.qty} ₴'
            for i in order.items.all()
        )
        resend.api_key = api_key
        resend.Emails.send({
            'from': 'VAREL Style <onboarding@resend.dev>',
            'to':   [recipient],
            'subject': f'🛍 Нове замовлення #{order.id} — VAREL Style',
            'text': (
                f'Замовлення #{order.id}\n\n'
                f'Клієнт: {order.first_name} {order.last_name}\n'
                f'Телефон: {order.phone}\n'
                f'Email: {order.email}\n\n'
                f'Доставка: {order.get_delivery_type_display()} — {order.city}, {order.branch}\n'
                f'Оплата: {order.get_payment_type_display()}\n\n'
                f'Товари:\n{items_text}\n\n'
                f'Разом: {order.total} ₴'
            ),
        })
        print(f'[EMAIL] Успішно відправлено #{order_id}')
    except Exception as e:
        print(f'[EMAIL] Помилка #{order_id}: {e}')


class OrderCreateView(APIView):
    """POST /api/orders/ — створити нове замовлення"""

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            # Telegram
            items_text = '\n'.join(
                f'  • {i.name} ({i.size}, {i.color}) × {i.qty} — {i.price * i.qty} ₴'
                for i in order.items.all()
            )
            send_telegram(
                f'🛍 <b>Нове замовлення #{order.id}</b>\n\n'
                f'👤 {order.first_name} {order.last_name}\n'
                f'📞 {order.phone}\n'
                f'📧 {order.email}\n\n'
                f'🚚 {order.get_delivery_type_display()} — {order.city}, {order.branch}\n'
                f'💳 {order.get_payment_type_display()}\n\n'
                f'{items_text}\n\n'
                f'💰 <b>Разом: {order.total} ₴</b>'
            )

            # Email (background thread — не блокує відповідь)
            threading.Thread(target=send_order_email, args=(order.id,), daemon=True).start()

            return Response({'success': True, 'order_id': order.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListView(APIView):
    """GET /api/orders/ — список замовлень (для адміна)"""

    def get(self, request):
        orders = Order.objects.prefetch_related('items').all()[:50]
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class BackupTriggerView(APIView):
    """GET /api/orders/backup/?token=... — тригер бекапу для зовнішнього cron (напр. cron-job.org)"""

    def get(self, request):
        expected = os.getenv('BACKUP_TOKEN')
        token = request.query_params.get('token', '')
        if not expected or not hmac.compare_digest(token, expected):
            return Response({'error': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)

        sent = send_backup_email()
        return Response({'sent': sent})
