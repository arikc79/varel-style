@echo off
chcp 65001 >nul
cls
echo ════════════════════════════════════════════════════════════
echo            🚀 VAREL STYLE - АВТОМАТИЧНЕ НАЛАШТУВАННЯ
echo ════════════════════════════════════════════════════════════
echo.

REM Перевірка Python
echo [1/6] Перевірка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не знайдено!
    echo.
    echo Будь ласка, встановіть Python 3.10+ з https://www.python.org/
    echo.
    pause
    exit /b 1
)
echo ✅ Python встановлено
echo.

REM Перехід до папки backend
cd /d "%~dp0backend"

REM Створення віртуального середовища
echo [2/6] Створення віртуального середовища...
if exist ".venv\" (
    echo ⏭️  Віртуальне середовище вже існує
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Помилка створення віртуального середовища
        pause
        exit /b 1
    )
    echo ✅ Віртуальне середовище створено
)
echo.

REM Встановлення залежностей
echo [3/6] Встановлення залежностей...
call .venv\Scripts\python.exe -m pip install --upgrade pip --quiet
call .venv\Scripts\python.exe -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Помилка встановлення залежностей
    pause
    exit /b 1
)
echo ✅ Залежності встановлено
echo.

REM Перевірка .env
echo [4/6] Налаштування конфігурації...
if not exist ".env" (
    copy .env.example .env >nul
    echo ✅ Файл .env створено
) else (
    echo ⏭️  Файл .env вже існує
)
echo.

REM Перевірка PostgreSQL
echo [4.5/6] Перевірка PostgreSQL...
psql --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  PostgreSQL не знайдено!
    echo.
    echo 📝 ВАЖЛИВО: Проект використовує PostgreSQL як основну БД.
    echo.
    echo Варіанти:
    echo 1. Встановіть PostgreSQL: https://www.postgresql.org/download/
    echo 2. Або використайте SQLite для тестування:
    echo    Відредагуйте .env і додайте рядок: USE_SQLITE=True
    echo.
    echo Натисніть будь-яку клавішу для продовження зі SQLite...
    pause >nul
    echo USE_SQLITE=True >> .env
    echo ⚠️  Використовується SQLite замість PostgreSQL
) else (
    echo ✅ PostgreSQL встановлено
)
echo.

REM Міграції
echo [5/6] Налаштування бази даних...
call .venv\Scripts\python.exe manage.py migrate --noinput >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Виконую міграції детально...
    call .venv\Scripts\python.exe manage.py migrate
)
echo ✅ База даних налаштована
echo.

REM Перевірка суперкористувача
echo [6/6] Перевірка адміністратора...
call .venv\Scripts\python.exe manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('exists' if User.objects.filter(username='admin').exists() else 'create')" >temp_check.txt 2>nul
set /p ADMIN_EXISTS=<temp_check.txt
del temp_check.txt >nul 2>&1

if "%ADMIN_EXISTS%"=="exists" (
    echo ⏭️  Адміністратор вже існує
) else (
    echo Створення адміністратора...
    echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') | call .venv\Scripts\python.exe manage.py shell >nul 2>&1
    echo ✅ Адміністратор створений (admin / admin123)
)
echo.

REM Імпорт даних
if exist "..\database\db_backup.json" (
    echo 📦 Завантаження демо-даних...
    cd ..
    call backend\.venv\Scripts\python.exe import_data.py >nul 2>&1
    if not errorlevel 1 (
        echo ✅ Демо-дані завантажено
    )
    cd backend
    echo.
)

echo ════════════════════════════════════════════════════════════
echo               ✅ НАЛАШТУВАННЯ ЗАВЕРШЕНО!
echo ════════════════════════════════════════════════════════════
echo.
echo 🚀 Запускаю сервер на http://127.0.0.1:8000
echo.
echo 📝 Адмін панель: http://127.0.0.1:8000/admin
echo    Логін: admin
echo    Пароль: admin123
echo.
echo Натисніть Ctrl+C щоб зупинити сервер
echo ════════════════════════════════════════════════════════════
echo.

REM Запуск сервера
call .venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000

pause

