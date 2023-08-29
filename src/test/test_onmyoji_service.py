# @Time: 2023年07月21日 08:16
# @Author: orcakill
# @File: test_onmyoji_service.py
# @Description: 服务测试类
import threading
import time
from unittest import TestCase

from src.dao.mapper import select_game_account
from src.model.enum import Onmyoji, Cvstrategy
from src.model.models import GameProjects, GameProjectsRelation, GameProject
from src.service.image_service import ImageService
from src.service.onmyoji_service import OnmyojiService
from src.utils.my_logger import logger

image_service = ImageService()
project_interrupt_flag = False


def assist_onmyoji():
    global project_interrupt_flag
    logger.debug("开启拒接协战")
    while not project_interrupt_flag:
        time.sleep(30)
        image_service.touch(Onmyoji.comm_FH_XSFYHSCH, cvstrategy=Cvstrategy.default)


class TestOnmyojiService(TestCase):

    def test_initialization(self):
        """
        项目一：登录
        :return:
        """
        global project_interrupt_flag
        logger.debug("测试-当前状态初始化开始")
        # 测试账号信息
        test_names = ['1']
        # 测试设备 0 云手机 1 夜神模拟器 2荣耀平板
        test_devices = '1'
        # 初始化设备信息
        image_service.auto_setup(test_devices)
        # 拒接协战
        thread2 = threading.Thread(target=assist_onmyoji, args=())
        thread2.start()
        for i in range(len(test_names)):
            test_name = test_names[i]
            # 初始化测试任务信息
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = select_game_account(test_name)
            game_project = GameProject()
            game_task = [game_projects, game_projects_relation, game_account, game_project]
            logger.debug("准备完成-当前状态初始化{}", test_name)
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            project_interrupt_flag = True
        thread2.join()
        logger.debug("测试-当前状态初始化结束")

    def test_daily_rewards(self):
        """
        项目2 每日奖励
        :return:
        """
        global project_interrupt_flag
        logger.debug("每日奖励领取")
        # test_names = ['2','3','4','5']
        test_names = ['1']
        test_devices = '1'
        # 初始化设备信息
        image_service.auto_setup(test_devices)
        # 拒接协战
        thread2 = threading.Thread(target=assist_onmyoji, args=())
        thread2.start()
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
            project_interrupt_flag = True
        thread2.join()
        logger.debug("测试-每日奖励结束")

    def test_encounter_demons(self):
        """
        项目3 逢魔之时
        :return:
        """
        global project_interrupt_flag
        logger.debug("开始测试-逢魔之时")
        # test_names = ['2','3','4','5']-
        test_names = ['2', '3', '4', '5']
        test_devices = '0'
        # 初始化设备信息
        image_service.auto_setup(test_devices)
        # 拒接协战
        thread2 = threading.Thread(target=assist_onmyoji, args=())
        thread2.start()
        for i in range(len(test_names)):
            test_name = test_names[i]
            # 初始化测试任务信息
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = select_game_account(test_name)
            game_project = GameProject()
            game_task = [game_projects, game_projects_relation, game_account, game_project]
            logger.debug("测试开始-逢魔之时{}", test_name)
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 执行测试任务
            OnmyojiService.encounter_demons(game_task)
            project_interrupt_flag = True
        thread2.join()
        logger.debug("测试-逢魔之时结束")

    def test_ghost_king(self):
        """
        项目4 地域鬼王
        :return:
        """
        global project_interrupt_flag
        logger.debug("开始测试-地域鬼王")
        # test_names = ['2','3','4','5']
        test_names = ['1']
        test_devices = '1'
        # 初始化设备信息
        image_service.auto_setup(test_devices)
        # 拒接协战
        thread2 = threading.Thread(target=assist_onmyoji, args=())
        thread2.start()
        for i in range(len(test_names)):
            test_name = test_names[i]
            # 初始化测试任务信息
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = select_game_account(test_name)
            game_project = GameProject()
            game_task = [game_projects, game_projects_relation, game_account, game_project]
            logger.debug("测试开始-地域鬼王{}", test_name)
            OnmyojiService.return_home(game_task)
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 执行测试任务
            OnmyojiService.ghost_king(game_task)
            project_interrupt_flag = True
        thread2.join()
        logger.debug("测试-地域鬼王结束")

    def test_foster_care(self):
        """
        项目5 式神寄养
        :return:
        """
        global project_interrupt_flag
        logger.debug("式神寄养")
        test_names = ['2', '3', '4', '5']
        # test_names = ['1']
        test_devices = '0'
        # 初始化设备信息
        image_service.auto_setup(test_devices)
        # 拒接协战
        thread2 = threading.Thread(target=assist_onmyoji, args=())
        thread2.start()
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
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 执行测试任务
            OnmyojiService.foster_care(game_task)
            logger.debug("{}测试完成", test_name)
            project_interrupt_flag = True
        thread2.join()

    def test_region_border(self):
        """
        项目7 阴阳寮突破
        :return:
        """
        global project_interrupt_flag
        logger.debug("阴阳寮突破")
        test_names = ['1']
        # test_names = ['3']
        test_devices = '1'
        # 初始化设备信息
        image_service.auto_setup(test_devices)
        # 拒接协战
        thread2 = threading.Thread(target=assist_onmyoji, args=())
        thread2.start()
        for i in range(len(test_names)):
            test_name = test_names[i]
            # 初始化测试任务信息
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = select_game_account(test_name)
            game_project = GameProject()
            game_task = [game_projects, game_projects_relation, game_account, game_project]
            logger.debug("开始测试-阴阳寮突破")
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 执行测试任务
            OnmyojiService.region_border(game_task)
            logger.debug("{}测试完成", test_name)
            project_interrupt_flag = True
        thread2.join()

    def test_border_fight(self):
        """
        项目8 个人突破
        :return:
        """
        global project_interrupt_flag
        logger.debug("个人突破")
        test_names = ['1']
        # test_names = ['3']
        test_devices = '1'
        # 初始化设备信息
        image_service.auto_setup(test_devices)
        # 拒接协战
        thread2 = threading.Thread(target=assist_onmyoji, args=())
        thread2.start()
        for i in range(len(test_names)):
            test_name = test_names[i]
            # 初始化测试任务信息
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = select_game_account(test_name)
            game_project = GameProject()
            game_task = [game_projects, game_projects_relation, game_account, game_project]
            logger.debug("开始测试-个人突破")
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 执行测试任务
            OnmyojiService.border_fight(game_task, 3)
            logger.debug("{}测试完成", test_name)
            project_interrupt_flag = True
        thread2.join()

    def test_friends_manage(self):
        """
        项目9 好友管理
        :return:
        """
        global project_interrupt_flag
        logger.debug("好友管理")
        test_names = ['1']
        # test_names = ['3']
        test_devices = '1'
        # 初始化设备信息
        image_service.auto_setup(test_devices)
        # 拒接协战
        thread2 = threading.Thread(target=assist_onmyoji, args=())
        thread2.start()
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
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 执行测试任务
            OnmyojiService.friends_manage(game_task)
            logger.debug("{}测试完成", test_name)
            project_interrupt_flag = True
        thread2.join()

    def test_friends_fight(self):
        """
        项目10 好友协战
        :return:
        """
        global project_interrupt_flag
        logger.debug("好友协战")
        test_names = ['3']
        # test_names = ['3']
        test_devices = '0'
        # 初始化设备信息
        image_service.auto_setup(test_devices)
        # 拒接协战
        thread2 = threading.Thread(target=assist_onmyoji, args=())
        thread2.start()
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
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 执行测试任务
            OnmyojiService.friends_fight(game_task)
            logger.debug("{}测试完成", test_name)
            project_interrupt_flag = True
        thread2.join()

    def test_awakening(self):
        """
        项目11 觉醒10
        :return:
        """
        global project_interrupt_flag
        logger.debug("觉醒十")
        test_names = ['1']
        # test_names = ['3']
        test_devices = '1'
        # 初始化设备信息
        image_service.auto_setup(test_devices)
        # 拒接协战
        thread2 = threading.Thread(target=assist_onmyoji, args=())
        thread2.start()
        for i in range(len(test_names)):
            test_name = test_names[i]
            # 初始化测试任务信息
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = select_game_account(test_name)
            game_project = GameProject()
            game_task = [game_projects, game_projects_relation, game_account, game_project]
            logger.debug("开始测试-觉醒十")
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 执行测试任务
            OnmyojiService.awakening(game_task)
            logger.debug("{}测试完成", test_name)
            project_interrupt_flag = True
        thread2.join()

    def test_soul_fight_thug(self):
        # 御魂打手
        logger.debug("开始测试")
        # 初始化设备信息
        image_service.auto_setup("1")
        # 执行点击角色头像和退出挑战
        OnmyojiService.soul_fight_thug()
