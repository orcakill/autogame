# @Time: 2024年03月26日 13:41
# @Author: orcakill
# @File: impl_find.py
# @Description: 图像接口实现类
import time

from src.model.enum import Cvstrategy
from src.service.airtest_service import AirtestService
from src.utils.my_logger import my_logger as logger

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
# 是否抛出异常
THROW = False


class ImplFind:
    @staticmethod
    def find_all(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT, timeouts: int = TIMEOUTS,
                 threshold: float = THRESHOLD, wait: float = WAIT, is_throw: bool = THROW,
                 rgb: bool = False):
        """
        多图查找
        :param rgb: 带颜色
        :param timeouts: 图片组超时时间
        :param wait: 图片等待识别时间
        :param is_throw: 是否显示异常
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 单张图片超时时间
        :param threshold: 图像识别阈值
        :return:
        """
        try:
            time.sleep(wait)
            template_list = AirtestService.get_template_list(folder_path, rgb, threshold)
            time_start = time.time()
            while time.time() - time_start < timeouts:
                for template in template_list:
                    pos = AirtestService.find_all(template, cvstrategy, timeout, is_throw)
                    if pos:
                        logger.debug("图像查找成功:{}", folder_path)
                        return pos
            return None
        except Exception as e:
            if is_throw:
                logger.error("异常：{}", e)
            else:
                pass
        return None

    @staticmethod
    def find_all_coordinate(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT,
                            timeouts: int = TIMEOUTS, threshold: float = THRESHOLD, wait: float = WAIT,
                            is_throw: bool = THROW, rgb: bool = False):
        """
        多图查找 只获取坐标
        :param rgb: 带颜色
        :param timeouts: 图片组超时时间
        :param wait: 图片等待识别时间
        :param is_throw: 是否显示异常
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 单张图片超时时间
        :param threshold: 图像识别阈值
        :return:
        """
        try:
            time.sleep(wait)
            template_list = AirtestService.get_template_list(folder_path, rgb, threshold)
            time_start = time.time()
            while time.time() - time_start < timeouts:
                for template in template_list:
                    pos = AirtestService.find_all(template, cvstrategy, timeout, is_throw)
                    if pos:
                        logger.debug("图像查找成功:{}", folder_path)
                        return [d['result'] for d in pos]
            return None
        except Exception as e:
            if is_throw:
                logger.error("异常：{}", e)
            else:
                pass
        return None
