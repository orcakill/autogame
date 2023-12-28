# @Time: 2023年12月21日 18:28
# @Author: orcakill
# @File: test_super_service.py
# @Description: 超鬼王
from unittest import TestCase

from src.test.test_onmyoji_service import TestOnmyojiService


class TestSuperService(TestCase):

    def test_current_awakening1(self):
        """
        项目1 个人突破+觉醒 荣耀平板
        :return:
        """
        TestOnmyojiService.test_project('1', '2', "个人突破")
        TestOnmyojiService.test_project('1', '2', "觉醒十", fight_times=100)

    def test_current_awakening2(self):
        """
        项目2 个人突破+觉醒  云手机
        :return:
        """
        TestOnmyojiService.test_project('2', '0', "觉醒十", fight_times=100)

    def test_current_awakening3(self):
        """
        项目3 个人突破+觉醒 夜神模拟器
        :return:
        """
        TestOnmyojiService.test_project('3', '1', "觉醒十", fight_times=100)

    def test_current_super1(self):
        """
        超鬼王
        :return:
        """
        TestOnmyojiService.test_project('1', '2', "当前活动1")

    def test_current_super2(self):
        """
        超鬼王
        :return:
        """
        TestOnmyojiService.test_project('2', '0', "当前活动1")

    def test_current_super3(self):
        """
        超鬼王
        :return:
        """
        TestOnmyojiService.test_project('3', '1', "当前活动1")
