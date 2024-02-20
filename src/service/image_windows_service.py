# @Time: 2024年01月26日 14:38
# @Author: orcakill
# @File: image_windows_service.py
# @Description: 图像识别，根据win32实现
import ctypes
import time

import cv2
import imageio
import numpy as np
import psutil
import win32api
import win32con
import win32gui
import win32process
import win32ui

from src.model.enum import Cvstrategy
from src.service.airtest_service import AirtestService
from src.service.image_service import ImageService
from src.utils.my_logger import my_logger as logger

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

THROW = True


class ImageWindowsService:

    @staticmethod
    def exists(windows_title: str, folder_path: str, cvstrategy: [] = CVSTRATEGY, timeouts: float = TIMEOUTS,
               threshold: float = THRESHOLD, wait: float = WAIT, interval: float = INTERVAL, is_throw: bool = THROW,
               is_click: bool = False, rgb: bool = False, x1: float = 0, x2: float = 1, y1: float = 0, y2: float = 1):
        """
        根据文件夹名获取图片进行图像识别，判断图片是否存在

        :param windows_title: 窗口标题
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param threshold: 图像识别阈值
        :param interval: 图片识别点击间隔时间
        :param rgb: 带颜色
        :param timeouts: 图片组超时时间
        :param wait: 图片等待识别时间
        :param is_click: 是否点击坐标
        :param is_throw: 是否显示异常
        :param y2: y2坐标比例
        :param x2: x2坐标比例
        :param y1: y1坐标比例
        :param x1: x1坐标比例
        :return:
        """
        try:
            time.sleep(wait)
            resolution = ImageWindowsService.resolution_hwnd(windows_title)
            template_list = ImageService.get_template_list(folder_path, rgb, threshold)
            time_start = time.time()
            while time.time() - time_start < timeouts:
                for template in template_list:
                    # 设备截图
                    image1 = ImageWindowsService.screenshot(windows_title, x1, x2, y1, y2)
                    match = AirtestService.cv_match(template, image1, cvstrategy)
                    if match:
                        pos = match['result']
                        if pos and pos is not None:
                            # 根据截取的比例，修正坐标
                            if (x1, y1, x2, y2) not in [0, 1, 0, 1]:
                                pos = (pos[0] + resolution[0] * x1, pos[1] + resolution[1] * y1)
                            if not is_click:
                                if is_throw:
                                    logger.debug("图像识别成功:{},{}", folder_path, template.filename)
                                else:
                                    logger.debug("图像识别成功:{}", folder_path)
                                return pos
                            if is_click:
                                time.sleep(interval)
                                re1 = match['rectangle'][0]
                                re2 = match['rectangle'][2]
                                logger.debug(pos)
                                ImageWindowsService.draw_rectangle(image1, re1[0], re1[1], re2[0], re2[1])
                                # 点击指定坐标
                                ImageWindowsService.mouse_click(windows_title, pos)
                                logger.debug("图像识别点击成功:{}", folder_path)
                                return True
            return False
        except Exception as e:
            if is_throw:
                logger.exception(e)
            else:
                pass
        return False

    @staticmethod
    def screenshot(windows_title: str, x1: float = 0, x2: float = 1, y1: float = 0, y2: float = 1):
        """
        设备截图，根据截图比例确定位置
        :param windows_title:
        :param x1:
        :param x2:
        :param y1:
        :param y2:
        :return:
        """
        # 获取窗口句柄
        hwnd = win32gui.FindWindow(None, windows_title)
        if hwnd:
            # 判断窗口是否最大化
            if not win32gui.IsIconic(hwnd):
                # 将窗口最大化
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                time.sleep(0.5)
            # 获取窗口位置和大小
            rect = win32gui.GetWindowRect(hwnd)
            x, y, w, h = rect
            if w >= 0 and h >= 0:
                # 创建一个与窗口大小相同的设备上下文
                hdc = win32gui.GetWindowDC(hwnd)
                dc_obj = win32ui.CreateDCFromHandle(hdc)
                mem_dc = dc_obj.CreateCompatibleDC()
                # 创建一个位图对象
                bitmap = win32ui.CreateBitmap()
                bitmap.CreateCompatibleBitmap(dc_obj, w, h)
                mem_dc.SelectObject(bitmap)
                # 将窗口内容绘制到位图上
                mem_dc.BitBlt((0, 0), (w, h), dc_obj, (0, 0), win32con.SRCCOPY)
                # 将位图保存为文件
                # bitmap.SaveBitmapFile(memDC, "D://screenshot.png")

                # bitmap转换ndarray
                signed_ints_array = bitmap.GetBitmapBits(True)
                ndarray_image = np.fromstring(signed_ints_array, dtype='uint8')
                ndarray_image.shape = (h, w, 4)
                ndarray_image = cv2.cvtColor(ndarray_image, cv2.COLOR_BGRA2RGB)
                # 释放位图资源
                win32gui.DeleteObject(bitmap.GetHandle())
                mem_dc.DeleteDC()
                dc_obj.DeleteDC()
                win32gui.ReleaseDC(hwnd, hdc)

                # 保存图片到磁盘
                imageio.imsave("D://screenshot2.png", ndarray_image)

                coordinate1 = (int(w * x1), int(h * y1))
                coordinate2 = (int(w * x2), int(h * y2))

                # 截取图片
                # cropped_image = ndarray_image[0:525,960:1920]
                cropped_image = ndarray_image[coordinate1[1]:coordinate2[1], coordinate1[0]:coordinate2[0]]

                # 保存图片到磁盘
                imageio.imsave("D://screenshot3.png", cropped_image)

                return cropped_image
            else:
                logger.debug("句柄宽高获取异常")
        else:
            logger.debug("未找到窗口句柄")

    @staticmethod
    def resolution_hwnd(windows_title: str):
        # 获取窗口句柄
        hwnd = win32gui.FindWindow(None, windows_title)
        # 判断窗口是否最大化
        if not win32gui.IsIconic(hwnd):
            # 将窗口最大化
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            time.sleep(0.5)
        # 获取窗口位置和大小
        rect = win32gui.GetWindowRect(hwnd)
        x, y, w, h = rect
        resolution = (w, h)
        return resolution

    @staticmethod
    def draw_rectangle(screen, x1, y1, x2, y2):
        """
        画图，根据指定范围的坐标在原图上画框
        :param screen:
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :return:
        """
        cv2.rectangle(screen, (x1, y1), (x2, y2), (0, 0, 255), 2)
        # 保存图片到本地磁盘
        imageio.imsave("D://draw.png", screen)

    @staticmethod
    def mouse_click(window_title: str, pos, hwnd=None):
        """
        鼠标点击，滑动
        :param window_title:
        :param pos:
        :param hwnd:
        :return:
        """
        x = pos[0]
        y = pos[1]
        # 检查句柄是否为空，为空则根据窗口标题获取句柄
        if window_title is not None and hwnd is None:
            hwnd = win32gui.FindWindow(None, window_title)
        if not hwnd:
            raise Exception("找不到窗口")
        lparam = win32api.MAKELONG(x, y)
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, win32con.WM_LBUTTONUP, lparam)
        logger.debug("点击成功")

    @staticmethod
    def is_win32_api_blocked(window_title: str, hwnd=None):
        """
        检查是否屏蔽win32的api
        :param hwnd: 句柄
        :return:
        """
        kernel32 = ctypes.windll.kernel32
        process_handle = kernel32.GetProcessHandleFromThread(ctypes.pointer(ctypes.c_void_p(hwnd)))
        if process_handle == 0:
            return True
        else:
            logger.debug("进程屏蔽了win32 api")
            return False

    @staticmethod
    def get_windows():
        windows1 = []
        win32gui.EnumWindows(lambda hwnd1, param: param.append(hwnd1), windows1)
        return windows1

    @staticmethod
    def get_window_info(hwnd):
        try:
            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process_name = psutil.Process(pid).name()
            return process_name, title, class_name, hwnd
        except Exception as e:
            logger.debug(f"获取windows窗口异常: {e}")
            return None

    @staticmethod
    def get_window_info_by_filter(filter_value, filter_type=None):
        windows = ImageWindowsService.get_windows()
        result = []
        for hwnd in windows:
            window_info = ImageWindowsService.get_window_info(hwnd)
            if window_info:
                process_name, title, class_name, hwnd = window_info
                if filter_type is None or filter_value is None:
                    result.append((process_name, title, class_name, hwnd))
                #     进程名
                elif filter_type == "process_name" and process_name == filter_value:
                    result.append((process_name, title, class_name, hwnd))
                #     窗口标题
                elif filter_type == "window_title" and title == filter_value:
                    result.append((process_name, title, class_name, hwnd))
                #     类名
                elif filter_type == "class_name" and class_name == filter_value:
                    result.append((process_name, title, class_name, hwnd))
                #     句柄
                elif filter_type == "hwnd" and hwnd == int(filter_value):
                    result.append((process_name, title, class_name, hwnd))
        return result


