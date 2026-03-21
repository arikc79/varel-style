# Frontend — VAREL

> ⚠️ **Статичний `frontend/` більше не використовується як точка входу.**  
> Починаючи з коміту `feat: migrate to Django full-stack` — фронтенд обслуговується через **Django Templates**.

---

## Де тепер знаходиться фронтенд

```
backend/
├── templates/
│   ├── base.html        ← базовий шаблон (nav, footer, модали, scripts)
│   └── index.html       ← головна сторінка ({% extends "base.html" %})
└── static/
    ├── css/
    │   ├── main.css     ← змінні, reset, типографіка, nav, footer
    │   ├── hero.css     ← hero секція
    │   ├── products.css ← каталог, картки товарів, фільтри
    │   ├── cart.css     ← кошик сайдбар
    │   └── checkout.css ← форма оформлення
    ├── js/
    │   ├── ui.js        ← toast, анімації, ESC-хендлер
    │   ├── cart.js      ← логіка кошика + збереження в localStorage
    │   ├── products.js  ← fetch('/api/products/') + рендер карток
    │   ├── modal.js     ← модальне вікно товару
    │   └── checkout.js  ← POST /api/orders/ з CSRF-токеном
    └── assets/
        └── hero.jpg     ← фото для hero
```

---

## Запуск

Фронтенд запускається разом із Django-сервером:

```bash
cd backend
python manage.py runserver
# Відкрити: http://127.0.0.1:8000/
```

---

## Як підключено до API

### Товари
`backend/static/js/products.js` завантажує товари з бази даних:
```js
// ✅ Реалізовано
const res = await fetch('/api/products/');
const products = await res.json();
```

### Замовлення
`backend/static/js/checkout.js` відправляє замовлення на бекенд:
```js
// ✅ Реалізовано
await fetch('/api/orders/', {
  method: 'POST',
  headers: { 'X-CSRFToken': getCsrfToken() },
  body: JSON.stringify(payload),
});
```

### Кошик
`backend/static/js/cart.js` зберігає стан між сесіями:
```js
// ✅ Реалізовано
localStorage.setItem('varel_cart', JSON.stringify(cart));
```

---

## Django Template теги

У шаблонах використовуються стандартні Django-теги:

```html
{% load static %}
{% static 'css/main.css' %}   <!-- підключення CSS -->
{% static 'js/products.js' %} <!-- підключення JS  -->
{% url 'index' %}             <!-- посилання на головну -->
{% block content %}{% endblock %} <!-- точка розширення -->
```

---

## Папка `frontend/` (застаріла)

Оригінальні файли збережено для довідки:

```
frontend/
├── index.html   ← оригінальна статична версія (не використовується)
├── css/         ← скопійовано в backend/static/css/
├── js/          ← перероблено і перенесено в backend/static/js/
└── assets/      ← скопійовано в backend/static/assets/
```
