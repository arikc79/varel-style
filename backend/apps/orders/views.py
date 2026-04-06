import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer

class OrderCreateView(APIView):
    """POST /api/orders/ — створити нове замовлення"""

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            # Відправляємо в Make.com webhook
            webhook_url = os.getenv('MAKE_WEBHOOK_URL')
            if webhook_url:
                try:
                    requests.post(webhook_url, json={
                        'order_id':   order.id,
                        'first_name': order.first_name,
                        'phone':      order.phone,
                        'email':      order.email,
                        'total':      order.total,
                        'delivery':   order.delivery_type,
                        'payment':    order.payment_type,
                        'items':      [
                            {'name': i.name, 'size': i.size, 'qty': i.qty, 'price': i.price}
                            for i in order.items.all()
                        ],
                    }, timeout=5)
                except Exception:
                    pass  # Не блокуємо відповідь якщо Make.com недоступний

            return Response({'success': True, 'order_id': order.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListView(APIView):
    """GET /api/orders/ — список замовлень (для адміна)"""

    def get(self, request):
        orders = Order.objects.prefetch_related('items').all()[:50]
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
