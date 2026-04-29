# VAREL — everyday style
## Структура проєкту
- `/backend/` — Django + DRF (бізнес-логіка, REST API, Django Admin)
- `/database/` — PostgreSQL схема та резервна копія даних
## Запуск локально
```bash
cd backend
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```
## Архітектура
Django-моноліт з вбудованим REST API.
Frontend: Django-шаблони + Vanilla JavaScript.
Кошик: localStorage браузера.
База даних: PostgreSQL.
