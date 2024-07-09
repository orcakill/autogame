import configparser
import os
from datetime import datetime as imp_datetime


class UtilsPath:
    @staticmethod
    def get_project_path():
        """
        获取项目路径
        :return: 项目根路径
        """
        # 获取当前文件的绝对路径
        p_path = os.path.abspath(os.path.dirname(__file__))
        # 通过字符串截取方式截取，当前文件相对路径./src/util/StrUtil.py
        return p_path[:p_path.rindex('src')]

    @staticmethod
    def get_project_path_log():
        """
        获取日志路径
        :return: 日志根路径
        """
        path = UtilsPath.get_project_path()
        return os.path.join(path, "log")

    @staticmethod
    def get_database_url():
        root_path = UtilsPath.get_project_path()
        config_path = root_path + "src\\resources\\config.ini"
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8")
        return config.get("database", "url")

    @staticmethod
    def get_onmyoji_image_path():
        project_path = UtilsPath.get_project_path()
        return project_path + "src\\resources\\static\\onmyoji\\"

    @staticmethod
    def get_server():
        root_path = UtilsPath.get_project_path()
        config_path = root_path + "src\\resources\\config.ini"
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8")
        dict1 = {'ip': config.get("server", "ip"), 'port': config.get("server", "port"),
                 'username': config.get("server", "username"), 'password': config.get("server", "password")}
        return dict1

    @staticmethod
    def get_mail():
        root_path = UtilsPath.get_project_path()
        config_path = root_path + "src\\resources\\config.ini"
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8")
        dict1 = {'sender_email': config.get("mail", "sender_email"),
                 'sender_password': config.get("mail", "sender_password"),
                 'recipient_email': config.get("mail", "recipient_email")}
        return dict1

    @staticmethod
    def get_scrcpy_path():
        project_path = UtilsPath.get_project_path()
        return project_path + "src\\resources\\static\\scrcpy\\"

    @staticmethod
    def get_print_image_path(name: str = 'img'):
        # 获取当前时间
        now = imp_datetime.now()
        # 将时间转换为字符串
        time_str = now.strftime("%Y-%m-%d_%H-%M-%S") + "_" + name
        path = os.path.join(UtilsPath.get_project_path_log(), "image")
        img_path = os.path.join(path, time_str) + '.png'
        return img_path

    @staticmethod
    def get_log_image_path():
        path = os.path.join(UtilsPath.get_project_path_log(), "image")
        return path
