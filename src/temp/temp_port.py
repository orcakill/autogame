"""
# @Time: 2023年08月27日19:33
# @Author: orcakill
# @File: temp_port.py
# @Description: 端口杀死测试
"""
import subprocess

import psutil

import socket

def kill_process_by_port(port):
    for proc in psutil.process_iter():
        try:
            connections = proc.connections()
            for conn in connections:
                if conn.laddr.port == port:
                    proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


# 获取指定IP端口的设备状态
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
        index = next((i for i, device in enumerate(devices) if device[0] == ip), -1)
        return devices[index][1]
    else:
        return None



def visit_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)  # 设置超时时间
    try:
        result = sock.connect_ex((ip, port))  # 尝试连接
        if result == 0:  # 如果连接成功，返回True
            return True
        else:
            return False  # 如果连接失败，返回False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        sock.close()  # 关闭socket连接


if __name__ == '__main__':
    # kill_process_by_port(50000)
    # kill_process_by_port(50001)

    # 使用示例
    ip = '114.115.139.203'
    port = ""
    print(visit_port(ip, port))
