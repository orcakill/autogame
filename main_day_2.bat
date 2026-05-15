@echo off
cd %~dp0
call venv\Scripts\activate
python src\main_day_2.py > log\bat\main_day_2.log

