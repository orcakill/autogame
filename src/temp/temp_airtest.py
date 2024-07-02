import subprocess
import time

import win32con
import win32gui
import win32ui

from src.service.airtest_service import AirtestService
from src.service.impl_image_service.impl_hwnd import ImplHwnd
from src.service.windows_service import WindowsService
from src.utils.my_logger import logger

if __name__ == '__main__':
    # 可以运行以下注释的代码，获得手机的序列号,诸君可自行提取自己的手机序列号
    # cmdstr = "adb devices"
    # backstr = os.popen(cmdstr).read()
    # print(backstr)
    device_name = "8ce78c9f"
    # device_name = "A2CDUN4312H00817"
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
        cmdstr = 'scrcpy' + device_n + ' --window-title ' + win_title
        logger.debug("执行命令{}", cmdstr)
        subprocess.Popen(cmdstr, shell=True)  # 打开scrcpy
        time.sleep(5)
        AirtestService.auto_setup_windows(title=win_title)
        AirtestService.snapshot("测试",True)
    else:
        logger.debug("未找到设备")
