"""
# @Time: 2023年09月15日22:49
# @Author: orcakill
# @File: test_cooperation.py
# @Description: 合作
"""
from unittest import TestCase

from src.model.enum import Onmyoji
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.test.test_onmyoji_service import TestOnmyojiService
from src.utils.my_logger import logger


class TestCooperation(TestCase):

    def test_border1(self):
        testOnmyojiService = TestOnmyojiService()
        testOnmyojiService.test_project(['1'], '1', "个人突破")

    def test_border2(self):
        testOnmyojiService = TestOnmyojiService()
        testOnmyojiService.test_project(['3'], '2', "个人突破")

    def test_soul1(self):
        # 队长
        ImageService.auto_setup("0")
        for i in range(80):
            logger.debug("组队挑战-测试-第{}次挑战", i + 1)
            is_fight = ImageService.touch(Onmyoji.soul_BQ_TZ)
            if not is_fight:
                ComplexService.refuse_reward()
                logger.debug("组队挑战-测试-点击可能的准备")
                ImageService.touch(Onmyoji.soul_BQ_ZB)
            ComplexService.fight_end(Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_ZDSB, Onmyoji.soul_BQ_ZCTZ,
                                     Onmyoji.soul_BQ_TCTZ, Onmyoji.soul_BQ_TZ, None, 100, 1)

    def test_soul2(self):
        # 队员
        ImageService.auto_setup("2")
        for i in range(80):
            logger.debug("组队挑战-测试-第{}次等待战斗结果", i + 1)
            ComplexService.fight_end_win(Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_TCTZ, 100, 1)
