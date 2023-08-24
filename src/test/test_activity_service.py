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
from src.model.enum import Onmyoji
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
    def assist_activity():
        global project_interrupt_flag
        logger.debug("开启拒接协战")
        while not project_interrupt_flag:
            time.sleep(30)
            image_service.touch(Onmyoji.comm_FH_XSFYHSCH)

    def test_current_activity0(self):
        global project_interrupt_flag
        logger.debug("当前活动测试-云手机")
        # test_names = ['2', '3', '4', '5']
        test_names = ['3']
        test_devices = '0'
        # 初始化设备信息
        image_service.auto_setup(test_devices)
        # 拒接协战
        thread2 = threading.Thread(target=self.assist_activity, args=())
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
            # 执行测试任务
            activity_service.current_activity(game_task)
            logger.debug("{}测试完成", test_name)
            project_interrupt_flag = True
        thread2.join()

    def test_current_activity1(self):
        global project_interrupt_flag
        logger.debug("当前活动测试-夜神模拟器")
        # test_names = ['2', '3', '4', '5']
        test_names = ['4']
        test_devices = '1'
        # 初始化设备信息
        image_service.auto_setup(test_devices)
        # 拒接协战
        thread2 = threading.Thread(target=self.assist_activity, args=())
        thread2.start()
        for i in range(len(test_names)):
            test_name = test_names[i]
            # 初始化测试任务信息
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = select_game_account(test_name)
            game_project = GameProject()
            game_task = [game_projects, game_projects_relation, game_account, game_project]
            logger.debug("开始测试-当前活动-夜神模拟器")
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 执行测试任务
            activity_service.current_activity(game_task)
            logger.debug("{}测试完成", test_name)
            project_interrupt_flag = True
        thread2.join()
