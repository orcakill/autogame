# @Time: 2023年08月23日 10:04
# @Author: orcakill
# @File: windows_service.py
# @Description: window 相关服务接口
import subprocess

from src.utils.my_logger import logger
import os


class WindowsService:
    @staticmethod
    def start_exe(process, name):
        process_name = process  # 替换为你的应用程序进程名称
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop_path, name + ".lnk")  # 替换为你的桌面快捷方式路径

        if not WindowsService.check_process_running(process_name):
            WindowsService.start_process(shortcut_path)
            logger.debug("应用程序未运行，已启动")
            return False
        else:
            logger.debug("应用程序正在运行")
            return True

    @staticmethod
    def check_process_running(process_name):
        # 使用tasklist命令检查进程是否正在运行
        with os.popen('tasklist /FI "IMAGENAME eq {}.exe"'.format(process_name)) as proc:
            output = proc.read()  # 检查输出结果中是否包含进程名称
        if process_name in output:
            return True
        else:
            return False

    @staticmethod
    def start_process(shortcut_path):
        # 使用快捷方式启动应用程序
        os.startfile(shortcut_path)

    @staticmethod
    def get_device_status_by_ip(ip):
        try:
            result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            return None
        output = result.stdout.decode('utf-8')
        if output.startswith('List of devices attached'):
            # 删除开头的"List of devices attached"和结尾的空行
            device_list_string = output.replace('List of devices attached', '').strip()
            # 拆分设备列表字符串为设备和状态的元组列表
            devices = [tuple(device.split('\t')) for device in device_list_string.split('\r\n') if device]
            if devices:
                for item in devices:
                    if item[0] == ip:
                        return item[1]
            else:
                return False
        else:
            return False
