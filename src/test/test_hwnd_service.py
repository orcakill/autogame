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
        获取所有窗口的信息，进程名，类名，句柄
        :return:
        """
        logger.info("全部句柄及信息")
        result = HwndService.get_all_hwnd_info()
        for r in result:
            logger.debug(r)
        logger.info("指定标题的句柄及信息")
        result = HwndService.get_all_hwnd_info(title="钉钉")
        for r in result:
            logger.debug(r)
        logger.info("指定进程的句柄及信息")
        result = HwndService.get_all_hwnd_info(process_name="DingTalk.exe")
        for r in result:
            logger.debug(r)
        logger.info("指定句柄下属的句柄及信息")
        result = HwndService.get_child_windows("131674")
        for i in range(len(result)):
            result1 = HwndService.get_all_hwnd_info(hwnd=result[i])
            logger.debug(result[i])
            logger.debug(result1)
            ImageWindowsService.screenshot(result[i], name=str(result[i]), print_image=True)
