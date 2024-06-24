"""
# @Time: 2024年06月22日20:48
# @Author: orcakill
# @File: temp_mincap.py
# @Description: TODO
"""
import os
import shutil
import socket
import struct
import sys
import time
from collections import OrderedDict
from datetime import datetime, timedelta

import uiautomator2 as u2

from src.utils.my_logger import logger


class Banner:
    def __init__(self):
        self.__banner = OrderedDict(
            [('version', 0),
             ('length', 0),
             ('pid', 0),
             ('realWidth', 0),
             ('realHeight', 0),
             ('virtualWidth', 0),
             ('virtualHeight', 0),
             ('orientation', 0),
             ('quirks', 0)
             ])

    def __setitem__(self, key, value):
        self.__banner[key] = value

    def __getitem__(self, key):
        return self.__banner[key]

    def keys(self):
        return self.__banner.keys()

    def __str__(self):
        return str(self.__banner)


class MiniCap:
    def __init__(self, host, port, banner):
        self.buffer_size = 4096
        self.host = host
        self.port = port
        self.banner = banner
        self.socket = None
        self.stop_flag = False

    def connect(self):
        """
        Connect to the specified host and port.

        Raises:
            socket.error: If there is any error creating the socket or connecting.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
        except socket.error as e:
            print(f"Failed to connect to {self.host}:{self.port}. Error: {e}")
            raise e

    @classmethod
    def save_image(cls, data):
        file_name = 'received_image.jpg'  # 图片名
        with open(file_name, 'wb') as f:
            for b in data:
                f.write(b.to_bytes(1, 'big'))

    def consume(self, stop_flag):
        readBannerBytes = 0
        bannerLength = 24
        readFrameBytes = 0
        frameBodyLength = 0
        data = []
        while not stop_flag:
            try:
                chunk = self.socket.recv(self.buffer_size)
            except socket.error as e:
                print(e)
                sys.exit(1)
            cursor = 0
            buf_len = len(chunk)
            while cursor < buf_len:
                if readBannerBytes < bannerLength:
                    map(lambda i, val: self.banner.__setitem__(self.banner.keys()[i], val),
                        [i for i in range(len(self.banner.keys()))], struct.unpack("<2b5ibB", chunk))
                    cursor = buf_len
                    readBannerBytes = bannerLength
                elif readFrameBytes < 4:
                    frameBodyLength += (chunk[cursor] << (readFrameBytes * 8)) >> 0
                    cursor += 1
                    readFrameBytes += 1
                else:
                    if buf_len - cursor >= frameBodyLength:
                        data.extend(chunk[cursor:cursor + frameBodyLength])
                        self.save_image(data)
                        cursor += frameBodyLength
                        frameBodyLength = readFrameBytes = 0
                        data = []
                    else:
                        data.extend(chunk[cursor:buf_len])
                        frameBodyLength -= buf_len - cursor
                        readFrameBytes += buf_len - cursor
                        cursor = buf_len

    def run(self, stop_flag):
        """
        Connect to the specified host and port, then consume all frames from the socket.
        Raises:
            socket.error: If there is any error creating the socket or connecting.
        """
        try:
            self.connect()
            self.consume(stop_flag)
        except socket.error as e:
            print(f"Failed to connect to {self.host}:{self.port}. Error: {e}")
            raise e

    def mini_cap_screen(self, local_path, time_out):
        """
        mini cap截图
        Args:
            local_path: 目标路径
            time_out: 超时时间（秒）
        Returns:
            local_path 或 None
        """
        src_path = "received_image.jpg"
        end_time = datetime.now() + timedelta(seconds=time_out)
        start_time = datetime.now()
        logger.info(f"mini cap 截图开始时间: {start_time}")

        while datetime.now() < end_time:
            if os.path.exists(src_path) and os.path.getsize(src_path) > 200000:
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                shutil.copy2(src_path, local_path)
                logger.info(f"Image copied to {local_path}")

                current_time = datetime.now()
                logger.info(f"mini cap 截图结束时间: {current_time}")
                logger.info(f"mini cap 截图耗时: {current_time - start_time}")

                return local_path
            time.sleep(0.1)

        logger.error("mini cap 截图失败，请检测mini cap service is running")
        return None


if __name__ == '__main__':
    device = u2.connect()
    # time.sleep(1)
    mc = MiniCap('localhost', 1717, Banner())
    mc.run(True)
    mc.mini_cap_screen("D:", 5)
