# @Time    : 2023年06月16日 09:15
# @Author  : orcakill
# @File    : image_service.py
# @Description : 图像识别接口
import os
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
TIMEOUT = 20
# 图像识别阈值
THRESHOLD = 0.7
# 图片识别次数（次）
NUMBER = 1
# 图片识别间隔(秒）·
INTERVAL = 1


class ImageService:
    @staticmethod
    def exists(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: int = TIMEOUT,
               threshold: float = THRESHOLD, number: int = NUMBER, interval: int = INTERVAL) -> bool:
        """
        根据文件夹名获取图片进行图像识别，判断图片是否存在
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param threshold: 图像识别阈值
        :param number:   图片组识别次数
        :param interval:   图片识别间隔
        :return: bool
        """
        return image_rec(folder_path, cvstrategy, timeout, "exists", threshold, number, interval)

    @staticmethod
    def touch(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: int = TIMEOUT,
              threshold: float = THRESHOLD, number: int = NUMBER, interval: int = INTERVAL) -> bool:
        """
        根据文件夹名获取图片进行图像识别，点击图片
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param threshold: 图像识别阈值
        :param number:   图片组识别次数
        :param interval:   图片识别间隔
        :return: bool
        """
        return image_rec(folder_path, cvstrategy, timeout, "touch", threshold, number, interval)


def image_rec(folder_path: str, cvstrategy: [], timeout: int, image_type: str, threshold: float, number: int,
              interval: int) -> bool:
    """
    根据文件夹名获取图片进行图像识别，点击图片
    :param folder_path: 图片文件夹路径
    :param cvstrategy: 图像识别算法
    :param timeout: 单张图片超时时间
    :param image_type: 识别类型
    :param threshold: 图像识别阈值
    :param number:   图片组识别次数
    :param interval:   图片识别间隔
    :return: bool
    """
    folder_all_path = os.path.join(get_onmyoji_image_path(), folder_path)
    for i in range(number):
        for file_name in os.listdir(folder_all_path):
            file_path = os.path.abspath(os.path.join(folder_all_path, file_name))
            # 判断文件是否存在
            if os.path.isfile(file_path):
                # 判断文件是否是图片类型
                file_ext = file_path.split('.')[-1].lower()
                if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                    # 图片类赋值
                    template = Template(filename=file_path)
                    # 根据识别类型，存在 或 存在并点击
                    if image_type == "exists":
                        # 判断图片是否存在
                        if airtest_service.exists(template, cvstrategy, timeout, threshold):
                            logger.debug("图片识别成功")
                            return True
                    elif image_type == "touch":
                        # 判断图片是否存在并点击
                        if airtest_service.touch(template, cvstrategy, timeout, threshold):
                            logger.debug("图片识别点击成功")
                            return True
            else:
                logger.debug("{}文件不存在", file_path)
        logger.debug("第{}轮图片未识别", i+1)
        # 等待 *秒
        time.sleep(interval)
    return False
