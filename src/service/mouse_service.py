# @Time: 2024年03月02日 16:39
# @Author: orcakill
# @File: mouse_service.py
# @Description: 鼠标操作类
import time

import win32api
import win32con


class MouseService():
    @staticmethod
    def mouse_click(hwnd, pos):
        x = pos[0]
        y = pos[1]
        param = win32api.MAKELONG(x, y)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, param)
        time.sleep(0.5)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, param)
