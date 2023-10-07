# @Time    : 2023年06月20日 15:17
# @Author  : orcakill
# @File    : test_ImageService.py
# @Description : 图像识别测试类

import datetime
from unittest import TestCase

from src.model.enum import Onmyoji
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.utils.my_logger import logger


class TestImageService(TestCase):
    def test_exists(self):
        now = datetime.datetime.now()
        ImageService.auto_setup("2")
        result = ImageService.cv_match(Onmyoji.border_WZGRJJ)
        logger.debug(result)
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_exists_coordinate(self):
        ImageService.auto_setup("0")
        now = datetime.datetime.now()
        ComplexService.fight_end(Onmyoji.border_ZDSL, Onmyoji.border_ZDSB,
                                 Onmyoji.border_ZCTZ, Onmyoji.home_TS, Onmyoji.border_GRJJ, None, 60, 1)
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_touch(self):
        ImageService.auto_setup("0")
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("开始")
        ImageService.exists(Onmyoji.home_DBCDDK)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_snapshot(self):
        ImageService.auto_setup("2")
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("开始")
        ImageService.snapshot("1", True)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_crop_image(self):
        ImageService.auto_setup("0")
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("开始")
        ImageService.crop_image(100, 100, 200, 200)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_find_all(self):

        """
        多图查找
        :return:
        """
        now = datetime.datetime.now()
        ImageService.auto_setup("1")
        # 测试代码
        logger.debug("开始")
        result = ImageService.find_all(Onmyoji.foster_XGY)
        if result:
            logger.debug(result)
            logger.debug(len(result))
            logger.debug(max(result, key=lambda x: x['result'][1])['result'])
        logger.debug("结束")
        now1 = datetime.datetime.now()
        logger.debug(now1 - now)

    def test_cv_match(self):
        ImageService.auto_setup("2")
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("开始")
        result = ImageService.cv_match(Onmyoji.border_YSJTPDB)
        logger.debug(result)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)
