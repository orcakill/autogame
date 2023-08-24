"""
# @Time: 2023年06月13日19:24
# @Author: orcakill
# @File: airtest_service.py
# @Description: airtest接口
"""
import logging
from datetime import datetime as imp_datetime

from airtest import aircv
from airtest.aircv import cv2_2_pil
from airtest.core.api import *
from airtest.core.helper import G
from airtest.core.settings import Settings

from src.utils.my_logger import my_logger as logger

# 控制airtest的日志输出
log_airtest = logging.getLogger("airtest")
log_airtest.setLevel(logging.CRITICAL)

# 图片点击识别等待时间(秒）·
WAIT = 2


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
    def snapshot(name:str,print_image: bool = False):
        """
        这个函数是用来实时截图的。它调用了G.DEVICE的snapshot()方法来获取截图，并将结果以数组的形式返回。
        :return: 数组
        """
        screen = G.DEVICE.snapshot()
        if print_image:
            pil_image = cv2_2_pil(screen)
            # 获取当前时间
            now = imp_datetime.now()
            # 将时间转换为字符串
            time_str = now.strftime("%Y-%m-%d-%H-%M-%S")+"_"+name
            pil_image.save("D:/image/" + time_str + ".png", quality=99, optimize=True)
        return screen

    @staticmethod
    def exists(template: Template, cvstrategy: [], timeout: float, is_throw: bool):
        """
        判断图片是否存在并返回坐标
        :param template: 图片类
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param is_throw: 是否显示异常
        :return: bool
        """
        Settings.CVSTRATEGY = cvstrategy
        Settings.FIND_TIMEOUT_TMP = timeout
        try:
            return exists(template)
        except Exception as e:
            if is_throw:
                logger.debug("异常：{}", e)

    @staticmethod
    def touch(template: Template, cvstrategy: [], timeout: float, is_throw: bool, times: int,
              duration: float):
        """
        判断图片是否存在
        :param times: 点击次数
        :param duration: 按住时间
        :param template: 图片类
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param is_throw: 是否显示异常
        :return: bool
        """
        Settings.CVSTRATEGY = cvstrategy
        Settings.FIND_TIMEOUT = timeout
        try:
            if touch(template, times=times, duration=duration):
                return True
            else:
                return False
        except Exception as e:
            if is_throw:
                logger.debug("异常：{}", e)

    @staticmethod
    def touch_coordinate(v: [], wait_time: float = WAIT):
        time.sleep(wait_time)
        if touch(v):
            logger.debug("坐标点击成功")
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

    @staticmethod
    def crop_image(x1, y1, x2, y2):
        screen = G.DEVICE.snapshot()
        # 局部截图
        local_screen = aircv.crop_image(screen, (x1, y1, x2, y2))
        return local_screen

    @staticmethod
    def resolving_power():
        if G.DEVICE.display_info['orientation'] in [1, 3]:
            height = G.DEVICE.display_info['width']
            width = G.DEVICE.display_info['height']
        else:
            height = G.DEVICE.display_info['height']
            width = G.DEVICE.display_info['width']
        return width, height

    @staticmethod
    def cv2_2_pil(local):
        return cv2_2_pil(local)
