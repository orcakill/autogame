"""
# @Time: 2023年06月13日19:24
# @Author: orcakill
# @File: airtest_service.py
# @Description: airtest接口
"""
import logging
import random
from datetime import datetime as imp_datetime

from airtest import aircv
from airtest.aircv import cv2_2_pil
from airtest.core.api import *
from airtest.core.helper import G
from airtest.core.settings import Settings

from src.service.windows_service import WindowsService
from src.utils import utils_path
from src.utils.my_logger import my_logger as logger
from src.utils.utils_path import get_onmyoji_image_path

# 控制airtest的日志输出
log_airtest = logging.getLogger("airtest")
log_airtest.setLevel(logging.CRITICAL)

# 图片点击识别等待时间(秒）·
WAIT = 2
# 图像识别阈值
THRESHOLD = 0.7


class AirtestService:
    @staticmethod
    def auto_setup(connect_name: str):
        auto_setup(__file__, logdir=False, devices=["Android://127.0.0.1:5037/" + connect_name])

    @staticmethod
    def snapshot(name: str, print_image: bool = False):
        """
        这个函数是用来实时截图的。它调用了G.DEVICE的snapshot()方法来获取截图，并将结果以数组的形式返回。
        :return: 数组
        """
        screen = G.DEVICE.snapshot()
        if print_image:
            pil_image = cv2_2_pil(screen)
            # 获取当前时间
            now = imp_datetime.now()
            # 将时间转换为字符串
            time_str = now.strftime("%Y-%m-%d_%H-%M-%S") + "_" + name
            path = os.path.join(utils_path.get_project_path_log(), "image")
            WindowsService.delete_folder_file(path, 2)
            path = os.path.join(path, time_str)
            pil_image.save(path + ".png", quality=99, optimize=True)
        return screen

    @staticmethod
    def exists(template: Template, cvstrategy: [], timeout: float, is_throw: bool):
        """
        判断图片是否存在并返回坐标
        :param template: 图片类
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param is_throw: 是否显示异常
        :return: bool
        """
        Settings.CVSTRATEGY = cvstrategy
        Settings.FIND_TIMEOUT_TMP = timeout
        try:
            return exists(template)
        except Exception as e:
            if is_throw:
                logger.error("异常：{}", e)
            else:
                pass

    @staticmethod
    def touch(template: Template, cvstrategy: [], timeout: float, is_throw: bool, times: int,
              duration: float):
        """
        判断图片是否存在
        :param times: 点击次数
        :param duration: 按住时间
        :param template: 图片类
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param is_throw: 是否显示异常
        :return: bool
        """
        Settings.CVSTRATEGY = cvstrategy
        Settings.FIND_TIMEOUT = timeout
        try:
            if touch(template, times=times, duration=duration):
                return True
            else:
                return False
        except Exception as e:
            if is_throw:
                logger.error("异常：{}", e)
            else:
                pass

    @staticmethod
    def touch_coordinate(v: [], duration: float, wait_time: float):
        time.sleep(wait_time)
        if touch(v, duration=duration):
            logger.debug("坐标点击成功")
            return True
        else:
            return False

    @staticmethod
    def restart_app(app: str):
        """
        重启APP
        :param app: app的包名
        :return: 无
        """
        stop_app(app)
        time.sleep(2)
        start_app(app)
        time.sleep(1)

    @staticmethod
    def stop_app(app: str):
        """
        停止APP
        :param app: app的包名
        :return: 无
        """
        stop_app(app)

    @staticmethod
    def swipe(v1: [], v2: [], duration):
        """
        重启APP
        :param duration: 滑动间隔
        :param v1: 图片1
        :param v2: 图片2
        :return: 无
        """
        if swipe(v1, v2, duration=duration):
            return True
        else:
            return False

    @staticmethod
    def crop_image(x1, y1, x2, y2):
        screen = G.DEVICE.snapshot()
        # 局部截图
        local_screen = aircv.crop_image(screen, (x1, y1, x2, y2))
        return local_screen

    @staticmethod
    def resolution_ratio():
        if G.DEVICE.display_info['orientation'] in [1, 3]:
            height = G.DEVICE.display_info['width']
            width = G.DEVICE.display_info['height']
        else:
            height = G.DEVICE.display_info['height']
            width = G.DEVICE.display_info['width']
        return width, height

    @staticmethod
    def cv2_2_pil(local):
        return cv2_2_pil(local)

    @staticmethod
    def find_all(template: Template, cvstrategy: [], timeout: float, is_throw: bool):
        """
        多图查找
        :param template: 图片类
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param is_throw: 是否显示异常
        :return:
        """
        Settings.CVSTRATEGY = cvstrategy
        Settings.FIND_TIMEOUT = timeout
        try:
            result = find_all(template)
            return result
        except Exception as e:
            if is_throw:
                logger.error("异常：{}", e)
            else:
                pass

    @staticmethod
    def loop_find(template: Template, cvstrategy: [], timeout: float, is_throw: bool):
        """
        多图查找
        :param template: 图片类
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param is_throw: 是否显示异常
        :return:
        """
        Settings.CVSTRATEGY = cvstrategy
        Settings.FIND_TIMEOUT = timeout
        try:
            result = loop_find(template)
            return result
        except Exception as e:
            if is_throw:
                logger.error("异常：{}", e)
            else:
                pass

    @staticmethod
    def cv_match(template: Template, screen, cvstrategy: []):
        Settings.CVSTRATEGY = cvstrategy
        return template._cv_match(screen)

    @staticmethod
    def match_in(template: Template, screen, cvstrategy: [], timeout: float, is_throw: bool):
        """
        判断图片是否存在并返回坐标
        :param screen:   局部截图
        :param template: 图片类
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param is_throw: 是否显示异常
        :return: bool
        """
        Settings.CVSTRATEGY = cvstrategy
        Settings.FIND_TIMEOUT_TMP = timeout
        try:
            return template.match_in(screen)
        except Exception as e:
            if is_throw:
                logger.error("异常：{}", e)
            else:
                pass

    @staticmethod
    def text(word: str):
        """
        文字
        :param word: 文字内容
        :return:
        """
        text1 = "input text '" + word + "'"
        shell(text1)

    @staticmethod
    def get_template_list(folder_path: str, rgb: bool = False, threshold: float = THRESHOLD):
        """
        根据文件夹名获取图片集合，转为template列表
        :param threshold: 图像识别阈值
        :param rgb: RGB
        :param folder_path: 图片文件夹路径
        :return:
        """
        template_list = []
        folder_all_path = os.path.join(get_onmyoji_image_path(), folder_path)
        folder_list = os.listdir(folder_all_path)
        random.shuffle(folder_list)
        for file_name in folder_list:
            file_path = os.path.abspath(os.path.join(folder_all_path, file_name))
            # 判断文件是否存在
            if os.path.isfile(file_path):
                # 判断文件是否是图片类型
                file_ext = file_path.split('.')[-1].lower()
                if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                    # 图片类赋值
                    template = Template(filename=file_path, rgb=rgb, threshold=threshold)
                    template_list.append(template)
            else:
                logger.debug("{}文件不存在", file_path)
        return template_list
