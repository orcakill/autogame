# @Time: 2023年09月13日 15:05
# @Author: orcakill
# @File: temp_connection.py
# @Description: 测试连接

import socket


def connection(ip, port=None):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if port:
            result = sock.connect_ex((ip, port))
        else:
            result = sock.connect_ex((ip, 80))  # 默认使用80端口进行测试

        if result == 0:
            print(f"Success: {ip}:{port} is accessible")
        else:
            print(f"Error: {ip}:{port} is not accessible")

        sock.close()
    except socket.error as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    # 测试IP地址
    connection('114.115.139.203')

    # 测试IP地址加端口
    connection('114.115.139.203', 21)
