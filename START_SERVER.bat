@echo off
cd /d "%~dp0backend"
echo ========================================
echo   VAREL STYLE - Django Server
echo ========================================
echo.
echo Запуск сервера на http://127.0.0.1:8000
echo.
echo Адмін панель: http://127.0.0.1:8000/admin
echo Логін: admin
echo Пароль: admin123
echo.
echo Натисніть Ctrl+C щоб зупинити сервер
echo ========================================
echo.
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
pause

