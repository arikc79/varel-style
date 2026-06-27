# Make.com Автоматизація

## Сценарії

### 1. Нове замовлення → Notion + Email
**Тригер:** Webhook від бекенду
**Дії:**
1. Записати замовлення в Notion database
2. Надіслати email менеджеру (info@first-style.ua)
3. Надіслати email підтвердження покупцю

### 2. Зміна статусу → Email покупцю
**Тригер:** Зміна поля "status" в Notion
**Дії:**
1. Надіслати email покупцю зі статусом

## Як налаштувати

1. Зайди на make.com → Create a new scenario
2. Перший модуль: **Webhooks → Custom webhook**
3. Скопіюй URL вебхуку → вставити в `.env` як `MAKE_WEBHOOK_URL`
4. Другий модуль: **Notion → Create a database item**
5. Третій модуль: **Email → Send an email**

## Структура Notion Database

| Поле | Тип |
|------|-----|
| Номер замовлення | Title |
| Клієнт | Text |
| Телефон | Phone |
| Email | Email |
| Товари | Text |
| Сума | Number |
| Доставка | Select |
| Оплата | Select |
| Статус | Select (🆕 Нове / ⚙️ В обробці / 📦 Відправлено / ✅ Виконано) |
| Дата | Date |
