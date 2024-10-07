@echo off  
cd %~dp0
call venv\Scripts\activate  
python src\main_day_1.py /file log\bat\main_day_1_%date:~0,4%%date:~5,2%%date:~8,2%.log
pause

