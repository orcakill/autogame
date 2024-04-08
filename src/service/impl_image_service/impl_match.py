"""
# @Time: 2024年03月31日11:10
# @Author: orcakill
# @File: impl_match.py
# @Description: match相关接口
"""
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


class ImplMatch:
    @staticmethod
    def cv_match(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeouts: int = TIMEOUTS,
                 threshold: float = THRESHOLD, wait: float = WAIT, is_throw: bool = THROW,
                 rgb: bool = False, x1: float = 0, x2: float = 1, y1: float = 0, y2: float = 1):
        """
        计算图片和设备截图的匹配结果，有result 坐标  confidence 相似度 区域范围
         :param cvstrategy: 图像识别算法
        :param y2: y2坐标比例
        :param x2: x2坐标比例
        :param y1: y1坐标比例0
        :param x1: x1坐标比例
        :param rgb: 带颜色
        :param timeouts: 图片组超时时间
        :param wait: 图片等待识别时间
        :param is_throw: 是否显示异常
        :param folder_path: 图片文件夹路径
        :param threshold: 图像识别阈值
        :return:
        """
        try:
            resolution = AirtestService.resolution_ratio()
            time.sleep(wait)
            template_list = AirtestService.get_template_list(folder_path, rgb, threshold)
            time_start = time.time()
            while time.time() - time_start < timeouts:
                for template in template_list:
                    # 设备截图
                    image1 = AirtestService.crop_image(x1 * resolution[0], y1 * resolution[1], x2 * resolution[0],
                                                       y2 * resolution[1])
                    return AirtestService.cv_match(template, image1, cvstrategy)
            return None
        except Exception as e:
            if is_throw:
                logger.error("异常：{}", e)
            else:
                pass
        return None

    @staticmethod
    def match_in(folder_path1: str, folder_path2: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT,
                 timeouts: int = TIMEOUTS, threshold: float = THRESHOLD, wait: float = WAIT,
                 is_throw: bool = THROW, rgb: bool = False):
        """
        根据文件夹名获取图片进行图像识别，判断图片内图片是否存在
        :param rgb: 带颜色
        :param timeouts: 图片组超时时间
        :param wait: 图片等待识别时间
        :param is_throw: 是否显示异常
        :param folder_path1: 图片文件夹路径1 局部图
        :param folder_path2: 图片文件夹路径2 局部图内图片
        :param cvstrategy: 图像识别算法
        :param timeout: 单张图片超时时间
        :param threshold: 图像识别阈值
        :return:
        """
        try:
            time.sleep(wait)
            result = ImplMatch.cv_match(folder_path1)
            if result:
                result_xy1 = result['rectangle'][0]
                result_xy2 = result['rectangle'][1]
                result_screen = AirtestService.crop_image(result_xy1[0], result_xy1[1], result_xy2[0], result_xy2[1])
                template_list = AirtestService.get_template_list(folder_path2, rgb, threshold)
                time_start = time.time()
                while time.time() - time_start < timeouts:
                    for template in template_list:
                        pos = AirtestService.match_in(template, result_screen, cvstrategy, timeout, is_throw)
                        if pos:
                            if is_throw:
                                logger.debug("局部图内图像识别成功:{},{}", folder_path2, template.filename)
                            else:
                                logger.debug("局部图内图像识别成功:{}", folder_path2)
                            return pos
            return False
        except Exception as e:
            if is_throw:
                logger.exception("异常：{}", e)
            else:
                pass
        return False
