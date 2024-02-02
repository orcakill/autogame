# @Time: 2024年01月26日 16:19
# @Author: orcakill
# @File: test_image_windows_service.py
# @Description: TODO
from unittest import TestCase

from src.model.enum import Onmyoji, Cvstrategy
from src.service.image_windows_service import ImageWindowsService


class ImageWindowsServiceTest(TestCase):

    # 根据程序名获取句柄
    @staticmethod
    def test_find_window_handles_by_exe():
        ImageWindowsService.find_window_handles_by_exe("D:\DingDing\main\current\DingTalk.exe")

    @staticmethod
    def test_resolution_hwnd():
        ImageWindowsService.resolution_hwnd("钉钉")

    @staticmethod
    def test_screenshot():
        ImageWindowsService.screenshot("钉钉")

    @staticmethod
    def test_mouser_click():
        ImageWindowsService.mouse_click("钉钉", (182, 174))

    @staticmethod
    def test_mouse_position():
        ImageWindowsService.mouse_position()
    @staticmethod
    def test_exists():
        ImageWindowsService.exists("钉钉", Onmyoji.windows_test1, is_click=True)
