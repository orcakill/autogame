"""
# @Time: 2023年08月27日19:33
# @Author: orcakill
# @File: temp_port.py
# @Description: 端口杀死测试
"""
import psutil


def kill_process_by_port(port):
    for proc in psutil.process_iter():
        try:
            connections = proc.connections()
            for conn in connections:
                if conn.laddr.port == port:
                    proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


if __name__ == '__main__':
    kill_process_by_port("50001")
