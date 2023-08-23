# @Time    : 2023年06月16日 09:15
# @Author  : orcakill
# @File    : image_service.py
# @Description : 图像识别接口
import os
import random
import time

from airtest.core.cv import Template

from src.model.enum import Cvstrategy
from src.service.airtest_service import AirtestService
from src.service.windows_service import WindowsService
from src.utils.my_logger import my_logger as logger
from src.utils.project_path import get_onmyoji_image_path
from datetime import datetime as imp_datetime

# 导入 airtest服务接口
airtest_service = AirtestService()

# 图像识别算法
CVSTRATEGY = Cvstrategy.sift
# 单张图片识别时间
TIMEOUT = 0.5
# 图片组识别时间
TIMEOUTS = 5
# 图像识别阈值
THRESHOLD = 0.7
# 图片识别轮次
REC_ROUND = 1
# 图片等待识别时间(秒）·
WAIT = 2
# 图片识别间隔(秒）·
INTERVAL = 1
# 点击次数
TIMES = 1
# 按住时间
DURATION = 0.01
windows_service = WindowsService()


class ImageService:
    @staticmethod
    def exists(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT, timeouts: int = TIMEOUTS,
               threshold: float = THRESHOLD, wait: float = WAIT, interval: float = INTERVAL, is_throw: bool = False,
               is_click: bool = False, rgb: bool = False):
        """
        根据文件夹名获取图片进行图像识别，判断图片是否存在
        :param interval: 图片识别点击间隔时间
        :param rgb: 带颜色
        :param timeouts: 图片组超时时间
        :param wait: 图片等待识别时间
        :param is_click: 是否点击坐标
        :param is_throw: 是否显示异常
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 单张图片超时时间
        :param threshold: 图像识别阈值
        :return:
        """
        try:
            time.sleep(wait)
            template_list = ImageService.get_template_list(folder_path, rgb, threshold)
            time_start = time.time()
            while time.time() - time_start < timeouts:
                for template in template_list:
                    pos = airtest_service.exists(template, cvstrategy, timeout, is_throw)
                    if pos and not is_click:
                        logger.debug("图像识别成功:{}", folder_path)
                        return pos
                    if pos and is_click:
                        time.sleep(interval)
                        logger.debug("图像识别点击成功:{}", folder_path)
                        airtest_service.touch_coordinate(pos)
                        return True
            return False
        except Exception as e:
            if is_throw:
                logger.debug("异常：{}", e)
                return False

    @staticmethod
    def touch(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT, timeouts: float = TIMEOUTS,
              threshold: float = THRESHOLD, wait: float = WAIT, is_throw: bool = False, times: int = TIMES,
              duration: float = DURATION, rgb: bool = False):
        """
        根据文件夹名获取图片进行图像识别，点击图片
        :param rgb: rgb
        :param timeouts: 图片组超时时间
        :param wait: 点击间隔时间
        :param times: 点击次数
        :param duration: 按住时间
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param threshold: 图像识别阈值
        :param is_throw: 是否显示异常,默认不显示异常
        :return: bool
        """
        time.sleep(wait)
        template_list = ImageService.get_template_list(folder_path, rgb, threshold)
        time_start = time.time()
        while time.time() - time_start < timeouts:
            for template in template_list:
                is_click = airtest_service.touch(template, cvstrategy, timeout, is_throw, times, duration)
                if is_click:
                    logger.debug("图像识别点击成功:{}", folder_path)
                    return True
        return False

    @staticmethod
    def auto_setup(game_device: str):
        """
        设备连接
        :param game_device:
        :return:
        """
        if game_device == "0":
            logger.debug("检查是否启动云手机")
            is_state = windows_service.start_exe("YsConsole", "云帅云手机")
            if not is_state:
                logger.debug("等待20秒")
                time.sleep(20)
        if game_device == "1":
            logger.debug("检查是否启动夜神模拟器")
            is_state = windows_service.start_exe("Nox", "夜神模拟器")
            if not is_state:
                logger.debug("等待20秒")
                time.sleep(20)
        airtest_service.auto_setup(game_device)

    @staticmethod
    def snapshot(print_image: bool = False):
        """
        设备截图
        :return:
        """
        img = airtest_service.snapshot()
        if img and print_image:
            pil_image = ImageService.cv2_2_pil(img)
            # 获取当前时间
            now = imp_datetime.now()
            # 将时间转换为字符串
            time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            pil_image.save("D:/" + time_str + ".png", quality=99, optimize=True)
        return img

    @staticmethod
    def touch_coordinate(v: [], wait: float = WAIT):
        """
        点击坐标
        :param v: 坐标
        :param wait: 等待开始时间
        :return:
        """
        airtest_service.touch_coordinate(v, wait)

    @staticmethod
    def restart_app(app: str):
        """
        重启APP
        :param app: 包名
        :return:
        """
        airtest_service.restart_app(app)

    @staticmethod
    def swipe(v1: [], v2: []):
        """
        滑动
        :param v1: 坐标1
        :param v2: 坐标2
        :return:
        """
        airtest_service.swipe(v1, v2)

    @staticmethod
    def crop_image(x1, y1, x2, y2):
        """
        局部截图
        :param x1: x1
        :param y1: y1
        :param x2: x2
        :param y2: y2
        :return:
        """
        airtest_service.crop_image(x1, y1, x2, y2)

    @staticmethod
    def resolving_power():
        """
        获取分辨率
        :return:
        """
        airtest_service.resolving_power()

    @staticmethod
    def cv2_2_pil(local):
        """
        转换图片格式
        :param local:图片
        :return:
        """
        airtest_service.cv2_2_pil(local)

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
