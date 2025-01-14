# @Time: 2025年01月14日 10:13
# @Author: orcakill
# @File: temp_screenshot_efficiency.py
# @Description: TODO
import time

from airtest.core.android import Android
from airtest.core.helper import G

from src.model.enum import Onmyoji
from src.service.airtest_service import AirtestService
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.utils.my_logger import my_logger as logger

if __name__ == '__main__':
    time_list = []
    for i in range(10):
        logger.info("第{}次", i + 1)
        ComplexService.auto_setup("1")
        now = time.time()
        result = ImageService.exists(Onmyoji.login_YYSTB)
        logger.debug("图像识别结果{}", result)
        now1 = time.time()
        logger.debug("耗时{}", now1 - now)
        time_list.append(now1 - now)
        logger.info("休息5秒")
        time.sleep(5)
    total = sum(time_list)  # 计算列表元素的总和
    average = total / len(time_list)  # 计算平均值
    logger.info("平均耗时{}", average)
    start_time = time_list[0]
    end_time = time_list[len(time_list) - 1]
    logger.info("最后识别{}和开始识别{}的时间差值{}", end_time, start_time, end_time - start_time)
