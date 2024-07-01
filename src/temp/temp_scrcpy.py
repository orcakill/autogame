import subprocess
import time

import win32con
import win32gui
import win32ui

from src.service.impl_image_service.impl_hwnd import ImplHwnd
from src.service.windows_service import WindowsService
from src.utils.my_logger import logger


def window_capture(filename, windows_hwnd, resolution_tuple):  # 窗口截屏
    # hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwnd_dc = win32gui.GetWindowDC(windows_hwnd)
    # 根据窗口的DC获取mfcDC
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    # mfcDC创建可兼容的DC
    save_dc = mfc_dc.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    save_bit_map = win32ui.CreateBitmap()
    w2 = resolution_tuple[0]  # 设置截图的X轴宽度【可根据截图保存的文件filename查看，然后实际调整】
    h2 = resolution_tuple[1]  # 设置截图的Y轴高度【可根据截图保存的文件filename查看，然后实际调整】
    # 为bitmap开辟空间
    save_bit_map.CreateCompatibleBitmap(mfc_dc, w2, h2)
    # 高度saveDC，将截图保存到saveBitmap中
    save_dc.SelectObject(save_bit_map)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    save_dc.BitBlt((0, 0), (w2, h2), mfc_dc, (0, 0), win32con.SRCCOPY)
    save_bit_map.SaveBitmapFile(save_dc, filename)


def get_adb_resolution(device_address):
    command = 'adb -s ' + device_address + ' shell wm size'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    resolution_tuple = output.decode().strip().split(' ')[-1]
    resolution_tuple = tuple(map(int, resolution_tuple.split('x')))
    if resolution_tuple:
        return resolution_tuple


def screen_title(windows_title):
    logger.debug("根据标题获取句柄")
    hwnd_info = ImplHwnd.get_all_hwnd_info(title=windows_title)
    logger.debug('句柄信息{}', hwnd_info)
    hwnd_tuple = hwnd_info[0]
    hwnd = hwnd_tuple[-1]
    if hwnd:
        logger.debug("句柄ID:{}", str(hwnd))
        cut_image_file = 'D://' + str(device_name) + '.png'
        window_capture(cut_image_file, hwnd, resolution)  # 对windows窗体进行截图
    else:
        logger.debug("未找到句柄")


def screen_hwnd(windows_title):
    logger.debug("根据标题获取句柄")
    hwnd_info = ImplHwnd.get_all_hwnd_info(title=windows_title)
    logger.debug('句柄信息{}', hwnd_info)
    hwnd_tuple = hwnd_info[0]
    hwnd = hwnd_tuple[-1]
    if hwnd:
        logger.debug("句柄ID:{}", str(hwnd))
        ImplHwnd.windows_screenshot(hwnd=hwnd,name='测试',print_image=True)
    else:
        logger.debug("未找到句柄")


if __name__ == '__main__':
    # 可以运行以下注释的代码，获得手机的序列号,诸君可自行提取自己的手机序列号
    # cmdstr = "adb devices"
    # backstr = os.popen(cmdstr).read()
    # print(backstr)
    # device_name = "8ce78c9f"
    device_name = "A2CDUN4312H00817"
    is_device = WindowsService.get_device_status_by_ip(device_name)
    if is_device:
        device_n = ' -s ' + device_name
        # scrcpy --crop设定屏幕=1080*1920并且偏移坐标为 (0,0)
        # 这里的--crop命令就是老版本的-c命令，新版本升级了，-c命令是错误的了。
        # 然而：网上面的所有有关scrcpy命令的教程文档，全部还是-c命令，真鸡儿扯淡，害我查半天
        # -m 1024 限制画面分辨率=1024
        # -b 4M修改视频码率=4M
        # --window-x 100 --window-y 200 --window-width 405 --window-height 720设定窗体起始坐标，设置窗体宽和高
        win_title = device_name
        # 注意这里是windows窗体标题，最好每次打开的windows窗体标题不同，否则多个窗体标题一样的话
        # 会出现错误，找不到句柄
        # 获取设备分辨率
        resolution = get_adb_resolution(device_name)
        logger.debug(resolution)
        cmdstr = 'scrcpy' + device_n + ' --crop=' + str(resolution[1]) + ':' + str(
            resolution[0]) + ':0:0 --window-title '
        cmdstr = cmdstr + win_title
        cmdstr = cmdstr + " -m 1024 -b 4M"
        logger.debug("执行命令{}", cmdstr)
        subprocess.Popen(cmdstr, shell=True)  # 打开scrcpy
        time.sleep(5)
        screen_hwnd(win_title)
    else:
        logger.debug("未找到设备")
