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

# 控制airtest的日志输出
log_airtest = logging.getLogger("airtest")
log_airtest.setLevel(logging.CRITICAL)


class AirtestService:
    @staticmethod
    def auto_setup():
        """
        设备连接
        :return:
        """
        auto_setup(__file__, logdir=False, devices=["android://"])

    @staticmethod
    def snapshot():
        """
        实时截图
        :return: 数组
        """
        return G.DEVICE.snapshot()

    @staticmethod
    def assert_exists(template: Template, cvstrategy: [], timeout: int):
        """
        判断图片是否存在
        :param template: 图片类
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :return:bool
        """
        Settings.CVSTRATEGY = cvstrategy
        if assert_exists(Template=template, timeout=timeout):
            return True
        else:
            return False

    @staticmethod
    def touch(template: Template, cvstrategy: [], timeout: int):
        """
        判断图片是否存在
        :param template: 图片类
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :return:bool
        """
        Settings.CVSTRATEGY = cvstrategy
        if touch(Template=template, timeout=timeout):
            return True
        else:
            return False

    @staticmethod
    def touch_coordinate(v: []):
        """
        点击坐标
        :param v: 坐标
        :return: bool
        """
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
        wait(2)
        start_app(app)
        wait(1)
