@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
cd /d "%~dp0"

rem Create log directory
if not exist "logs\bat" mkdir "logs\bat"

rem 用 PowerShell 获取纯数字日期（如 20260530）
for /f %%a in ('powershell -Command "Get-Date -Format yyyyMMdd"') do set "datestr=%%a"
set "logfile=logs\bat\main_day_all_%datestr%.log"

echo [%date% %time%] Checking for running main_day_all.py...

set "found=0"
for /f "tokens=2 delims==" %%i in ('wmic process where "name='python.exe' and commandline like '%%main_day_all.py%%'" get processid /value 2^>nul') do (
    set "found=1"
    echo [%date% %time%] Found PID=%%i, terminating...
    taskkill /f /pid %%i >nul 2>&1
)
if %found% equ 0 (
    echo [%date% %time%] No running process found.
) else (
    timeout /t 2 /nobreak >nul
    echo [%date% %time%] Process terminated.
)

call venv\Scripts\activate
echo [%date% %time%] Starting main_day_all.py...
python src\main_day_all.py >> "%logfile%" 2>&1