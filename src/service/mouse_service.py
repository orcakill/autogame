# @Time: 2024年03月02日 16:39
# @Author: orcakill
# @File: mouse_service.py
# @Description: 鼠标操作类
import time

import win32api
import win32con


class MouseService():
    @staticmethod
    def mouse_click(hwnd, pos, down_type: str = 'left', times: int = 1):
        """
        鼠标点击操作
        :param hwnd: 窗口句柄
        :param pos: 坐标
        :param down_type: 点击类型 left 左键 right 右键
        :param times: 点击次数 1次
        :return:
        """
        x1 = pos[0]
        y1 = pos[1]
        param1 = win32api.MAKELONG(x1, y1)
        # 左右键点击
        if down_type == 'left':
            win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, param1)
        else:
            win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, param1)
        # 左右键释放
        time.sleep(0.5)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, param1)
