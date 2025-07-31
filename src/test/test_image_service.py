# @Time    : 2023年06月20日 15:17
# @Author  : orcakill
# @File    : test_ImageService.py
# @Description : 图像识别测试类

import datetime
import time
from unittest import TestCase

from src.model.enum import Onmyoji, Cvstrategy
from src.service.airtest_service import AirtestService
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.utils.my_logger import logger
from src.utils.utils_time import UtilsTime

cvstrategy = Cvstrategy.default


class TestImageService(TestCase):

    def test_exists(self):
        ComplexService.auto_setup("0")
        logger.debug("开始")
        now = time.time()
        ImageService.ocr_touch(["切换", "缥缈之旅","网易一缥缈之旅切换","相伴相随", "桃映春馨", "两情相悦", "遥远之忆", "抢先体验服"])
        now1 = time.time()
        logger.debug("结束")
        logger.debug(UtilsTime.convert_seconds(now1 - now))

    def test_exists_coordinate(self):
        ComplexService.auto_setup("4")

    def test_key_back(self):
        ComplexService.auto_setup("1")
        ImageService.keyevent_back()

    def test_touch(self):
        ComplexService.auto_setup("1")
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("开始")
        ImageService.touch(Onmyoji.login_DLAN, cvstrategy=Cvstrategy.default, wait=4)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_touch_coordinate(self):
        ComplexService.auto_setup("1")
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("开始")
        ImageService.touch_coordinate((873, 357))
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_snapshot(self):
        """
        0云手机-001
        1 夜神模拟器
        2 平板
        3 手机
        4 云手机-002
        :return:
        """
        ComplexService.auto_setup("0")
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("开始")
        ImageService.snapshot("1", False)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_check_method(self):
        """
        0云手机-001
        1 夜神模拟器
        2 平板
        3 手机
        4 云手机-002
        :return:
        """
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("开始")
        ComplexService.auto_setup("3")
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_snapshot_for(self):
        # 测试代码
        logger.debug("开始")
        ComplexService.auto_setup("2")
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
        ComplexService.auto_setup("0")
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
        ComplexService.auto_setup("2")
        # 测试代码
        logger.debug("开始")
        result = ImageService.find_all(Onmyoji.arrange_QZBZ)
        if result:
            logger.debug(result)
            logger.debug(len(result))
            logger.debug([d['result'] for d in result])
            logger.debug(max(result, key=lambda x: x['result'][1])['result'])
        else:
            logger.debug("无识别结果")
        logger.debug("结束")
        now1 = datetime.datetime.now()
        logger.debug(now1 - now)

    def test_cv_match(self):
        ComplexService.auto_setup("1")
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("开始")
        result = ImageService.cv_match(Onmyoji.border_YSJTPDB)
        logger.debug(result)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_text(self):
        ComplexService.auto_setup("1")
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("开始")
        ImageService.text("666")
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_app(self):
        now = datetime.datetime.now()
        # 测试代码
        serialno = "8ce78c9f"
        # serialno = "A2CDUN4312H00817"
        logger.debug("开始")
        AirtestService.adb_restart_app("com.netease.onmyoji")
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_match(self):
        ComplexService.auto_setup("1")
        now = time.time()
        # 测试代码
        logger.debug("开始")
        r1 = ImageService.snapshot("1", True)
        logger.debug(r1)
        r = ImageService.cv_match("D:b.png")
        logger.debug(r)
        logger.debug("结束")
        now1 = time.time()
        print(now1 - now)

    def test_start_app(self):
        ComplexService.auto_setup("2")
        ImageService.restart_app("com.netease.nie.yosemite")
