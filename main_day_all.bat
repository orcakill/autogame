@echo off
cd %~dp0

:: 终止正在运行的 main_day_all.py 进程
echo [%date% %time%] 检查并终止已存在的 main_day_all.py 进程...
tasklist /fi "imagename eq python.exe" /fo csv | find /i "main_day_all.py" >nul
if %errorlevel% equ 0 (
    echo [%date% %time%] 发现正在运行的进程，正在终止...
    taskkill /f /im python.exe /fi "windowtitle eq main_day_all.py*" >nul 2>&1
    timeout /t 2 /nobreak >nul
    echo [%date% %time%] 进程终止完成
) else (
    echo [%date% %time%] 未发现正在运行的进程
)

:: 激活虚拟环境并启动 Python 脚本
call venv\Scripts\activate
echo [%date% %time%] 启动 main_day_all.py...
python src\main_day_all.py >> "logs\bat\main_day_all_%date:~0,4%%date:~5,2%%date:~8,2%.log"