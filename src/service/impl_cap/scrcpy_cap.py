# @Time: 2024年07月09日 10:57
# @Author: orcakill
# @File: scrcpy_cap.py
# @Description: 通过scrcpy截图
import cv2
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
        ndarray_image = ImplHwnd.windows_screenshot(hwnd=scrcpy_hwnd)
        bgr_image = cv2.cvtColor(ndarray_image, cv2.COLOR_RGB2BGR)
        return bgr_image

    def snapshot(self, ensure_orientation=True, *args, **kwargs):
        """
        Take a screenshot and convert it into a cv2 image object

        获取一张屏幕截图，并转化成cv2的图像对象

        Returns: numpy.ndarray

        """
        ndarray_image = self.get_frame_from_stream()
        return ndarray_image
