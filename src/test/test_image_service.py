# @Time    : 2023年06月20日 15:17
# @Author  : orcakill
# @File    : test_image_service.py
# @Description : 图像识别测试类
import os
from ctypes import windll

import win32gui
import win32ui
import win32con
import win32api
import numpy as np
from PIL import Image


from src.service.airtest_service import AirtestService
from src.service.image_service import ImageService
import datetime
from airtest.core.api import *
from src.model.enum import Onmyoji, Cvstrategy

image_service = ImageService
airtest_service=AirtestService


def test_exists():
    airtest_service.auto_setup("0")
    now=datetime.datetime.now()
    print(image_service.touch(Onmyoji.login_QHFWQ,cvstrategy=Cvstrategy.default))
    now1 = datetime.datetime.now()
    print(now1-now)

    # # 获取窗口句柄
    # hwnd = win32gui.FindWindow(None, "夜神模拟器")
    #
    # # 获取窗口大小
    # left, top, right, bottom = win32gui.GetClientRect(hwnd)
    # width, height = right - left, bottom - top
    #
    # # 获取设备上下文DC
    # hwndDC = win32gui.GetWindowDC(hwnd)
    # mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # saveDC = mfcDC.CreateCompatibleDC()
    #
    # # 创建位图对象
    # saveBitMap = win32ui.CreateBitmap()
    # saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    #
    # # 将位图对象选入设备上下文
    # saveDC.SelectObject(saveBitMap)
    #
    # # 截取指定区域的屏幕，并将其保存到位图对象中
    # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    #
    # # 将位图对象转换为PIL图像对象
    # bmpinfo = saveBitMap.GetInfo()
    # bmpstr = saveBitMap.GetBitmapBits(True)
    # im = Image.frombuffer(
    #     'RGB',
    #     (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
    #     bmpstr, 'raw', 'BGRX', 0, 1)
    #
    # # 将PIL图像对象转换为numpy数组
    # im = np.array(im)
    #
    #
    #
    # # 保存截图
    # Image.fromarray(im).save("screenshot.png")
