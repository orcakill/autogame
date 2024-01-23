sqlacodegen url outfile=test_models.py  

# 生成requirements.txt
pip freeze > requirements.txt

# 更新前先更新pip版本
python.exe -m pip install --upgrade pip

# 打开项目目录，根据requirements.txt更新项目包
pip install -r requirements.txt