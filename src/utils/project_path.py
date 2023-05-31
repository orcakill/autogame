import os


def get_project_path():
    # 获取当前文件的绝对路径
    p_path = os.path.abspath(os.path.dirname(__file__))
    # 通过字符串截取方式截取，当前文件相对路径./src/util/StrUtil.py
    return p_path[:p_path.rindex('src')]
