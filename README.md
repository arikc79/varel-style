# 🎉 VAREL STYLE - Інтернет-магазин одягу

> Django веб-додаток для продажу одягу з адмін-панеллю, API та системою замовлень

![Django](https://img.shields.io/badge/Django-6.0.4-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Швидкий старт (2 кроки!)

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

> ⚡ Скрипт автоматично: перевірить Python → створить venv → встановить залежності → налаштує БД → створить адміна → запустить сервер

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
- 📸 **25 фото товарів**

---

## 🛠️ Технології

| Категорія | Технологія |
|-----------|------------|
| Backend | Django 6.0.4 + Django REST Framework |
| Database | SQLite (можна PostgreSQL) |
| Frontend | Django Templates + Vanilla JavaScript |
| API | Django REST Framework |
| Media | Pillow для обробки зображень |

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

# 5. Виконайте міграції
python manage.py migrate

# 6. Створіть суперкористувача
python manage.py createsuperuser

# 7. Запустіть сервер
python manage.py runserver
```

---

## 🔧 Налаштування

### Перехід на PostgreSQL:

1. Встановіть PostgreSQL
2. Відредагуйте `backend/.env`:
   ```env
   USE_SQLITE=False
   DB_NAME=varel_style
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```
3. Виконайте міграції:
   ```bash
   python manage.py migrate
   ```

### Інтеграція з Make.com:

У файлі `backend/.env` додайте:
```env
MAKE_WEBHOOK_URL=https://hook.eu1.make.com/your-webhook-id
```

---

## 🎨 Скріншоти

(Тут можна додати скріншоти вашого сайту)

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

## 🎯 TODO (майбутні покращення)

- [ ] Додати пошук товарів
- [ ] Додати відгуки користувачів
- [ ] Інтегрувати оплату (Stripe/LiqPay)
- [ ] Додати багатомовність
- [ ] Створити мобільний додаток
- [ ] Додати бажаний список (wishlist)

---

**Зроблено з ❤️ для VAREL STYLE**

⭐ Поставте зірку, якщо проект вам сподобався!

