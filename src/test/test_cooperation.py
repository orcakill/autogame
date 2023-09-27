"""
# @Time: 2023年09月15日22:49
# @Author: orcakill
# @File: test_cooperation.py
# @Description: 合作
"""
import time
from unittest import TestCase

from src.model.enum import Onmyoji, Cvstrategy
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
        testOnmyojiService.test_project(['6'], '2', "个人突破")

    def test_soul1(self):
        # 队长
        ImageService.auto_setup("2")
        for i in range(80):
            logger.debug("组队挑战-第{}次挑战", i + 1)
            is_fight = ImageService.touch(Onmyoji.soul_BQ_ZDTZ, wait=4)
            logger.debug("判断是否自动战斗")
            is_auto = ImageService.exists(Onmyoji.soul_BQ_ZD, timeouts=5)
            if not is_auto:
                logger.debug("未挑战")
                is_fight = False
            # 无自动战斗，则重新点击挑战，拒接悬赏
            if not is_fight:
                ComplexService.refuse_reward()
                ImageService.touch(Onmyoji.soul_BQ_ZDTZ)
            ComplexService.fight_end_win(Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_TCTZ, 100, 2)

    def test_soul2(self):
        # 队员
        ImageService.auto_setup("1")
        for i in range(80):
            logger.debug("组队挑战-测试-第{}次等待战斗结果", i + 1)
            ComplexService.fight_end_win(Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_TCTZ, 100, 1)

    def test_plot(self):
        """
        剧情
        :return:
        """
        ImageService.auto_setup("2")
        for i in range(100):
            logger.debug("{}次", i + 1)
            logger.debug("三个点")
            ImageService.touch(Onmyoji.plot_SGD)
            logger.debug("跳过")
            ImageService.touch(Onmyoji.plot_XFTG)
            logger.debug("右上快进")
            ImageService.touch(Onmyoji.plot_XFTG, cvstrategy=Cvstrategy.default)
            logger.debug("小怪战斗")
            is_fight = ImageService.touch(Onmyoji.plot_XGZD)
            if is_fight:
                logger.debug("准备")
                ImageService.touch(Onmyoji.plot_ZB, wait=5)
                time.sleep(15)
            logger.debug("退出挑战")
            ImageService.touch(Onmyoji.explore_TCTZ)
            logger.debug("等待3s")
            time.sleep(3)
