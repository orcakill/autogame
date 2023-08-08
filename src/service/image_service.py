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
from src.utils.my_logger import my_logger as logger
from src.utils.project_path import get_onmyoji_image_path

# 导入 airtest服务接口
airtest_service = AirtestService()

# 图像识别算法
CVSTRATEGY = Cvstrategy.sift
# 单张图片识别时间
TIMEOUT = 1
# 图片组识别时间
TIMEOUTS = 20
# 图像识别阈值
THRESHOLD = 0.7
# 图片识别轮次
REC_ROUND = 1
# 图片识别间隔(秒）·
INTERVAL = 1
# 点击次数
TIMES = 1
# 按住时间
DURATION = 0.01


class ImageService:
    @staticmethod
    def exists(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: int = TIMEOUT, timeouts: int = TIMEOUTS,
               threshold: float = THRESHOLD, interval: float = INTERVAL, is_throw: bool = False,
               is_click: bool = False):
        """
        根据文件夹名获取图片进行图像识别，判断图片是否存在
        :param timeouts: 图片组超时时间
        :param interval: 间隔时间
        :param is_click: 是否点击坐标
        :param is_throw: 是否显示异常
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 单张图片超时时间
        :param threshold: 图像识别阈值
        :return:
        """
        time.sleep(interval)
        template_list = get_template_list(folder_path)
        time_start = time.time()
        while time.time() - time_start < timeouts:
            for template in template_list:
                pos = airtest_service.exists(template, cvstrategy, timeout, threshold, is_throw)
                if pos and not is_click:
                    logger.debug("图像识别成功:{}", folder_path)
                    return pos
                if pos and is_click:
                    logger.debug("图像识别点击成功:{}", folder_path)
                    airtest_service.touch_coordinate(pos)
                    return True
        return False

    @staticmethod
    def touch(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT,timeouts: int = TIMEOUTS,
              threshold: float = THRESHOLD, interval: float = INTERVAL, is_throw: bool = False, times: int = TIMES,
              duration: float = DURATION):
        """
        根据文件夹名获取图片进行图像识别，点击图片
        :param timeouts: 图片组超时时间
        :param interval: 点击间隔时间
        :param times: 点击次数
        :param duration: 按住时间
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param threshold: 图像识别阈值
        :param is_throw: 是否显示异常,默认不显示异常
        :return: bool
        """
        time.sleep(interval)
        template_list = get_template_list(folder_path)
        time_start = time.time()
        while time.time() - time_start < timeouts:
            for template in template_list:
                is_click = airtest_service.touch(template, cvstrategy, timeout, threshold, is_throw, times, duration)
                if is_click:
                    logger.debug("图像识别点击成功:{}", folder_path)
                    return True
        return False

    @staticmethod
    def wait(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: int = 20,
             threshold: float = THRESHOLD, interval: float = INTERVAL, is_throw: bool = False,
             is_click: bool = False):
        """
        根据文件夹名获取图片进行图像识别，等待图片出现并点击
        :param is_click: 是否点击坐标
        :param interval: 图像识别间隔
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param threshold: 图像识别阈值
        :param is_throw: 是否显示异常,默认不显示异常
        :return: bool
        """
        time.sleep(interval)
        template_list = get_template_list(folder_path)
        for template in template_list:
            pos = airtest_service.wait(template, cvstrategy, timeout, threshold, interval, is_throw)
            if pos and not is_click:
                logger.debug("图像识别成功:{}", folder_path)
                return pos
            if pos and is_click:
                airtest_service.touch_coordinate(pos)
                logger.debug("图像识别点击成功:{}", folder_path)
                return pos
        return False


def get_template_list(folder_path: str):
    """
    根据文件夹名获取图片集合，转为template列表
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
                template = Template(filename=file_path)
                template_list.append(template)
        else:
            logger.debug("{}文件不存在", file_path)
    return template_list
