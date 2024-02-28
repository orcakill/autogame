# @Time: 2024年01月26日 16:19
# @Author: orcakill
# @File: test_image_windows_service.py
# @Description: TODO
from unittest import TestCase

from src.model.enum import Onmyoji
from src.service.image_windows_service import ImageWindowsService
from src.utils.my_logger import logger


class ImageWindowsServiceTest(TestCase):

    @staticmethod
    def test_resolution_hwnd():
        ImageWindowsService.resolution_hwnd("钉钉")

    @staticmethod
    def test_screenshot():
        ImageWindowsService.screenshot("钉钉")