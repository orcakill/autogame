"""
# @Time: 2023年08月24日00:51
# @Author: orcakill
# @File: test_activity_service.py
# @Description: 活动测试类
"""
import threading
import time
from unittest import TestCase

from src.dao.mapper import select_game_account
from src.model.enum import Onmyoji, Cvstrategy
from src.model.models import GameProjects, GameProjectsRelation, GameProject
from src.service.activity_service import ActivityService
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.ocr_service import OcrService
from src.service.onmyoji_service import OnmyojiService
from src.utils.my_logger import logger

activity_service = ActivityService()
# 服务接口
image_service = ImageService()
complex_service = ComplexService()
ocr_service = OcrService()
project_interrupt_flag = False


class TestActivityService(TestCase):

    @staticmethod
    def test_current_activity0():
        """
        当前活动,设备云手机
        :return:
        """
        test_names = ['1', '2']
        test_devices = '0'
        TestActivityService.test_current_activity(test_names, test_devices)

    @staticmethod
    def test_current_activity1():
        """
        当前活动,设备夜神模拟器
        :return:
        """
        test_names = ['1', '2']
        test_devices = '1'
        TestActivityService.test_current_activity(test_names, test_devices)

    @staticmethod
    def test_current_activity2():
        """
        当前活动,设备荣耀平板
        :return:
        """
        test_names = ['1', '2']
        test_devices = '2'
        TestActivityService.test_current_activity(test_names, test_devices)

    @staticmethod
    def assist_activity():
        global project_interrupt_flag
        logger.debug("开启拒接协战")
        while not project_interrupt_flag:
            time.sleep(30)
            image_service.touch(Onmyoji.comm_FH_XSFYHSCH, cvstrategy=Cvstrategy.default)

    @staticmethod
    def test_current_activity(test_names, test_devices):
        global project_interrupt_flag
        logger.debug("当前活动测试-云手机")
        test_names = test_names
        test_devices = test_devices
        # 初始化设备信息
        image_service.auto_setup(test_devices)
        # 拒接协战
        thread2 = threading.Thread(target=TestActivityService.assist_activity, args=())
        thread2.start()
        for i in range(len(test_names)):
            test_name = test_names[i]
            # 初始化测试任务信息
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = select_game_account(test_name)
            game_project = GameProject()
            game_task = [game_projects, game_projects_relation, game_account, game_project]
            logger.debug("开始测试-当前活动-云手机")
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 执行测试任务
            activity_service.current_activity(game_task)
            logger.debug("{}测试完成", test_name)
            project_interrupt_flag = True
        thread2.join()

    @staticmethod
    def test_current_lbs():
        global project_interrupt_flag
        logger.debug("LBS鬼王测试")
        test_names = ['1']
        test_devices = '1'
        # 初始化设备信息
        image_service.auto_setup(test_devices)
        # 拒接协战
        thread2 = threading.Thread(target=TestActivityService.assist_activity, args=())
        thread2.start()
        for i in range(len(test_names)):
            test_name = test_names[i]
            # 初始化测试任务信息
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = select_game_account(test_name)
            game_project = GameProject()
            game_task = [game_projects, game_projects_relation, game_account, game_project]
            logger.debug("开始测试-LBS鬼王")
            OnmyojiService.return_home(game_task)
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 执行测试任务
            activity_service.current_lbs(game_task)
            logger.debug("{}测试完成", test_name)
            project_interrupt_flag = True
        thread2.join()
