# @Time    : 2023年06月20日 15:17
# @Author  : orcakill
# @File    : test_ImageService.py
# @Description : 图像识别测试类

import datetime
import time
from unittest import TestCase

from src.model.enum import Onmyoji, Cvstrategy
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.utils.my_logger import logger

cvstrategy = Cvstrategy.default


class TestImageService(TestCase):
    def test_exists(self):
        now = datetime.datetime.now()
        ImageService.auto_setup("1")
        result =  ImageService.exists(Onmyoji.explore_LHGL,cvstrategy=Cvstrategy.default)
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

    def test_touch_coordinate(self):
        ImageService.auto_setup("1")
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("开始")
        ImageService.touch_coordinate((873,357))
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)
    def test_snapshot(self):
        ImageService.auto_setup("0")
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("开始")
        ImageService.snapshot("1", True)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_snapshot_for(self):
        # 测试代码
        logger.debug("开始")
        ImageService.auto_setup("1")
        now = datetime.datetime.now()
        logger.debug("循环开始")
        for i in range(100):
            logger.debug("第{}次", i + 1)
            ImageService.snapshot("百鬼夜行", True)
            time.sleep(1)
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
        result = ImageService.find_all(Onmyoji.explore_JYJC)
        if result:
            logger.debug(result)
            logger.debug(len(result))
            logger.debug([d['result'] for d in result])
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

    def test_text(self):
        ImageService.auto_setup("1")
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("开始")
        result = ImageService.text("666")
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)
