# @Time: 2024年07月06日 15:26
# @Author: orcakill
# @File: test_scrcpy2.py
# @Description:测试文件截图
import subprocess
import time

import console_ctrl
import cv2

from src.service.windows_service import WindowsService
from src.utils.my_logger import logger
from src.utils.utils_path import UtilsPath

if __name__ == '__main__':
    device_name = "127.0.0.1:62001"
    is_device = WindowsService.get_device_status_by_ip(device_name)
    if is_device:
        device_n = ' -s ' + device_name
        command = 'scrcpy' + device_n + ' --no-playback --record ' + UtilsPath.get_srccpy_path() + "srcpy.mp4"
        logger.debug("执行命令{}", command)
        process = subprocess.Popen(command, shell=True)

        time.sleep(5)

        # 等待录屏结束
        if process  and process.poll() is None:  # 如果进程仍在运行
            console_ctrl.send_ctrl_c(process.pid)  # 发送 Ctrl+C 信号

        # 读取 MP4 文件
        video = cv2.VideoCapture(UtilsPath.get_srccpy_path() + "srcpy.mp4")

        # 获取第一帧
        success, image = video.read()

        if success:
            # 保存第一帧图片
            cv2.imwrite('D:a.png', image)
        else:
            print("无法获取第一帧图片")
    else:
        logger.debug("未找到设备")
