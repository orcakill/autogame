"""
# @Time: 2023年08月24日00:51
# @Author: orcakill
# @File: test_activity_service.py
# @Description: 活动测试类
"""
from unittest import TestCase

from src.controller.onmyoji_controller import OnmyojiController
from src.model.models import GameProjects, GameProjectsRelation, GameProject, GameAccount
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
        TestActivityService.test_project([5], '1', '买票')

    @staticmethod
    def test_project(test_names, test_devices, project_name):
        """
        项目测试
        :param test_names:
        :param test_devices:
        :param project_name:
        :return:
        """
        # 初始化项目组信息
        logger.debug("活动")
        game_tasks = OnmyojiController.create_tasks(test_names, "", project_name)
        for i in range(len(game_tasks)):
            logger.debug("活动")
            game_task = game_tasks[i]
            game_projects = GameProjects(game_task[0])
            game_projects_relation = GameProjectsRelation(game_task[1])
            game_account = GameAccount(game_task[2])
            game_project = GameProject(game_task[3])
            logger.debug("活动-当前状态初始化:{}", game_account.role_name)
            # 连接设备
            ImageService.auto_setup(test_devices)
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 项目 1、
            if game_project.project_name in ["买票"]:
                game_task = [game_projects, game_projects_relation, game_account, game_project]
                ActivityService.current_buy(game_task)
