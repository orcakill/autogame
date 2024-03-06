# @Time: 2024年02月28日 10:18
# @Author: orcakill
# @File: hwnd_service.py
# @Description: 句柄相关查询及操作
import time

import psutil
import win32api
import win32gui
import win32process

from src.utils.my_logger import my_logger as logger


class HwndService:
    @staticmethod
    def get_current_hwnd():
        """
        获取当前窗口的信息，进程名，类名，句柄
        :return:
        """
        time.sleep(2)
        logger.debug("获取当前窗口句柄")
        point = win32api.GetCursorPos()  # win32api.GetCursorPos 获取鼠标当前的坐标(x,y)
        hwnd = win32gui.WindowFromPoint(point)  # 查看坐标位置窗口的句柄
        title = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process_name = psutil.Process(pid).name()
        logger.debug((process_name, title, class_name, hwnd))

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
        def enum_windows_proc(hwnd, param):
            param.append(hwnd)
            return True

        # 调用枚举窗口API
        win32gui.EnumWindows(enum_windows_proc, all_window_hwnd)

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
    def find_hwnd(class_name):
        all_windows = HwndService.get_all_hwnd()  # 查询所有句柄
        matched_windows = []  # 存放所有匹配类名的句柄id

        # 在所有窗口中查找类名匹配的窗口句柄
        for window_handle in all_windows:
            # get_title方法  检查传入句柄对应的类名和我们实际的类名是否对应
            hwnd = HwndService.is_hwnd_class_name(window_handle, class_name)
            if hwnd:
                matched_windows.append(hwnd)  # 如果对应就写入列表

        # 如果没有匹配到，则在所有子窗口中查找标题匹配的窗口句柄
        if matched_windows:
            return matched_windows
        else:
            child_window_handles = []
            for parent_window_handle in all_windows:
                # 不论子窗口是否有数据都追加到列表
                child_window_handles.extend(HwndService.get_child_windows(parent_window_handle))
            for child_window_handle in child_window_handles:
                if HwndService.is_hwnd_class_name(child_window_handle, class_name):
                    matched_windows.append(HwndService.is_hwnd_class_name(child_window_handle, class_name))
        return matched_windows
