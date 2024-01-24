import cv2
import numpy as np
import win32api
import win32con
import win32gui
import win32ui

def get_window_image(hwnd):
    # 获取窗口的设备上下文
    hdc = win32gui.GetDC(hwnd)
    # 创建一个与内存设备上下文兼容的位图
    bmp = win32ui.CreateBitmap()
    # 获取窗口的宽高
    width = win32gui.GetClientRect(hwnd)[2]
    height = win32gui.GetClientRect(hwnd)[3]
    # 创建一个与内存设备上下文兼容的位图
    bmp.CreateCompatibleBitmap(hdc, width, height)
    # 将位图与内存设备上下文关联
    hdc.SelectObject(bmp)
    # 将窗口的内容复制到内存设备上下文
    hdc.BitBlt((0, 0), (width, height), hdc, (0, 0), win32con.SRCCOPY)
    # 获取位图数据
    bitmap_data = bmp.GetBitmapBits(True)
    # 将位图数据转换为numpy数组
    image = np.frombuffer(bitmap_data, dtype=np.uint8).reshape((height, width, 3))
    # 释放内存设备上下文
    hdc.DeleteDC()
    # 释放设备上下文
    win32gui.ReleaseDC(hwnd, hdc)
    return image

if __name__ == "__main__":
    # 获取窗口句柄
    hwnd = win32gui.FindWindow(None, "钉钉")
    # 判断窗口是否最大化
    if not win32gui.IsIconic(hwnd):
        # 将窗口最大化
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    # 获取窗口截图
    image = get_window_image(hwnd)
    # 保存窗口截图
    cv2.imwrite("D:window_screenshot.png", image)