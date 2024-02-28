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
        HwndService.get_current_hwnd()

    @staticmethod
    def test_get_hwnd_class_name():
        hwnd=0
        class_name=HwndService.get_hwnd_class_name(198902)
        logger.debug(class_name)