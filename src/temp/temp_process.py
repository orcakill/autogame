# @Time: 2023年08月23日 09:50
# @Author: orcakill
# @File: temp_process.py
# @Description: 测试window 服务
import os

import psutil


def check_process_running(process_name):
    # 使用tasklist命令检查进程是否正在运行
    output = os.popen('tasklist /FI "IMAGENAME eq {}.exe"'.format(process_name)).read()
    # 检查输出结果中是否包含进程名称
    if process_name in output:
        return True
    else:
        return False


def start_process(shortcut_path):
    # 使用快捷方式启动应用程序
    os.startfile(shortcut_path)


def main():
    process_name = "Nox"  # 替换为你的应用程序进程名称
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    shortcut_path = os.path.join(desktop_path, "夜神模拟器.lnk")  # 替换为你的桌面快捷方式路径

    if not check_process_running(process_name):
        start_process(shortcut_path)
        print("应用程序未运行，已启动。")
    else:
        print("应用程序正在运行。")


if __name__ == "__main__":
    # 获取所有进程列表
    processes = psutil.process_iter()

    # 输出每个进程的名称
    for process in processes:
        print(process.name())
    main()
