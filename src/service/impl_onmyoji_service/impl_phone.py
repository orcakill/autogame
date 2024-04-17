# @Time: 2024年04月16日 14:48
# @Author: orcakill
# @File: impl_phone.py
# @Description: 云手机自动登录连接
from src.model.enum import Onmyoji, WinProcessName, WinClassName
from src.service.image_service import ImageService


class ImplPhone:

    @staticmethod
    def phone_login(game_device: str):
        """
        云手机登录
        :param game_device:
        :return:
        """
        # # 获取云手机句柄
        hwnd = ImageService.find_hwnd(WinProcessName.phone_exe, WinClassName.phone_home)
        # 登录，或者根据设备号登录云手机
        ImageService.exists_windows(hwnd, Onmyoji.phone_DL)
        # 连接adb
        # 同意连接
