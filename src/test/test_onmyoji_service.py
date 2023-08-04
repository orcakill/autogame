# @Time: 2023年07月21日 08:16
# @Author: orcakill
# @File: test_onmyoji_service.py
# @Description: 服务测试类
from unittest import TestCase

from src.dao.mapper import select_game_account
from src.model.models import GameProjects, GameProjectsRelation, GameProject
from src.service.airtest_service import AirtestService
from src.service.onmyoji_service import OnmyojiService
from src.utils.my_logger import logger


class TestOnmyojiService(TestCase):
    def test_initialization(self):
        # 测试登录功能
        game_projects = GameProjects()
        game_projects_relation = GameProjectsRelation()
        game_account = select_game_account("3")
        game_project = GameProject()
        game_task = [game_projects, game_projects_relation, game_account, game_project]
        logger.debug("开始测试")
        # 初始化设备信息
        AirtestService.auto_setup("0")
        # 当前状态初始化
        OnmyojiService.initialization(game_task)

    def test_border_fight(self):
        # 初始化测试任务信息
        game_projects = GameProjects()
        game_projects_relation = GameProjectsRelation()
        game_account = select_game_account("5")
        game_project = GameProject()
        game_task = [game_projects, game_projects_relation, game_account, game_project]
        logger.debug("开始测试")
        # 初始化设备信息
        AirtestService.auto_setup("0")
        # 当前状态初始化
        OnmyojiService.initialization(game_task)
        # 执行测试任务
        OnmyojiService.border_fight(game_task)

    def test_soul_fight_thug(self):
        # 御魂打手
        logger.debug("开始测试")
        # 初始化设备信息
        AirtestService.auto_setup("1")
        # 执行点击角色头像和退出挑战
        OnmyojiService.soul_fight_thug()
