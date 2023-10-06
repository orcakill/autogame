# @Time: 2023年08月23日 10:04
# @Author: orcakill
# @File: windows_service.py
# @Description: window 相关服务接口
import os
import shutil
import subprocess
import time

import psutil
import pythoncom
import win32com
from win32com.client import Dispatch

from src.utils import utils_path
from src.utils.my_logger import logger


class WindowsService:
    @staticmethod
    def start_exe(process, name):
        process_name = process  # 替换为你的应用程序进程名称
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop_path, name + ".lnk")  # 替换为你的桌面快捷方式路径

        if not WindowsService.check_process_running(process_name):
            WindowsService.start_process(shortcut_path)
            logger.debug("应用程序未运行，已启动")
            time.sleep(10)
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
        pythoncom.CoInitialize()
        # 使用快捷方式启动应用程序
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        file_path = shortcut.Targetpath
        # 使用subprocess模块运行程序，并创建新的控制台窗口
        subprocess.Popen(file_path, creationflags=subprocess.CREATE_NEW_CONSOLE)

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

    @staticmethod
    def limit_cpu_percentage(percentage):
        process = psutil.Process(os.getpid())
        cpu_count = psutil.cpu_count()
        cpu_limit = int(cpu_count * (percentage / 100))
        process.cpu_affinity(list(range(cpu_limit)))

    @staticmethod
    def delete_folder_file(folder_path, day: int = 1):
        """
        删除创建时间2天以上的
        :return:
        """
        # 获取当前时间
        now = time.time()

        # 遍历文件夹中的所有文件
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # 获取文件的创建时间
            create_time = os.path.getctime(file_path)
            # 计算创建时间距今的天数
            days_diff = (now - create_time) / (24 * 60 * 60)
            # 如果创建时间距今 x  天以上，则删除文件
            if days_diff > day:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)


if __name__ == '__main__':
    path = os.path.join(utils_path.get_project_path_log(), "debug")
    WindowsService.delete_folder_file(path, 2)
