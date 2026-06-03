# VAREL — Backend (Django)

## Встановлення

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate    # Mac/Linux

pip install -r requirements.txt
```

## Налаштування

```bash
cp .env.example .env
# Відкрий .env і заповни PostgreSQL дані (локально або Supabase)
```

Мінімум для локального запуску PostgreSQL:

```bash
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
DB_SSLMODE=prefer
```

## Запуск

```bash
python manage.py check --database default
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API endpoints

| Метод | URL | Опис |
|-------|-----|------|
| GET | `/api/products/` | Всі товари |
| GET | `/api/products/?category=Джинси` | Фільтр за категорією |
| GET | `/api/products/<id>/` | Один товар |
| POST | `/api/orders/` | Створити замовлення |
| GET | `/api/orders/list/` | Список замовлень |

## Адмін панель

```
http://localhost:8000/admin/
```

## Структура

```
backend/
├── manage.py
├── requirements.txt
├── .env.example
├── first_style/        ← налаштування Django
│   ├── settings.py
│   └── urls.py
└── apps/
    ├── products/       ← товари (model, view, serializer)
    └── orders/         ← замовлення (model, view, serializer)
```
