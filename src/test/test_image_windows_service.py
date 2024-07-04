# @Time: 2024年01月26日 16:19
# @Author: orcakill
# @File: test_image_windows_service.py
# @Description: TODO
from unittest import TestCase

from src.model.enum import Onmyoji
from src.service.image_service import ImageService
from src.utils.my_logger import my_logger as logger


class ImageWindowsServiceTest(TestCase):
    @staticmethod
    def test_get_current_hwnd():
        """
        获取当前窗口的信息，进程名，类名，句柄
        :return:
        """
        logger.debug(ImageService.get_current_hwnd())
        # ('notepad.exe', '', 'Edit', 264420)

    @staticmethod
    def test_get_all_info():
        """
        获取所有窗口的信息，进程名，类名，句柄
        :return:
        """
        logger.info("1全部句柄及信息")
        result = ImageService.get_all_hwnd_info()
        for r in result:
            logger.debug(r)
        logger.info("2指定标题的句柄及信息")
        result = ImageService.get_all_hwnd_info(title="8ce78c9f")
        for r in result:
            logger.debug(r)
        logger.info("3指定进程的句柄及信息")
        result = ImageService.get_all_hwnd_info(process_name="scrcpy.exe")
        for i in range(len(result)):
            hwnd = result[i][3]
            result_child = ImageService.get_all_hwnd_info(hwnd=hwnd)
            logger.debug(result_child)
            ImageService.windows_screenshot(hwnd, name=str(hwnd), print_image=True)
        logger.info("4指定句柄下属的句柄及信息")
        ImageService.get_child_windows("67766")
        # for i in range(len(result)):
        #     result1 = ImageService.get_all_hwnd_info(hwnd=result[i])
        #     logger.debug(result[i])
        #     logger.debug(result1)
        #     ImageService.screenshot(result[i], name=str(result[i]), print_image=True)

    @staticmethod
    def test_resolution_hwnd():
        ImageService.find_resolution_hwnd(123)

    @staticmethod
    def test_screenshot():
        hwnd = ImageService.find_hwnd("YsPhone.exe", "Qt5QWindowIcon")
        logger.debug(hwnd)
        hwnd2 = ImageService.get_all_hwnd_info(class_name="Qt5QWindowIcon")
        logger.debug(hwnd2)
        ImageService.windows_screenshot(hwnd[0], '测试', True)

    @staticmethod
    def test_exists():
        ImageService.exists_windows(131740, Onmyoji.windows_test1, is_click=True)

    @staticmethod
    def test_get_all_hwnd_info():
        result = ImageService.get_all_hwnd_info(process_name="notepad.exe")
        for i in range(len(result)):
            hwnd = result[i][3]
            result_child = ImageService.get_all_hwnd_info(hwnd=hwnd)
            logger.debug(result_child)
            ImageService.windows_screenshot(hwnd, name=str(hwnd), print_image=True)
