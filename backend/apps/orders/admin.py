from django.contrib import admin
from django.utils.html import format_html, mark_safe, escape
from django.urls import reverse
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model           = OrderItem
    extra           = 0
    can_delete      = False
    fields          = ['product_link', 'name', 'size', 'qty', 'price', 'subtotal']
    readonly_fields = ['product_link', 'name', 'size', 'qty', 'price', 'subtotal']

    def product_link(self, obj):
        if obj.product_id:
            url = reverse('admin:products_product_change', args=[obj.product_id])
            return format_html(
                '<a href="{}" target="_blank" style="font-size:11px">#{}</a>',
                url, obj.product_id,
            )
        return mark_safe('<span style="color:#999">—</span>')
    product_link.short_description = 'ID товару'

    def subtotal(self, obj):
        price = obj.price or 0
        qty   = obj.qty   or 0
        return format_html('<b>{} ₴</b>', f'{price * qty:,}')
    subtotal.short_description = 'Сума'


# ── Адмін замовлень ───────────────────────────────────────────────────────────

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # ID не в list_display_links → не є посиланням; кліки по рядку ведуть через order_link
    list_display        = ['order_number', 'client_info', 'items_summary',
                           'total_display', 'delivery_payment', 'status', 'created_at']
    list_display_links  = None          # Django не генерує жодних посилань сам
    list_filter         = ['status', 'delivery_type', 'payment_type']
    search_fields       = ['first_name', 'last_name', 'phone', 'email']
    list_editable       = ['status']
    readonly_fields     = ['created_at', 'full_order_card']
    inlines             = [OrderItemInline]
    fieldsets = (
        ('👤 Клієнт',            {'fields': ('first_name', 'last_name', 'phone', 'email')}),
        ('🚚 Доставка',          {'fields': ('delivery_type', 'city', 'branch')}),
        ('💳 Оплата та сума',    {'fields': ('payment_type', 'total')}),
        ('📋 Статус',            {'fields': ('status', 'created_at')}),
        ('🛒 Склад замовлення',  {'fields': ('full_order_card',)}),
    )

    # ── Колонки списку ────────────────────────────────────────────────────────

    def order_number(self, obj):
        url = reverse('admin:orders_order_change', args=[obj.pk])
        return format_html(
            '<a href="{}" target="_blank" style="font-weight:bold;font-size:13px">#{}</a>',
            url, obj.pk,
        )
    order_number.short_description = '№'
    order_number.admin_order_field = 'id'

    def client_info(self, obj):
        name = escape(f'{obj.first_name} {obj.last_name}'.strip())
        phone = escape(obj.phone)
        email = escape(obj.email) if obj.email else ''
        lines = [f'<b>{name}</b>', phone]
        if email:
            lines.append(f'<span style="color:#666;font-size:11px">{email}</span>')
        return mark_safe('<br>'.join(lines))
    client_info.short_description = 'Клієнт'

    def items_summary(self, obj):
        items = list(obj.items.all()[:3])
        if not items:
            return '—'
        lines = [
            f'<span style="font-size:12px">{escape(i.name)} '
            f'<span style="color:#888">×{i.qty} / {escape(i.size)}</span></span>'
            for i in items
        ]
        rest = obj.items.count() - 3
        if rest > 0:
            lines.append(f'<span style="color:#888;font-size:11px">… ще {rest} поз.</span>')
        return mark_safe('<br>'.join(lines))
    items_summary.short_description = 'Товари'

    def total_display(self, obj):
        return format_html(
            '<b style="color:#1a7a3c;font-size:14px">{} ₴</b>', f'{obj.total:,}'
        )
    total_display.short_description = 'Сума'
    total_display.admin_order_field = 'total'

    def delivery_payment(self, obj):
        d = escape(dict(Order.DELIVERY_CHOICES).get(obj.delivery_type, obj.delivery_type))
        p = escape(dict(Order.PAYMENT_CHOICES).get(obj.payment_type, obj.payment_type))
        city = f'<br><span style="color:#666;font-size:11px">{escape(obj.city)}</span>' if obj.city else ''
        return mark_safe(f'{d}{city}<br><span style="color:#555;font-size:11px">{p}</span>')
    delivery_payment.short_description = 'Доставка / Оплата'

    # ── Повна картка на сторінці замовлення ───────────────────────────────────

    def full_order_card(self, obj):
        items = list(obj.items.all())
        if not items:
            return mark_safe('<p style="color:#999">Позиції відсутні</p>')

        # Рядки товарів
        rows = ''
        for i, item in enumerate(items):
            bg    = '#fff' if i % 2 == 0 else '#f9f9f9'
            price = item.price or 0
            qty   = item.qty   or 0
            sub   = price * qty
            prod_link = ''
            if item.product_id:
                url = reverse('admin:products_product_change', args=[item.product_id])
                prod_link = f' <a href="{url}" target="_blank" style="font-size:10px;color:#999">[відкрити]</a>'
            rows += (
                f'<tr style="background:{bg}">'
                f'<td style="padding:8px 14px">{escape(item.name)}{prod_link}</td>'
                f'<td style="padding:8px 14px;text-align:center">'
                f'  <span style="background:#e8f4ff;padding:2px 8px;border-radius:4px;font-size:12px">'
                f'  {escape(item.size)}</span>'
                f'</td>'
                f'<td style="padding:8px 14px;text-align:center">{item.qty}</td>'
                f'<td style="padding:8px 14px;text-align:right">{price:,} ₴</td>'
                f'<td style="padding:8px 14px;text-align:right">'
                f'  <b style="color:#1a7a3c">{sub:,} ₴</b>'
                f'</td>'
                f'</tr>'
            )

        # Блоки інфо
        delivery_label = escape(dict(Order.DELIVERY_CHOICES).get(obj.delivery_type, obj.delivery_type))
        payment_label  = escape(dict(Order.PAYMENT_CHOICES).get(obj.payment_type, obj.payment_type))
        city_branch = ''
        if obj.city or obj.branch:
            city_branch = (
                f'<div style="margin-top:4px;font-size:12px;color:#555">'
                f'{escape(obj.city)}{"," if obj.city and obj.branch else ""} {escape(obj.branch)}'
                f'</div>'
            )

        html = f'''
        <div style="max-width:780px;font-family:sans-serif;font-size:13px">

          <!-- Клієнт / Доставка / Оплата -->
          <div style="display:flex;gap:16px;margin-bottom:16px;flex-wrap:wrap">

            <div style="flex:1;min-width:200px;background:#f0f4ff;border-radius:8px;padding:12px 16px">
              <div style="font-weight:bold;margin-bottom:6px;color:#2c3e50">👤 Клієнт</div>
              <div><b>{escape(obj.first_name)} {escape(obj.last_name)}</b></div>
              <div style="margin-top:4px">📞 {escape(obj.phone)}</div>
              {"<div style='margin-top:4px'>✉️ " + escape(obj.email) + "</div>" if obj.email else ""}
            </div>

            <div style="flex:1;min-width:200px;background:#f0fff4;border-radius:8px;padding:12px 16px">
              <div style="font-weight:bold;margin-bottom:6px;color:#2c3e50">🚚 Доставка</div>
              <div>{delivery_label}</div>
              {city_branch}
            </div>

            <div style="flex:1;min-width:200px;background:#fff8f0;border-radius:8px;padding:12px 16px">
              <div style="font-weight:bold;margin-bottom:6px;color:#2c3e50">💳 Оплата</div>
              <div>{payment_label}</div>
              <div style="margin-top:8px;font-size:15px">
                Разом: <b style="color:#1a7a3c">{obj.total:,} ₴</b>
              </div>
            </div>

          </div>

          <!-- Таблиця товарів -->
          <table style="width:100%;border-collapse:collapse;border:1px solid #ddd;border-radius:8px;overflow:hidden">
            <thead>
              <tr style="background:#2c3e50;color:#fff">
                <th style="padding:10px 14px;text-align:left">Товар</th>
                <th style="padding:10px 14px;text-align:center">Розмір</th>
                <th style="padding:10px 14px;text-align:center">К-сть</th>
                <th style="padding:10px 14px;text-align:right">Ціна</th>
                <th style="padding:10px 14px;text-align:right">Сума</th>
              </tr>
            </thead>
            <tbody>{rows}</tbody>
            <tfoot>
              <tr style="background:#f5f5f5;border-top:2px solid #ddd">
                <td colspan="4" style="padding:10px 14px;text-align:right;font-size:14px">
                  <b>Загальна сума:</b>
                </td>
                <td style="padding:10px 14px;text-align:right;font-size:16px">
                  <b style="color:#1a7a3c">{obj.total:,} ₴</b>
                </td>
              </tr>
            </tfoot>
          </table>

        </div>
        '''
        return mark_safe(html)
    full_order_card.short_description = 'Деталі замовлення'