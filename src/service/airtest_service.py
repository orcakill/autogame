"""
# @Time    : 2023年06月13日19:24
# @Author  : orcakill
# @File    : airtest_service.py
# @Description : airtest接口
"""
import logging
from airtest.core.api import *
from airtest.core.helper import G
from airtest.core.settings import Settings
from src.utils.my_logger import my_logger as logger

# 控制airtest的日志输出
log_airtest = logging.getLogger("airtest")
log_airtest.setLevel(logging.CRITICAL)


class AirtestService:
    @staticmethod
    def auto_setup(game_device: str):
        """
        设备连接
        :return:
        """
        if game_device == "0":
            auto_setup(__file__, logdir=False, devices=["android://"])
        if game_device == "1":
            auto_setup(__file__, logdir=False, devices=["Android://127.0.0.1:5037/127.0.0.1:62001"])

    @staticmethod
    def snapshot():
        """
        这个函数是用来实时截图的。它调用了G.DEVICE的snapshot()方法来获取截图，并将结果以数组的形式返回。
        :return: 数组
        """
        return G.DEVICE.snapshot()

    @staticmethod
    def exists(template: Template, cvstrategy: [], timeout: int, threshold: float):
        """
        判断图片是否存在
        :param template: 图片类
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param threshold: 图像识别阈值
        :return: bool
        """
        Settings.CVSTRATEGY = cvstrategy
        Settings.FIND_TIMEOUT = timeout
        Settings.THRESHOLD = threshold
        try:
            if exists(template):
                return True
            else:
                return False
        except Exception as e:
            logger.debug("异常：{}", e)

    @staticmethod
    def exists_coordinate(template: Template, cvstrategy: [], timeout: int, threshold: float):
        """
        判断图片是否存在并返回坐标
        :param template: 图片类
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param threshold: 图像识别阈值
        :return: bool
        """
        Settings.CVSTRATEGY = cvstrategy
        Settings.FIND_TIMEOUT = timeout
        Settings.THRESHOLD = threshold
        try:
            return exists(template)
        except Exception as e:
            logger.debug("异常：{}", e)

    @staticmethod
    def touch(template: Template, cvstrategy: [], timeout: int, threshold: float):
        """
        判断图片是否存在
        :param template: 图片类
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param threshold: 图像识别阈值
        :return: bool
        """
        Settings.CVSTRATEGY = cvstrategy
        Settings.FIND_TIMEOUT = timeout
        Settings.THRESHOLD = threshold
        try:
            if touch(template):
                return True
            else:
                return False
        except Exception as e:
            logger.debug("异常：{}", e)

    @staticmethod
    def touch_coordinate(v: []):
        if touch(v):
            return True
        else:
            return False

    @staticmethod
    def restart_app(app: str):
        """
        重启APP
        :param app: app的包名
        :return: 无
        """
        stop_app(app)
        time.sleep(2)
        start_app(app)
        time.sleep(1)

    @staticmethod
    def swipe(v1: [], v2: []):
        """
        重启APP
        :param v1: 图片1
        :param v2: 图片2
        :return: 无
        """
        if swipe(v1, v2):
            return True
        else:
            return False
