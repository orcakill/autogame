# @Time: 2024年03月22日 09:29
# @Author: orcakill
# @File: impl_exists.py
# @Description: 图像识别接口，实现类
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

THROW = False


def exists(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT, timeouts: float = TIMEOUTS,
           threshold: float = THRESHOLD, wait: float = WAIT, interval: float = INTERVAL, is_throw: bool = THROW,
           is_click: bool = False, rgb: bool = False):
    """
    根据文件夹名获取图片进行图像识别，判断图片是否存在
    :param folder_path: 图片文件夹路径
    :param cvstrategy: 图像识别算法
    :param timeout: 单张图片超时时间
    :param threshold: 图像识别阈值
    :param interval: 图片识别点击间隔时间
    :param rgb: 带颜色
    :param timeouts: 图片组超时时间
    :param wait: 图片等待识别时间
    :param is_click: 是否点击坐标
    :param is_throw: 是否显示异常
    :return:
    """
    try:
        time.sleep(wait)
        template_list = AirtestService.get_template_list(folder_path, rgb, threshold)
        time_start = time.time()
        while time.time() - time_start < timeouts:
            for template in template_list:
                pos = AirtestService.exists(template, cvstrategy, timeout, is_throw)
                if pos and not is_click:
                    if is_throw:
                        logger.debug("图像识别成功:{},{}", folder_path, template.filename)
                    else:
                        logger.debug("图像识别成功:{}", folder_path)
                    return pos
                if pos and is_click:
                    time.sleep(interval)
                    logger.debug("图像识别点击成功:{}", folder_path)
                    AirtestService.touch_coordinate(pos, duration=DURATION, wait_time=WAIT)
                    return True
        return False
    except Exception as e:
        if is_throw:
            logger.exception("异常：{}", e)
        else:
            pass
    return False
