# @Time: 2024年02月28日 11:26
# @Author: orcakill
# @File: test_hwnd_service.py
# @Description: TODO
from unittest import TestCase

from src.service.hwnd_service import HwndService
from src.service.image_windows_service import ImageWindowsService
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
        # ('notepad.exe', '', 'Edit', 264420)

    @staticmethod
    def test_get_all_hwnd_info():
        """
        获取当前窗口的信息，进程名，类名，句柄
        :return:
        """
        result=HwndService.get_all_hwnd_info()
        for r in result:
            logger.debug(r)

    @staticmethod
    def test_screen():
        """
        获取当前窗口的信息，进程名，类名，句柄
        :return:
        """
        ImageWindowsService.screenshot(windows_title="",hwnd="264420")


    @staticmethod
    def test_get_hwnd_class_name():
        class_name = HwndService.get_hwnd_class_name(133388)
        logger.debug(class_name)

    @staticmethod
    def test_find_hwnd():
        hwnd= HwndService.find_hwnd("Edit")
        logger.debug(hwnd)
