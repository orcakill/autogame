@echo off
cd %~dp0
"%~dp0.venv\python.exe" src\main.py /file log\bat\main_%date:~0,4%%date:~5,2%%date:~8,2%.log
pause

