# @Time: 2023年08月21日 15:32
# @Author: orcakill
# @File: test_onmyoji_controller.py
# @Description: 每日执行项目-测试
import time

from src.model.enum import Onmyoji
from src.service.image_service import ImageService
from src.utils.my_logger import my_logger as logger

image_service = ImageService()
project_interrupt_flag1 = False


def test_assist1():
    global project_interrupt_flag1
    logger.debug("开启拒接协战")
    while not project_interrupt_flag1:
        time.sleep(30)
        image_service.touch(Onmyoji.comm_FH_XSFYHSCH)
