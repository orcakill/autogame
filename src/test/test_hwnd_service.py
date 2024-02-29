# @Time: 2024年02月28日 11:26
# @Author: orcakill
# @File: test_hwnd_service.py
# @Description: TODO
from unittest import TestCase

from src.service.hwnd_service import HwndService
from src.utils.my_logger import my_logger as logger


# 1.获取当前窗口的信息，进程名，类名，句柄 test_get_current_hwnd()
# 2、根据句柄获取当前窗口的类名
class TestHwndService(TestCase):
    # 1.获取当前窗口的信息，进程名，类名，句柄
    @staticmethod
    def test_get_current_hwnd():
        """
        获取当前窗口的信息，进程名，类名，句柄
        :return:
        """
        HwndService.get_current_hwnd()

    @staticmethod
    def test_get_hwnd_class_name():
        class_name = HwndService.get_hwnd_class_name(133388)
        logger.debug(class_name)

    @staticmethod
    def test_find_hwnd():
        hwnd= HwndService.find_hwnd("Edit")
        logger.debug(hwnd)
