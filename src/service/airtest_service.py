"""
# @Time    : 2023年06月13日19:24
# @Author  : orcakill
# @File    : airtest_service.py
# @Description : airtest接口
"""
from airtest.aircv import cv2_2_pil
from airtest.core.api import auto_setup, exists
from airtest.core.helper import G
import logging

# 控制airtest的日志输出
log_airtest = logging.getLogger("airtest")
log_airtest.setLevel(logging.CRITICAL)


class AirtestService():
    @staticmethod
    def auto_setup():
        """
        设备连接
        :return:
        """
        auto_setup(__file__, logdir=False, devices=["android://"])

    @staticmethod
    def snapshot():
        screen1 = G.DEVICE.snapshot()
        pil_img = cv2_2_pil(screen1)
        pil_img.save(r"D:/test.png", quality=99, optimize=True)

    @staticmethod
    def exist():
        return exists()
