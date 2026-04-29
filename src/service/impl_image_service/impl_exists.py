# @Time: 2024年03月22日 09:29
# @Author: orcakill
# @File: impl_exists.py
# @Description: 图像识别接口，实现类
import random
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
INTERVAL = 0.01
# 点击次数
TIMES = 1
# 按住时间
DURATION = 0.01

THROW = False


class ImplExistsTouch:
    @staticmethod
    def exists(folder_path: str, cvstrategy: list = CVSTRATEGY, timeout: float = TIMEOUT, timeouts: float = TIMEOUTS,
               threshold: float = THRESHOLD, wait: float = WAIT, interval: float = INTERVAL, is_throw: bool = THROW,
               is_click: bool = False, rgb: bool = False, deviation: float = 1, duration: float = DURATION):
        """
        根据文件夹名获取图片进行图像识别，判断图片是否存在
        :param duration: 长按
        :param deviation: 制作误差
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
        time.sleep(wait)
        template_list = AirtestService.get_template_list(folder_path, rgb, threshold)
        time_start = time.time()
        while time.time() - time_start < timeouts:
            for template in template_list:
                try:
                    if deviation == 0 and is_click:
                        result = AirtestService.touch(folder_path, template, cvstrategy, timeout, is_throw,
                                                     click_times=TIMES, duration=duration)
                        if result:
                            AirtestService.draw_point("", 0, 0, name=folder_path+"_零误差")
                            return result
                        continue  # 单张图片识别失败，继续下一张

                    else:
                        pos = AirtestService.exists(template, cvstrategy, timeout, is_throw)
                        # print(template.filename)
                        if pos:
                            # 制作误差
                            random_range1 = random.randint(-15, 15)
                            random_range2 = random.randint(random_range1, 15)
                            random_num1 = random.randint(random_range1, random_range2) * deviation
                            random_num2 = random.randint(random_range1, random_range2) * deviation
                            pos = (int(pos[0] + random_num1), int(pos[1] + random_num2))
                            # 截图打印
                            AirtestService.draw_point("", pos[0], pos[1], name=folder_path)
                            if is_click:
                                time.sleep(interval)
                                logger.debug("图像识别点击成功:{}", folder_path)
                                AirtestService.touch_coordinate(pos, duration=duration, wait_time=wait)
                                return True
                            if not is_click:
                                if is_throw:
                                    logger.debug("图像识别成功:{},{}", folder_path, template.filename)
                                else:
                                    logger.debug("图像识别成功:{}", folder_path)
                                return pos
                except Exception as e:
                    if is_throw:
                        logger.debug("单张图片识别异常，继续下一张: {}", e)
                    continue  # 单张图片识别异常，跳过继续下一张
        AirtestService.draw_point("", 0, 0, name=folder_path + "_未识别")
        return False
