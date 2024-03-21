# @Time: 2024年01月26日 16:19
# @Author: orcakill
# @File: test_image_windows_service.py
# @Description: TODO
from unittest import TestCase

from src.model.enum import Onmyoji
from src.service.image_windows_service import ImageWindowsService
from src.utils.my_logger import my_logger as logger


class ImageWindowsServiceTest(TestCase):
    @staticmethod
    def test_get_current_hwnd():
        """
        获取当前窗口的信息，进程名，类名，句柄
        :return:
        """
        ImageWindowsService.get_current_hwnd()
        # ('notepad.exe', '', 'Edit', 264420)

    @staticmethod
    def test_get_all_info():
        """
        获取所有窗口的信息，进程名，类名，句柄
        :return:
        """
        logger.info("全部句柄及信息")
        result = ImageWindowsService.get_all_hwnd_info()
        for r in result:
            logger.debug(r)
        logger.info("指定标题的句柄及信息")
        result = ImageWindowsService.get_all_hwnd_info(title="云帅云手机")
        for r in result:
            logger.debug(r)
        logger.info("指定进程的句柄及信息")
        result = ImageWindowsService.get_all_hwnd_info(process_name="YsConsole.exe")
        for i in range(len(result)):
            hwnd=result[i][3]
            result1 = ImageWindowsService.get_all_hwnd_info(hwnd=hwnd)
            logger.debug(result[i])
            logger.debug(result1)
            ImageWindowsService.windows_screenshot(hwnd, name=str(hwnd), print_image=True)
        logger.info("指定句柄下属的句柄及信息")
        result = ImageWindowsService.get_child_windows("264916")
        # for i in range(len(result)):
        #     result1 = ImageWindowsService.get_all_hwnd_info(hwnd=result[i])
        #     logger.debug(result[i])
        #     logger.debug(result1)
        #     ImageWindowsService.screenshot(result[i], name=str(result[i]), print_image=True)

    @staticmethod
    def test_resolution_hwnd():
        ImageWindowsService.resolution_hwnd(123)

    @staticmethod
    def test_screenshot():
        hwnd = ImageWindowsService.find_hwnd("Qt5QWindowIcon")
        logger.debug(hwnd)
        hwnd2=ImageWindowsService.get_all_hwnd_info(class_name="Qt5QWindowIcon")
        logger.debug(hwnd2)
        ImageWindowsService.windows_screenshot(hwnd[0], '测试', True)

    @staticmethod
    def test_exists():
        ImageWindowsService.exists(131740, Onmyoji.windows_test1, is_click=True)
