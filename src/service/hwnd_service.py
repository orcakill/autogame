# @Time: 2024年02月28日 10:18
# @Author: orcakill
# @File: hwnd_service.py
# @Description: 句柄相关查询及操作
import time

import psutil
import win32api
import win32con
import win32gui
import win32process

from src.utils.my_logger import my_logger as logger


class HwndService:
    @staticmethod
    def get_current_hwnd():
        time.sleep(2)

        point = win32api.GetCursorPos()  # win32api.GetCursorPos 获取鼠标当前的坐标(x,y)

        hwnd = win32gui.WindowFromPoint(point)  # 查看坐标位置窗口的句柄

        logger.debug(hwnd)

    @staticmethod
    def get_hwnd_class_name(hwnd):
        class_name = win32gui.GetClassName(hwnd)
        return class_name

    @staticmethod
    def mouse_click(pos, window_title: str = None, hwnd=None):
        """
        鼠标点击，滑动
        :param window_title:窗口标题
        :param pos:坐标
        :param hwnd:句柄
        :return:
        """
        x = pos[0]
        y = pos[1]
        # 检查句柄是否为空，为空则根据窗口标题获取句柄
        if window_title is not None and hwnd is None:
            hwnd = win32gui.FindWindow(None, window_title)
        if not hwnd:
            raise Exception("找不到窗口")
        logger.debug(hwnd)
        lparam = win32api.MAKELONG(x, y)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
        time.sleep(0.5)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lparam)

    @staticmethod
    def get_all_hwnd():
        """
        获取所有窗口句柄
        :return:
        """
        all_window_handles = []

        # 枚举所有窗口句柄，添加到列表中
        def enum_windows_proc(hwnd, param):
            param.append(hwnd)
            return True

        # 调用枚举窗口API
        win32gui.EnumWindows(enum_windows_proc, all_window_handles)

        return all_window_handles  # 返回的是一个句柄id的列表

    @staticmethod
    def get_hwnd_info(hwnd):
        """
        根据一个窗口句柄获取一个窗口信息
        :param hwnd:
        :return:
        """
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
    def get_hwnd_list(process_name=None, window_title=None, class_name=None, hwnd=None):
        """
        根据进程名、窗口标题、类名、句柄获取进程信息列表
        :param process_name:
        :param window_title:
        :param class_name:
        :param hwnd:
        :return:
        """

        windows = HwndService.get_all_hwnd()
        result = []
        for window_hwnd in windows:
            window_info = HwndService.get_hwnd_info(window_hwnd)
            if window_info:
                process_name1, window_title1, class_name1, hwnd1 = window_info
                # 参数全为空，则获取全部
                if process_name is None and window_title is None and class_name is None and hwnd is None:
                    result.append((process_name1, window_title1, class_name1, hwnd1))
                # 参数不为空，按参数获取数据
                elif process_name == process_name1 or window_title == window_title1 \
                        or class_name == class_name1 or hwnd == hwnd1:
                    result.append((process_name1, window_title1, class_name1, hwnd1))
        return result
