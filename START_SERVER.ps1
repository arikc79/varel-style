# VAREL STYLE - Запуск Django сервера
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   VAREL STYLE - Django Server" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Запуск сервера на http://127.0.0.1:8000" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Адмін панель: http://127.0.0.1:8000/admin" -ForegroundColor White
Write-Host "   Логін: admin" -ForegroundColor Gray
Write-Host "   Пароль: admin123" -ForegroundColor Gray
Write-Host ""
Write-Host "Натисніть Ctrl+C щоб зупинити сервер" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "$PSScriptRoot\backend"
& .\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000

