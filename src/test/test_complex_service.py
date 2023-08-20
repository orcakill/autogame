# @Time: 2023年08月05日 15:48
# @Author: orcakill
# @File: test_complex_service.py
# @Description: TODO
import datetime
from unittest import TestCase

from src.model.enum import Onmyoji
from src.service.airtest_service import AirtestService
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.utils.my_logger import logger

image_service = ImageService
airtest_service = AirtestService
complex_service = ComplexService


class TestComplexService(TestCase):

    def test_fight(self):
        airtest_service.auto_setup("0")
        fight_fight = Onmyoji.awaken_TZ
        fight_win = Onmyoji.awaken_ZDSL
        fight_fail = Onmyoji.awaken_ZDSB
        fight_again = Onmyoji.awaken_ZCTZ
        fight_end = Onmyoji.awaken_TCTZ
        logger.debug("开始")
        now = datetime.datetime.now()
        for i in range(10):
            logger.debug("测试，挑战{}次", i + 1)
            is_fight = image_service.touch(fight_fight)
            if is_fight:
                logger.debug("判断是否未挑战")
                is_fight = image_service.touch(fight_fight, wait=2)
                if is_fight:
                    logger.debug("再次点击挑战")
            logger.debug("等待战斗结果")
            complex_service.fight_end(fight_win, fight_fail, fight_again, fight_end, fight_fight, 60)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_fight_end(self):
        airtest_service.auto_setup("0")
        logger.debug("开始")
        now = datetime.datetime.now()
        complex_service.fight_end(Onmyoji.border_ZDSL, Onmyoji.border_ZDSB,
                                  Onmyoji.border_ZCTZ, Onmyoji.border_TCTZ, Onmyoji.border_GRJJ,
                                  300,1)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_swipe_floor(self):
        airtest_service.auto_setup("0")
        logger.debug("开始")
        now = datetime.datetime.now()
        complex_service.swipe_floor(Onmyoji.awaken_C, Onmyoji.awaken_SC, 1, 5)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_top_addition(self):
        airtest_service.auto_setup("0")
        logger.debug("开始")
        now = datetime.datetime.now()
        complex_service.top_addition(Onmyoji.awaken_JC, Onmyoji.awaken_JXJC, Onmyoji.awaken_JCG, Onmyoji.awaken_JCG, 0)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)
