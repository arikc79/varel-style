@echo off
setlocal

set HOST=%~1
set PORT=%~2

if "%HOST%"=="" set HOST=127.0.0.1
if "%PORT%"=="" set PORT=8000

powershell -ExecutionPolicy Bypass -File "%~dp0run.ps1" -ServerHost %HOST% -Port %PORT%

