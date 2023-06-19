import os
import configparser


def get_project_path():
    """
    获取项目路径
    :return: 项目根路径
    """
    # 获取当前文件的绝对路径
    p_path = os.path.abspath(os.path.dirname(__file__))
    # 通过字符串截取方式截取，当前文件相对路径./src/util/StrUtil.py
    return p_path[:p_path.rindex('src')]


def get_database_url():
    root_path = get_project_path()
    config_path = root_path + "src\\resources\\config.ini"
    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8")
    return config.get("database", "url")


def get_onmyoji_image_path():
    project_path = get_project_path()
    return project_path + "src\\resources\\static\\onmyoji\\"
