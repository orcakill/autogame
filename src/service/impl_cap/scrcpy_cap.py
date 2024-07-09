# @Time: 2024年07月09日 10:57
# @Author: orcakill
# @File: scrcpy_cap.py
# @Description: 通过scrcpy截图
from airtest.core.android import Android
from airtest.core.android.cap_methods.base_cap import BaseCap

from src.service.impl_image_service.impl_hwnd import ImplHwnd


class ScrcpyCap(BaseCap):

    def __init__(self, adb, *args, **kwargs):
        super(ScrcpyCap, self).__init__(adb=adb)
        self.adb = adb

    def get_frame_from_stream(self):
        serialno = self.adb.serialno
        scrcpy_hwnd_info = ImplHwnd.get_all_hwnd_info(title=serialno)
        scrcpy_hwnd_tuple = scrcpy_hwnd_info[0]
        scrcpy_hwnd = scrcpy_hwnd_tuple[-1]
        screen = ImplHwnd.windows_screenshot(scrcpy_hwnd)
        return screen
