# @Time    : 2023年06月16日 09:15
# @Author  : orcakill
# @File    : image_service.py
# @Description : 图像识别接口

from src.model.enum import Cvstrategy
from src.service.airtest_service import AirtestService
from src.service.impl_image_service.impl_exists import ImplExistsTouch
from src.service.impl_image_service.impl_find_all import ImplFindAll
from src.service.impl_image_service.impl_hwnd import ImplHwnd
from src.service.impl_image_service.impl_match import ImplMatch
from src.service.impl_image_service.impl_ocr import ImplOcr

# 图像识别算法
CVSTRATEGY = Cvstrategy.sift
# 单张图片识别时间
TIMEOUT = 0.5
# 图片组识别时间
TIMEOUTS = 5
# 图像识别阈值
THRESHOLD = 0.7
# 图片识别轮次
REC_ROUND = 1
# 图片等待识别时间(秒）·
WAIT = 2
# 图片识别间隔(秒）·
INTERVAL = 1
# 点击次数
TIMES = 1
# 按住时间
DURATION = 0.01

THROW = False


class ImageService:

    @staticmethod
    def exists(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT, timeouts: float = TIMEOUTS,
               threshold: float = THRESHOLD, wait: float = WAIT, interval: float = INTERVAL, is_throw: bool = THROW,
               is_click: bool = False, rgb: bool = False):
        """
        根据文件夹名获取图片进行图像识别，判断图片是否存在
        """
        return ImplExistsTouch.exists(folder_path=folder_path, cvstrategy=cvstrategy, timeout=timeout,
                                      timeouts=timeouts, threshold=threshold, wait=wait, interval=interval,
                                      is_throw=is_throw, is_click=is_click, rgb=rgb)

    @staticmethod
    def touch(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT, timeouts: float = TIMEOUTS,
              threshold: float = THRESHOLD, wait: float = WAIT, is_throw: bool = THROW, times: int = TIMES,
              duration: float = DURATION, rgb: bool = False):
        """
        根据文件夹名获取图片进行图像识别，点击图片
        """
        return ImplExistsTouch.touch(folder_path=folder_path, cvstrategy=cvstrategy, timeout=timeout, timeouts=timeouts,
                                     threshold=threshold, wait=wait, is_throw=is_throw, times=times,
                                     duration=duration, rgb=rgb)

    @staticmethod
    def snapshot(name: str = None, print_image: bool = False):
        """
        设备截图
        """
        return AirtestService.snapshot(name, print_image)

    @staticmethod
    def get_cap_method(device):
        """
        设备截图
        """
        return AirtestService.get_cap_method(device)

    @staticmethod
    def get_check_method(device):
        """
        设备截图
        """
        return AirtestService.check_method(device)

    @staticmethod
    def touch_coordinate(v: [], wait: float = WAIT, duration: float = DURATION):
        """
        点击坐标
        """
        AirtestService.touch_coordinate(v, wait, duration)

    @staticmethod
    def restart_app(app: str):
        """
        重启APP
        """
        AirtestService.adb_restart_app(app)

    @staticmethod
    def stop_app(app: str):
        """
        停止APP
        """
        AirtestService.adb_stop_app(app)

    @staticmethod
    def swipe(v1: [], v2: [], duration: float = 0.5):
        """
        滑动
        """
        AirtestService.swipe(v1, v2, duration)

    @staticmethod
    def crop_image(x1, y1, x2, y2):
        """
        局部截图
        """
        return AirtestService.crop_image(x1, y1, x2, y2)

    @staticmethod
    def resolution_ratio():
        """
        获取分辨率
        """
        return AirtestService.resolution_ratio()

    @staticmethod
    def cv2_2_pil(local):
        """
        转换图片格式 将cv2转换为pil
        """
        return AirtestService.cv2_2_pil(local)

    @staticmethod
    def find_all(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT, timeouts: int = TIMEOUTS,
                 threshold: float = THRESHOLD, wait: float = WAIT, is_throw: bool = THROW,
                 rgb: bool = False):
        """
        多图查找，获取多个坐标
        """
        return ImplFindAll.find_all(folder_path=folder_path, cvstrategy=cvstrategy, timeout=timeout, timeouts=timeouts,
                                    threshold=threshold, wait=wait, is_throw=is_throw, rgb=rgb)

    @staticmethod
    def find_all_num(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT, timeouts: int = TIMEOUTS,
                     threshold: float = THRESHOLD, wait: float = WAIT, is_throw: bool = THROW,
                     rgb: bool = False):
        """
        多图查找，获取多个坐标数量0000
        """
        return ImplFindAll.find_all_num(folder_path=folder_path, cvstrategy=cvstrategy, timeout=timeout,
                                        timeouts=timeouts, threshold=threshold, wait=wait, is_throw=is_throw, rgb=rgb)

    @staticmethod
    def find_all_coordinate(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT,
                            timeouts: int = TIMEOUTS, threshold: float = THRESHOLD, wait: float = WAIT,
                            is_throw: bool = THROW, rgb: bool = False):
        """
        多图查找 只获取坐标
        """
        return ImplFindAll.find_all_coordinate(folder_path=folder_path, cvstrategy=cvstrategy, timeout=timeout,
                                               timeouts=timeouts, threshold=threshold, wait=wait, is_throw=is_throw,
                                               rgb=rgb)

    @staticmethod
    def cv_match(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeouts: int = TIMEOUTS,
                 threshold: float = THRESHOLD, wait: float = WAIT, is_throw: bool = THROW,
                 rgb: bool = False, x1: float = 0, x2: float = 1, y1: float = 0, y2: float = 1):
        """
        计算图片和设备截图的匹配结果，有result 坐标  confidence 相似度 区域范围
        """
        return ImplMatch.cv_match(folder_path=folder_path, cvstrategy=cvstrategy, timeouts=timeouts,
                                  threshold=threshold, wait=wait, is_throw=is_throw, rgb=rgb, x1=x1, x2=x2, y1=y1,
                                  y2=y2)

    @staticmethod
    def match_in(folder_path1: str, folder_path2: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT,
                 timeouts: int = TIMEOUTS, threshold: float = THRESHOLD, wait: float = WAIT,
                 is_throw: bool = THROW, rgb: bool = False):
        """
        根据文件夹名获取图片进行图像识别，判断图片内图片是否存在
        """
        return ImplMatch.match_in(folder_path1=folder_path1, folder_path2=folder_path2, cvstrategy=cvstrategy,
                                  timeout=timeout, timeouts=timeouts, threshold=threshold, wait=wait, is_throw=is_throw,
                                  rgb=rgb)

    @staticmethod
    def text(word: str):
        """
        输入文字
        """
        AirtestService.text(word)

    @staticmethod
    def touch_all_coordinate(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT,
                             timeouts: int = TIMEOUTS, threshold: float = THRESHOLD, wait: float = WAIT,
                             is_throw: bool = THROW, rgb: bool = False, rank: int = 1):
        """
        多图查找点击 获取坐标并点击
        """
        return ImplFindAll.touch_all_coordinate(folder_path=folder_path, cvstrategy=cvstrategy, timeout=timeout,
                                                timeouts=timeouts, threshold=threshold, wait=wait,
                                                is_throw=is_throw, rgb=rgb, rank=rank)

    @staticmethod
    def exists_windows(hwnd, folder_path: str, cvstrategy: [] = CVSTRATEGY, timeouts: float = TIMEOUTS,
                       threshold: float = THRESHOLD, wait: float = WAIT, interval: float = INTERVAL,
                       is_throw: bool = THROW, is_click: bool = False, rgb: bool = False, x1: float = 0, x2: float = 1,
                       y1: float = 0, y2: float = 1):
        """
        windows 根据文件夹名获取图片进行图像识别，判断图片是否存在
        """
        return ImplHwnd.exists_windows(hwnd, folder_path=folder_path, cvstrategy=cvstrategy, timeouts=timeouts,
                                       threshold=threshold, wait=wait, interval=interval, is_throw=is_throw,
                                       is_click=is_click, rgb=rgb, x1=x1, x2=x2, y1=y1, y2=y2)

    @staticmethod
    def touch_windows(hwnd, folder_path: str, cvstrategy: [] = CVSTRATEGY, timeouts: float = TIMEOUTS,
                      threshold: float = THRESHOLD, wait: float = WAIT, interval: float = INTERVAL,
                      is_throw: bool = THROW, is_click: bool = True, rgb: bool = False, x1: float = 0, x2: float = 1,
                      y1: float = 0, y2: float = 1):
        """
        windows 根据文件夹名获取图片进行图像识别，判断图片是否存在
        """
        return ImplHwnd.exists_windows(hwnd, folder_path=folder_path, cvstrategy=cvstrategy, timeouts=timeouts,
                                       threshold=threshold, wait=wait, interval=interval, is_throw=is_throw,
                                       is_click=is_click, rgb=rgb, x1=x1, x2=x2, y1=y1, y2=y2)

    @staticmethod
    def find_hwnd(process_name, class_name):
        """
        windows 根据进程名、类名获取句柄
        """
        return ImplHwnd.find_hwnd(process_name, class_name)

    @staticmethod
    def get_current_hwnd():
        """
        windows 获取当前句柄等信息
        """
        return ImplHwnd.get_current_hwnd()

    @staticmethod
    def get_all_hwnd_info(process_name=None, title=None, class_name=None, hwnd=None):
        """
        windows 获取全部句柄等信息
        """
        return ImplHwnd.get_all_hwnd_info(process_name, title, class_name, hwnd)

    @staticmethod
    def windows_screenshot(hwnd: int, name: str = None, print_image: bool = False, x1: float = 0, x2: float = 1,
                           y1: float = 0, y2: float = 1):
        """
        windows  设备截图，根据截图比例确定位置
        """
        return ImplHwnd.windows_screenshot(hwnd, name, print_image, x1, x2, y1, y2)

    @staticmethod
    def get_child_windows(parent_window_hwnd):
        """
        # 遍历窗口句柄的所有子窗口
        """
        return ImplHwnd.get_child_windows(parent_window_hwnd)

    @staticmethod
    def find_resolution_hwnd(hwnd: int):
        """
        获取句柄的分辨率
        """
        return ImplHwnd.find_resolution_hwnd(hwnd)

    @staticmethod
    def draw_rectangle(screen, x1, y1, x2, y2):
        """
        在图上画框，确定识别准确率
        """
        return AirtestService.draw_rectangle(screen, x1, y1, x2, y2)

    @staticmethod
    def ocr_touch(word):
        """
        在图上画框，确定识别准确率
        """
        return ImplOcr.ocr_touch(word)

    @staticmethod
    def get_adb_resolution(device_address):
        """
        获取安卓设备分辨率
        """
        return AirtestService.get_adb_resolution(device_address)
