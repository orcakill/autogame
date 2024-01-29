# @Time: 2024年01月26日 14:38
# @Author: orcakill
# @File: image_windows_service.py
# @Description: 图像识别，根据win32实现
import numpy as np
import win32con
import win32gui
import win32ui
import time

from src.model.enum import Cvstrategy
from src.service.airtest_service import AirtestService
from src.service.image_service import ImageService
from src.utils.my_logger import my_logger as logger
from PIL import Image

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
                    image1 = ImageWindowsService.screenshot(windows_title, x1 * resolution[0], y1 * resolution[1],
                                                            x2 * resolution[0],
                                                            y2 * resolution[1])
                    pos = AirtestService.cv_match(template, image1, cvstrategy)
                    if pos:
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
                            logger.debug("图像识别点击成功:{}", folder_path)
                            ImageService.touch_coordinate(pos)
                            return True
            return False
        except Exception as e:
            if is_throw:
                logger.exception("异常：{}", e)
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
        # 判断窗口是否最大化
        if not win32gui.IsIconic(hwnd):
            # 将窗口最大化
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            time.sleep(0.5)
        # 获取窗口位置和大小
        rect = win32gui.GetWindowRect(hwnd)
        x, y, w, h = rect
        # 创建一个与窗口大小相同的设备上下文
        hdc = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(hdc)
        memDC = dcObj.CreateCompatibleDC()
        # 创建一个位图对象
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(dcObj, w, h)
        memDC.SelectObject(bitmap)
        # 将窗口内容绘制到位图上
        memDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)
        # 将位图保存为文件
        bitmap.SaveBitmapFile(memDC, "D://screenshot.png")
        # 释放资源
        win32gui.DeleteObject(bitmap.GetHandle())
        memDC.DeleteDC()
        dcObj.DeleteDC()
        win32gui.ReleaseDC(hwnd, hdc)
        # 将位图转换为ndarray格式
        image_array = np.array(bitmap)
        # # 获取image_array的宽度和高度
        # width = image_array.shape[1]
        # height = image_array.shape[0]
        # # 根据四个点的坐标实现局部截图
        # cropped_image_array = image_array[width * x1:height * y1, width * x2:height * y2]
        # 将ndarray格式的图片转换为PIL Image对象
        image = Image.fromarray(image_array)
        # 保存图片到磁盘
        image.save("D://screenshot1.png")
        return image_array

    @staticmethod
    def resolution_hwnd(windows_title: str):
        # 获取窗口句柄
        hwnd = win32gui.FindWindow(None, windows_title)
        # 获取客户区域的大小
        client_rect = win32gui.GetClientRect(hwnd)
        t = (client_rect[2], client_rect[3])
        return t
