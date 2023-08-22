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
        logger.debug("结界突破")
        # test_names = ['2','3','4','5']
        test_names = ['3']
        test_devices = '0'
        # 初始化设备信息
        AirtestService.auto_setup(test_devices)
        for i in range(len(test_names)):
            test_name = test_names[i]
            # 初始化测试任务信息
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = select_game_account(test_name)
            game_project = GameProject()
            game_task = [game_projects, game_projects_relation, game_account, game_project]
            logger.debug("开始测试-结界突破{}", test_name)
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

    def test_awakening(self):
        logger.debug("结界突破")
        # test_names = ['2','3','4','5']
        test_names = ['2']
        test_devices = '0'
        # 初始化设备信息
        AirtestService.auto_setup(test_devices)
        for i in range(len(test_names)):
            test_name = test_names[i]
            # 初始化测试任务信息
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = select_game_account(test_name)
            game_project = GameProject()
            game_task = [game_projects, game_projects_relation, game_account, game_project]
            logger.debug("开始测试-觉醒{}", test_name)
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 执行测试任务
            OnmyojiService.awakening(game_task)

    def test_daily_rewards(self):
        logger.debug("每日奖励领取")
        # test_names = ['2','3','4','5']
        test_names = ['5']
        test_devices = '0'
        # 初始化设备信息
        AirtestService.auto_setup(test_devices)
        for i in range(len(test_names)):
            test_name = test_names[i]
            # 初始化测试任务信息
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = select_game_account(test_name)
            game_project = GameProject()
            game_task = [game_projects, game_projects_relation, game_account, game_project]
            logger.debug("开始测试-每日奖励{}", test_name)
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 执行测试任务
            OnmyojiService.daily_rewards(game_task)

    def test_encounter_demons(self):
        logger.debug("逢魔之时")
        test_names = ['2', '3', '4', '5']
        # test_names = ['5']
        test_devices = '0'
        # 初始化设备信息
        AirtestService.auto_setup(test_devices)
        for i in range(len(test_names)):
            test_name = test_names[i]
            # 初始化测试任务信息
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = select_game_account(test_name)
            game_project = GameProject()
            game_task = [game_projects, game_projects_relation, game_account, game_project]
            logger.debug("开始测试-逢魔之时{}", test_name)
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 执行测试任务
            OnmyojiService.encounter_demons(game_task)

    def test_ghost_king(self):
        logger.debug("地域鬼王")
        test_names = ['2', '3', '4', '5']
        test_devices = '0'
        # 初始化设备信息
        AirtestService.auto_setup(test_devices)
        for i in range(len(test_names)):
            test_name = test_names[i]
            # 初始化测试任务信息
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = select_game_account(test_name)
            game_project = GameProject()
            game_task = [game_projects, game_projects_relation, game_account, game_project]
            logger.debug("开始测试-地域鬼王")
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 执行测试任务
            OnmyojiService.ghost_king(game_task)
            logger.debug("{}测试完成", test_name)

    def test_friends_manage(self):
        logger.debug("好友管理")
        # test_names = ['2', '3', '4', '5']
        test_names = ['3']
        test_devices = '0'
        # 初始化设备信息
        AirtestService.auto_setup(test_devices)
        for i in range(len(test_names)):
            test_name = test_names[i]
            # 初始化测试任务信息
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = select_game_account(test_name)
            game_project = GameProject()
            game_task = [game_projects, game_projects_relation, game_account, game_project]
            logger.debug("开始测试-好友管理")
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 执行测试任务
            OnmyojiService.friends_manage(game_task)
            logger.debug("{}测试完成", test_name)

    def test_friends_fight(self):
        logger.debug("好友协战")
        # test_names = ['2', '3', '4', '5']
        test_names = ['4', '5']
        test_devices = '0'
        # 初始化设备信息
        AirtestService.auto_setup(test_devices)
        for i in range(len(test_names)):
            test_name = test_names[i]
            # 初始化测试任务信息
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = select_game_account(test_name)
            game_project = GameProject()
            game_task = [game_projects, game_projects_relation, game_account, game_project]
            logger.debug("开始测试-好友协战")
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 执行测试任务
            OnmyojiService.friends_fight(game_task)
            logger.debug("{}测试完成", test_name)

    def test_foster_care(self):
        logger.debug("式神寄养")
        # test_names = ['2', '3', '4', '5']
        test_names = ['2']
        test_devices = '0'
        # 初始化设备信息
        AirtestService.auto_setup(test_devices)
        for i in range(len(test_names)):
            test_name = test_names[i]
            # 初始化测试任务信息
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = select_game_account(test_name)
            game_project = GameProject()
            game_task = [game_projects, game_projects_relation, game_account, game_project]
            logger.debug("开始测试-式神寄养")
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 执行测试任务
            OnmyojiService.foster_care(game_task)
            logger.debug("{}测试完成", test_name)
