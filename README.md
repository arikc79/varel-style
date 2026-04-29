# 🎉 VAREL STYLE - Інтернет-магазин одягу

> Django веб-додаток для продажу одягу з адмін-панеллю, API та системою замовлень

![Django](https://img.shields.io/badge/Django-6.0.4-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Швидкий старт (2 кроки!)

### Перед початком:
**Встановіть PostgreSQL 12+** з https://www.postgresql.org/download/

> 💡 Або використайте SQLite для швидкого тестування (додайте `USE_SQLITE=True` у `.env`)

### 1️⃣ Клонуйте репозиторій:
```bash
git clone https://github.com/arikc79/varel-style.git
cd varel-style
```

### 2️⃣ Запустіть автоматичне налаштування:
```bash
# Windows - просто двічі клацніть:
SETUP_AND_RUN.bat

# Або вручну через PowerShell:
.\SETUP_AND_RUN.bat
```

**Готово!** 🎉 Сервер запуститься на http://127.0.0.1:8000

> ⚡ Скрипт автоматично: перевірить PostgreSQL → створить venv → встановить залежності → налаштує БД → створить адміна → запустить сервер

---

## 🌐 Посилання

- **Головна**: http://127.0.0.1:8000/
- **Каталог**: http://127.0.0.1:8000/catalog
- **Адмін панель**: http://127.0.0.1:8000/admin
- **API**: http://127.0.0.1:8000/api/products/

## 🔑 Дані для входу

- **Логін**: `admin`
- **Пароль**: `admin123`

---

## 📦 Що включено

### Готовий функціонал:
- ✅ Каталог товарів з фільтрами по категоріях
- ✅ Сторінки окремих товарів з фото
- ✅ Кошик (localStorage)
- ✅ Оформлення замовлення
- ✅ REST API для інтеграцій
- ✅ Адмін панель Django
- ✅ Інтеграція з Make.com webhook

### Демо-дані:
- 👖 **Джинси** - 3 моделі (Berlin Slim Fit, Rio Skinny Fit, Oslo Carrot Fit)
- 👟 **Кросівки** - 2 моделі AVVA
- 👔 **Сорочки** - 2 моделі (Britli Striped Seersucker, AVVA)
- 📸 **27 фото товарів**

---

## 🛠️ Технології

| Категорія | Технологія |
|-----------|------------|
| Backend | Django 6.0.4 + Django REST Framework |
| **Database** | **PostgreSQL 12+** (SQLite fallback) |
| Frontend | Django Templates + Vanilla JavaScript |
| API | Django REST Framework |
| Media | Pillow для обробки зображень |

---

## 🗄️ Налаштування бази даних

### PostgreSQL (рекомендовано):

1. **Встановіть PostgreSQL**: https://www.postgresql.org/download/

2. **Створіть базу даних**:
   ```bash
   # Windows (через psql)
   psql -U postgres
   CREATE DATABASE varel_style;
   \q
   ```

3. **Налаштуйте `backend/.env`**:
   ```env
   DB_NAME=varel_style
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

4. **Запустіть SETUP_AND_RUN.bat** - він автоматично виконає міграції

### SQLite (для швидкого тестування):

Якщо PostgreSQL не встановлений, додайте у `backend/.env`:
```env
USE_SQLITE=True
```

---

## 📁 Структура проекту

```
varel-style/
├── SETUP_AND_RUN.bat          # 🚀 Автоматичне налаштування та запуск
├── START_SERVER.bat            # 🏃 Швидкий запуск (після налаштування)
├── ІНСТРУКЦІЯ_ЗАПУСКУ.md       # 📖 Детальна документація
├── import_data.py              # 📦 Скрипт імпорту демо-даних
├── .gitignore                  # 🚫 Git ignore rules
├── backend/
│   ├── manage.py               # Django CLI
│   ├── requirements.txt        # Python залежності
│   ├── .env.example            # Приклад конфігурації
│   ├── apps/
│   │   ├── products/           # 📦 Додаток товарів
│   │   ├── orders/             # 🛒 Додаток замовлень
│   │   └── core/               # 🏠 Основні сторінки
│   ├── first_style/            # ⚙️ Django налаштування
│   ├── media/products/         # 🖼️ Фото товарів
│   ├── static/                 # 🎨 CSS/JS файли
│   └── templates/              # 📄 HTML шаблони
└── database/
    └── db_backup.json          # 💾 Backup даних
```

---

## 📡 API Endpoints

| Метод | URL | Опис |
|-------|-----|------|
| `GET` | `/api/products/` | Список всіх товарів |
| `GET` | `/api/products/?category=Джинси` | Товари за категорією |
| `GET` | `/api/products/<id>/` | Деталі товару |
| `POST` | `/api/orders/` | Створити замовлення |
| `GET` | `/api/orders/list/` | Список замовлень |
| `GET` | `/api/categories/` | Список категорій |

### Приклад запиту:
```bash
curl http://127.0.0.1:8000/api/products/
```

---

## ⚙️ Ручне налаштування (опціонально)

Якщо хочете налаштувати вручну:

```bash
# 1. Створіть віртуальне середовище
cd backend
python -m venv .venv

# 2. Активуйте його
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux

# 3. Встановіть залежності
pip install -r requirements.txt

# 4. Налаштуйте .env
copy .env.example .env
# Відредагуйте .env з вашими даними PostgreSQL

# 5. Виконайте міграції
python manage.py migrate

# 6. Створіть суперкористувача
python manage.py createsuperuser

# 7. Завантажте демо-дані (опціонально)
cd ..
python import_data.py

# 8. Запустіть сервер
cd backend
python manage.py runserver
```

---

## 🔧 Конфігурація

### Приклад файлу `.env`:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL Database
DB_NAME=varel_style
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_SSLMODE=prefer
DB_CONN_MAX_AGE=60

# Fallback на SQLite (опціонально)
# USE_SQLITE=True

# Make.com Webhook (опціонально)
MAKE_WEBHOOK_URL=https://hook.eu1.make.com/your-webhook
```

---

## 🎨 Скріншоти

(Тут можна додати скріншоти вашого сайту)

---

## 📝 Що робить SETUP_AND_RUN.bat

1. ✅ Перевіряє Python 3.10+
2. ✅ Перевіряє PostgreSQL
3. ✅ Створює віртуальне середовище
4. ✅ Встановлює залежності
5. ✅ Копіює `.env.example` → `.env`
6. ✅ Виконує міграції
7. ✅ Створює адміністратора (admin / admin123)
8. ✅ Імпортує демо-дані
9. ✅ Запускає сервер

**Якщо PostgreSQL не знайдений**, скрипт автоматично запропонує використати SQLite.

---

## 🐛 Troubleshooting

### PostgreSQL не знайдений:
```bash
# Перевірте встановлення
psql --version

# Якщо не встановлений, завантажте:
https://www.postgresql.org/download/
```

### Помилка з'єднання з БД:
```bash
# Перевірте, чи запущений PostgreSQL
# Windows:
services.msc  # Знайдіть postgresql-x64-XX

# Або використайте SQLite:
echo USE_SQLITE=True >> backend\.env
```

### Інші проблеми:
- Перегляньте `ІНСТРУКЦІЯ_ЗАПУСКУ.md`
- Створіть [Issue на GitHub](https://github.com/arikc79/varel-style/issues)

---

## 🎯 TODO (майбутні покращення)

- [ ] Додати пошук товарів
- [ ] Додати відгуки користувачів
- [ ] Інтегрувати оплату (Stripe/LiqPay)
- [ ] Додати багатомовність
- [ ] Створити мобільний додаток
- [ ] Додати wishlist

---

## 📝 Ліцензія

MIT License - використовуйте як завгодно!

---

## 🤝 Підтримка

Якщо виникли питання:
1. Перегляньте файл `ІНСТРУКЦІЯ_ЗАПУСКУ.md`
2. Перевірте [Django документацію](https://docs.djangoproject.com/)
3. Створіть Issue на GitHub

---

**Зроблено з ❤️ для VAREL STYLE**

⭐ Поставте зірку, якщо проект вам сподобався!

