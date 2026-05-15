@echo off
cd %~dp0
call venv\Scripts\activate
python src\main.py /file log\bat\main_%date:~0,4%%date:~5,2%%date:~8,2%.log
pause