if __name__ == "__main__":
    # 示例：获取所有窗口的信息
    all_windows_info = ImageWindowsService.get_window_info_by_filter(None)
    for info in all_windows_info:
        print(f"进程名: {info[0]}, 窗口标题: {info[1]}, 类名: {info[2]}, 句柄: {info[3]}")

    # 示例：获取指定进程名为"chrome.exe"的窗口信息
    chrome_windows_info = ImageWindowsService.get_window_info_by_filter("chrome.exe", "process_name")
    for info in chrome_windows_info:
        print(f"进程名: {info[0]}, 窗口标题: {info[1]}, 类名: {info[2]}, 句柄: {info[3]}")

    # 示例：获取指定窗口标题为"Notepad"的窗口信息
    notepad_windows_info = ImageWindowsService.get_window_info_by_filter("Notepad", "window_title")
    for info in notepad_windows_info:
        print(f"进程名: {info[0]}, 窗口标题: {info[1]}, 类名: {info[2]}, 句柄: {info[3]}")

    # 示例：获取指定类名为"ConsoleWindowClass"的窗口信息
    console_windows_info = ImageWindowsService.get_window_info_by_filter("ConsoleWindowClass", "class_name")
    for info in console_windows_info:
        print(f"进程名: {info[0]}, 窗口标题: {info[1]}, 类名: {info[2]}, 句柄: {info[3]}")

    # 示例：获取指定句柄为10000的窗口信息
    hwnd_10000_info = ImageWindowsService.get_window_info_by_filter("10000", "hwnd")
    for info in hwnd_10000_info:
        print(f"进程名: {info[0]}, 窗口标题: {info[1]}, 类名: {info[2]}, 句柄: {info[3]}")
