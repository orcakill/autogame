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
        print(image_service.touch(Onmyoji.login_QHFWQ, cvstrategy=Cvstrategy.default))
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
        # image_service.touch(Onmyoji.home_TS, timeout=0.1, is_throw=True)
        touch(Template(
            r"D:\study\Project\***REMOVED***code\python\autogame\src\resources\static\onmyoji\首页\探索\屏幕截图 2023-08-03 222007.png"))
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)
