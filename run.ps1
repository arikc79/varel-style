param(
    [string]$ServerHost = "127.0.0.1",
    [int]$Port = 8000
)

$backendManage = Join-Path $PSScriptRoot "backend\manage.py"

if (-not (Test-Path $backendManage)) {
    Write-Error "backend/manage.py was not found. Check project path."
    exit 1
}

python $backendManage runserver "$ServerHost`:$Port"
