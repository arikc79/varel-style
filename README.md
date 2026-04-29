# VAREL Style 🛍️

> Інтернет-магазин чоловічого одягу. Вінниця, Україна.

## Стек

| Шар | Технологія |
|-----|-----------|
| Frontend | HTML / CSS / Vanilla JS |
| Backend | Python / Django / Django REST Framework |
| Database | PostgreSQL (Supabase) |
| Automation | Make.com (webhooks) |
| Hosting | Vercel (frontend) + Railway/Render (backend) |

## Структура репозиторію

```
varel-style/
├── frontend/          ← Верстка: HTML, CSS, JS
│   ├── index.html
│   ├── assets/
│   ├── css/
│   └── js/
├── backend/           ← Django API-сервер
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── apps/
│   │   ├── core/      ← базові views/urls
│   │   ├── products/  ← товари (CRUD + API)
│   │   └── orders/    ← замовлення (CRUD + API)
│   ├── first_style/   ← Django settings
│   ├── static/
│   └── templates/
├── database/          ← SQL-схема та seed-дані
│   ├── schema.sql
│   └── seed.sql
└── automation/        ← Make.com сценарії (JSON)
    └── make-scenarios/
        └── order-flow.json
```

## Швидкий старт

### Frontend
Відкрити `frontend/index.html` у браузері — або запустити live-server.

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp .env.example .env            # заповнити змінні
python manage.py migrate
python manage.py runserver
```

API доступний за адресою: `http://localhost:8000/api/`

### Змінні середовища (`.env`)

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
DB_SSLMODE=prefer
```

## Гілки

| Гілка | Призначення |
|-------|-------------|
| `main` | продакшн — не пушити напряму |
| `dev` | загальна розробка |
| `feature/frontend` | верстка |
| `feature/backend` | API / Django |
| `feature/database` | схема БД |
| `feature/automation` | Make.com |

## Команда

| Роль | Папка |
|------|-------|
| Frontend | `frontend/` |
| Backend | `backend/` |
| Database | `database/` |
| Automation | `automation/` |

## Правила

- ❌ Не пушити напряму в `main`
- ✅ Кожна задача — окремий PR → `dev`
- ✅ Формат комітів: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`
- ❌ Не комітити `.env`, `db.sqlite3`, користувацький `media/`
- ✅ Дозволено комітити демо-фото товарів у `backend/media/products/`

## Ліцензія

MIT © VAREL Style Team, 2026

