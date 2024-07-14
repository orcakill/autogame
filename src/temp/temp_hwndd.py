"""
# @Time: 2024年07月12日22:55
# @Author: orcakill
# @File: temp_hwndd.py
# @Description: TODO
"""
import ctypes

import win32api
import win32gui
import tkinter as tk


from ctypes import windll


def get_scaling():
    user32 = windll.user32
    # 获取现在的尺寸（缩放后
    now_width = user32.GetSystemMetrics(0)
    now_height = user32.GetSystemMetrics(1)
    # 限制UI缩放
    user32.SetProcessDPIAware()
    # 获取屏幕真实的尺寸
    origin_width = user32.GetSystemMetrics(0)
    origin_height = user32.GetSystemMetrics(1)
    # 计算缩放比例
    scaling = round(origin_width / now_width, 2)
    print('现在的尺寸 =>', now_width, now_height)
    print('真实的尺寸 =>', origin_width, origin_height)
    print('缩放比例为 =>', scaling)
    return scaling







if __name__ == '__main__':
    print(get_scaling())
