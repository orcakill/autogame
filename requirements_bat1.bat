@echo off  
cd %~dp0
call venv\Scripts\activate  
pip install --quiet -r requirements1.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
pause
