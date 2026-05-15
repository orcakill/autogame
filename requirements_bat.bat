@echo off  
cd %~dp0
call venv\Scripts\activate  
pip install -r requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
pause
