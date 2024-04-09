# @Time    : 2023年06月16日 09:15
# @Author  : orcakill
# @File    : image_service.py
# @Description : 图像识别接口

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
from src.service.impl_image_service.impl_exists import ImplExistsTouch
from src.service.impl_image_service.impl_find import ImplFind
from src.service.impl_image_service.impl_match import ImplMatch
from src.service.mouse_service import MouseService
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
        AirtestService.restart_app(app)

    @staticmethod
    def stop_app(app: str):
        """
        停止APP
        """
        AirtestService.stop_app(app)

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
        :param rgb: 带颜色
        :param timeouts: 图片组超时时间
        :param wait: 图片等待识别时间
        :param is_throw: 是否显示异常
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 单张图片超时时间
        :param threshold: 图像识别阈值
        :return:
        """
        return ImplFind.find_all(folder_path=folder_path, cvstrategy=cvstrategy, timeout=timeout, timeouts=timeouts,
                                 threshold=threshold, wait=wait, is_throw=is_throw, rgb=rgb)

    @staticmethod
    def find_all_coordinate(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT,
                            timeouts: int = TIMEOUTS, threshold: float = THRESHOLD, wait: float = WAIT,
                            is_throw: bool = THROW, rgb: bool = False):
        """
        多图查找 只获取坐标
        :param rgb: 带颜色
        :param timeouts: 图片组超时时间
        :param wait: 图片等待识别时间
        :param is_throw: 是否显示异常
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 单张图片超时时间
        :param threshold: 图像识别阈值
        :return:
        """
        return ImplFind.find_all_coordinate(folder_path=folder_path, cvstrategy=cvstrategy, timeout=timeout,
                                            timeouts=timeouts, threshold=threshold, wait=wait, is_throw=is_throw,
                                            rgb=rgb)

    @staticmethod
    def cv_match(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeouts: int = TIMEOUTS,
                 threshold: float = THRESHOLD, wait: float = WAIT, is_throw: bool = THROW,
                 rgb: bool = False, x1: float = 0, x2: float = 1, y1: float = 0, y2: float = 1):
        """
        计算图片和设备截图的匹配结果，有result 坐标  confidence 相似度 区域范围
         :param cvstrategy: 图像识别算法
        :param y2: y2坐标比例
        :param x2: x2坐标比例
        :param y1: y1坐标比例
        :param x1: x1坐标比例
        :param rgb: 带颜色
        :param timeouts: 图片组超时时间
        :param wait: 图片等待识别时间
        :param is_throw: 是否显示异常
        :param folder_path: 图片文件夹路径
        :param threshold: 图像识别阈值
        :return:
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
        :param rgb: 带颜色
        :param timeouts: 图片组超时时间
        :param wait: 图片等待识别时间
        :param is_throw: 是否显示异常
        :param folder_path1: 图片文件夹路径1 局部图
        :param folder_path2: 图片文件夹路径2 局部图内图片
        :param cvstrategy: 图像识别算法
        :param timeout: 单张图片超时时间
        :param threshold: 图像识别阈值
        :return:
        """
        try:
            time.sleep(wait)
            result = ImageService.cv_match(folder_path1)
            if result:
                result_xy1 = result['rectangle'][0]
                result_xy2 = result['rectangle'][1]
                result_screen = ImageService.crop_image(result_xy1[0], result_xy1[1], result_xy2[0], result_xy2[1])
                template_list = AirtestService.get_template_list(folder_path2, rgb, threshold)
                time_start = time.time()
                while time.time() - time_start < timeouts:
                    for template in template_list:
                        pos = AirtestService.match_in(template, result_screen, cvstrategy, timeout, is_throw)
                        if pos:
                            if is_throw:
                                logger.debug("局部图内图像识别成功:{},{}", folder_path2, template.filename)
                            else:
                                logger.debug("局部图内图像识别成功:{}", folder_path2)
                            return pos
            return False
        except Exception as e:
            if is_throw:
                logger.exception("异常：{}", e)
            else:
                pass
        return False

    @staticmethod
    def text(word: str):
        """
        文字
        :param word: 文字内容
        :return:
        """
        AirtestService.text(word)

    @staticmethod
    def touch_all_coordinate(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT,
                             timeouts: int = TIMEOUTS, threshold: float = THRESHOLD, wait: float = WAIT,
                             is_throw: bool = THROW, rgb: bool = False, rank: int = 1):
        """
        多图查找 只获取坐标
        :param rank: 点击第几个
        :param rgb: 带颜色
        :param timeouts: 图片组超时时间
        :param wait: 图片等待识别时间
        :param is_throw: 是否显示异常
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 单张图片超时时间
        :param threshold: 图像识别阈值
        :return:
        """
        try:
            time.sleep(wait)
            template_list = AirtestService.get_template_list(folder_path, rgb, threshold)
            time_start = time.time()
            while time.time() - time_start < timeouts:
                for template in template_list:
                    pos = AirtestService.find_all(template, cvstrategy, timeout, is_throw)
                    if pos and len(pos) >= rank - 1:
                        coordinate = pos[rank - 1]['result']
                        logger.debug("图像查找点击成功:{},坐标{}", folder_path, coordinate)
                        ImageService.touch_coordinate(coordinate)
                        return coordinate
            return False
        except Exception as e:
            if is_throw:
                logger.error("异常：{}", e)
            else:
                pass
        return False

    @staticmethod
    def exists_windows(hwnd, folder_path: str, cvstrategy: [] = CVSTRATEGY, timeouts: float = TIMEOUTS,
                       threshold: float = THRESHOLD, wait: float = WAIT, interval: float = INTERVAL,
                       is_throw: bool = THROW,
                       is_click: bool = False, rgb: bool = False, x1: float = 0, x2: float = 1, y1: float = 0,
                       y2: float = 1):
        """
        根据文件夹名获取图片进行图像识别，判断图片是否存在

        :param hwnd: 句柄
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
            resolution = ImageService.resolution_hwnd(hwnd)
            template_list = AirtestService.get_template_list(folder_path, rgb, threshold)
            time_start = time.time()
            while time.time() - time_start < timeouts:
                for template in template_list:
                    # 设备截图
                    image1 = ImageService.windows_screenshot(hwnd, '', True, x1, x2, y1, y2)
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
                                # 打印识别结果
                                # re1 = match['rectangle'][0]
                                # re2 = match['rectangle'][2]
                                # logger.debug(pos)
                                # ImageService.draw_rectangle(image1, re1[0], re1[1], re2[0], re2[1])
                                # 点击指定坐标
                                MouseService.mouse_click(hwnd, pos)
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
    def windows_screenshot(hwnd: int, name: str = None, print_image: bool = False, x1: float = 0, x2: float = 1,
                           y1: float = 0,
                           y2: float = 1):
        """
        设备截图，根据截图比例确定位置
        :param print_image
        :param name:
        :param hwnd:
        :param x1:
        :param x2:
        :param y1:
        :param y2:
        :return:
        """
        if hwnd:
            # 判断窗口是否最大化
            # if not win32gui.IsIconic(hwnd):
            #     # 将窗口最大化
            #     win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            #     time.sleep(0.5)
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
                ndarray_image = np.fromstring(signed_ints_array, dtype='uint8', count=-1, sep='')
                ndarray_image.shape = (h, w, 4)
                ndarray_image = cv2.cvtColor(ndarray_image, cv2.COLOR_BGRA2RGB)
                # 释放位图资源
                win32gui.DeleteObject(bitmap.GetHandle())
                mem_dc.DeleteDC()
                dc_obj.DeleteDC()
                win32gui.ReleaseDC(hwnd, hdc)

                if print_image:
                    # 保存图片到磁盘
                    imageio.imsave("D://screenshot_" + name + "_1.png", ndarray_image)

                coordinate1 = (int(w * x1), int(h * y1))
                coordinate2 = (int(w * x2), int(h * y2))

                # 截取图片
                # cropped_image = ndarray_image[0:525,960:1920]
                cropped_image = ndarray_image[coordinate1[1]:coordinate2[1], coordinate1[0]:coordinate2[0]]

                if print_image:
                    # 保存图片到磁盘
                    imageio.imsave("D://screenshot_" + name + "_2.png", cropped_image)

                return cropped_image
            else:
                logger.debug("句柄宽高获取异常")
        else:
            logger.debug("未找到窗口句柄")

    @staticmethod
    def resolution_hwnd(hwnd: int):
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
    def get_current_hwnd():
        """
        获取当前窗口的信息，进程名，类名，句柄
        :return:
        """
        time.sleep(2)
        logger.debug("获取当前窗口句柄")
        point = win32api.GetCursorPos()  # win32api.GetCursorPos 获取鼠标当前的坐标(x,y)
        logger.debug(point)
        hwnd = win32gui.WindowFromPoint(point)  # 查看坐标位置窗口的句柄
        title = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process_name = psutil.Process(pid).name()
        logger.debug(("进程名：" + process_name, "标题:" + title, "类名：" + class_name, "句柄：" + str(hwnd)))

    @staticmethod
    def get_hwnd_class_name(hwnd):
        class_name = win32gui.GetClassName(hwnd)
        return class_name

    @staticmethod
    def get_all_hwnd():
        # 获取当前主机上的所有句柄id
        all_window_hwnd = []

        # 枚举所有窗口句柄，添加到列表中
        def enum_windows_proc(hwnd, param):
            param.append(hwnd)
            return True

        # 调用枚举窗口API
        win32gui.EnumWindows(enum_windows_proc, all_window_hwnd)

        return all_window_hwnd  # 返回的是一个句柄id的列表

    @staticmethod
    def get_all_hwnd_info(process_name=None, title=None, class_name=None, hwnd=None):
        # 获取当前主机上的所有句柄id,进程信息，窗口标题
        all_window_hwnd = []

        all_window_hwnd_info = []

        # 枚举所有窗口句柄，添加到列表中
        def enum_windows_proc(windows_hwnd, param):
            param.append(windows_hwnd)
            return True

        if hwnd is None:
            # 调用枚举窗口API
            win32gui.EnumWindows(enum_windows_proc, all_window_hwnd)
        else:
            all_window_hwnd.append(hwnd)

        for hwnd1 in all_window_hwnd:
            title1 = win32gui.GetWindowText(hwnd1)
            class_name1 = win32gui.GetClassName(hwnd1)
            _, pid = win32process.GetWindowThreadProcessId(hwnd1)
            process_name1 = psutil.Process(pid).name()
            if process_name is None and title is None and class_name is None and hwnd is None:
                all_window_hwnd_info.append((process_name1, title1, class_name1, hwnd1))
            elif process_name == process_name1 or title == title1 or class_name == class_name1 or hwnd == hwnd1:
                all_window_hwnd_info.append((process_name1, title1, class_name1, hwnd1))
        return all_window_hwnd_info  # 返回列表

    @staticmethod
    # 查询传入的句柄id、类名
    def is_hwnd_class_name(hwnd, class_name):
        # 查询句柄的类名
        window_class = win32gui.GetClassName(hwnd)

        # 判断窗口类名是否和指定的类名相同，如果相同则返回该窗口句柄，否则返回空值
        if window_class == class_name:
            return hwnd

    @staticmethod
    # 遍历窗口句柄的所有子窗口
    def get_child_windows(parent_window_hwnd):
        child_window_handles = []

        def enum_windows_proc(hwnd, param):
            param.append(hwnd)
            return True

        # win32gui.EnumChildWindows    遍历窗口句柄的所有子窗口
        win32gui.EnumChildWindows(parent_window_hwnd, enum_windows_proc, child_window_handles)
        return child_window_handles

    @staticmethod
    def find_hwnd(process_name, class_name):
        all_windows = ImageService.get_all_hwnd()  # 查询所有句柄
        matched_windows = []  # 存放所有匹配类名的句柄id

        # 在所有窗口中查找类名匹配的窗口句柄
        for window_handle in all_windows:
            # get_title方法  检查传入句柄对应的类名和我们实际的类名是否对应
            hwnd = ImageService.is_hwnd_class_name(window_handle, class_name)
            if hwnd:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                process_name1 = psutil.Process(pid).name()
                if process_name1 == process_name:
                    matched_windows.append(hwnd)  # 如果对应就写入列表

        # 如果没有匹配到，则在所有子窗口中查找标题匹配的窗口句柄
        if matched_windows:
            return matched_windows
        else:
            child_window_handles = []
            for parent_window_handle in all_windows:
                # 不论子窗口是否有数据都追加到列表
                child_window_handles.extend(ImageService.get_child_windows(parent_window_handle))
            for child_window_handle in child_window_handles:
                if ImageService.is_hwnd_class_name(child_window_handle, class_name):
                    _, pid = win32process.GetWindowThreadProcessId(child_window_handle)
                    process_name1 = psutil.Process(pid).name()
                    if process_name1 == process_name:
                        matched_windows.append(ImageService.is_hwnd_class_name(child_window_handle, class_name))
        if len(matched_windows) >= 1:
            return matched_windows[0]
        return matched_windows
