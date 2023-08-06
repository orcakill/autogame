# @Time    : 2023年06月20日 15:17
# @Author  : orcakill
# @File    : test_image_service.py
# @Description : 图像识别测试类

import datetime
from unittest import TestCase

from airtest.core.api import touch
from airtest.core.cv import Template

from src.model.enum import Onmyoji, Cvstrategy
from src.service.airtest_service import AirtestService
from src.service.image_service import ImageService
from src.utils.my_logger import logger

image_service = ImageService
airtest_service = AirtestService


class TestImageService(TestCase):
    def test_exists(self):
        airtest_service.auto_setup("0")
        now = datetime.datetime.now()
        # is_border = image_service.exists(Onmyoji.border_JJTZJWP)
        is_border = image_service.exists(Onmyoji.border_WJJTZJ,cvstrategy=Cvstrategy.default)
        logger.debug(is_border)
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_exists_coordinate(self):
        airtest_service.auto_setup("0")
        now = datetime.datetime.now()
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_touch(self):
        airtest_service.auto_setup("0")
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("开始")
        image_service.touch(Onmyoji.border_JG,cvstrategy=Cvstrategy.default,interval=1)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)
