# @Time    : 2023年06月16日 09:15
# @Author  : orcakill
# @File    : image_service.py
# @Description : 图像识别接口
import os
import random

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
TIMEOUT = 20
# 图像识别阈值
THRESHOLD = 0.7
# 图片识别轮次
REC_ROUND = 1
# 图片识别间隔(秒）·
INTERVAL = 1


class ImageService:
    @staticmethod
    def exists(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: int = TIMEOUT,
               threshold: float = THRESHOLD) -> bool:
        """
        根据文件夹名获取图片进行图像识别，判断图片是否存在
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param threshold: 图像识别阈值
        :return: bool
        """
        template_list = get_template_list(folder_path)
        is_exist = False
        for template in template_list:
            is_exist = airtest_service.exists(template, cvstrategy, timeout, threshold)
        return is_exist

    @staticmethod
    def exists_coordinate(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: int = TIMEOUT,
                          threshold: float = THRESHOLD):
        """
        根据文件夹名获取图片进行图像识别，判断图片是否存在并返回坐标
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param threshold: 图像识别阈值
        :return:
        """
        template_list = get_template_list(folder_path)
        coordinate = ()
        for template in template_list:
            coordinate = airtest_service.exists_coordinate(template, cvstrategy, timeout, threshold)
        return coordinate

    @staticmethod
    def touch(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: int = TIMEOUT,
              threshold: float = THRESHOLD, interval: int = INTERVAL) -> bool:
        """
        根据文件夹名获取图片进行图像识别，点击图片
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param threshold: 图像识别阈值
        :return: bool
        """
        template_list = get_template_list(folder_path)
        is_click = False
        for template in template_list:
            is_click = airtest_service.touch(template, cvstrategy, timeout, threshold, interval)
        return is_click


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
