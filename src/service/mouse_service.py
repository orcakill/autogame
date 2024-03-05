# @Time: 2024年03月02日 16:39
# @Author: orcakill
# @File: mouse_service.py
# @Description: 鼠标操作类
import time

import win32api
import win32con


class MouseService():
    @staticmethod
    def mouse_click(hwnd, pos1, pos2: tuple = None, down_type: str = 'left_down', times: int = 1, wait_time: int = 0.4):
        """
        鼠标点击操作
        :param wait_time: 等待时间
        :param hwnd: 窗口句柄
        :param pos1: 坐标1
        :param pos2: 坐标2
        :param down_type: 点击类型 left_down 左键点击 right_down 右键点击 left_move 左键拖拽 right_move 右键拖拽
        :param times: 点击次数 1次
        :return:
        """
        param1 = win32api.MAKELONG(pos1[0], pos1[1])
        param2 = None
        if pos2:
            param2 = win32api.MAKELONG(pos2[0], pos1[2])
        # 双击
        for i_click in range(1, times):
            # 左右键 点击
            if down_type == 'left_down':
                win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, param1)
                time.sleep(wait_time)
                win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, param1)
            elif down_type == 'right_down':
                win32api.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_LBUTTON, param1)
                time.sleep(wait_time)
                win32api.PostMessage(hwnd, win32con.WM_RBUTTONUP, None, param1)
            # 左右键 拖拽
            elif down_type == 'left_move':
                win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, param1)
                time.sleep(wait_time)
                win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, param2)
            elif down_type == 'right_move':
                win32api.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_LBUTTON, param1)
                time.sleep(wait_time)
                win32api.PostMessage(hwnd, win32con.WM_RBUTTONUP, None, param2)
