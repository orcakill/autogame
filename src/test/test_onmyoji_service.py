# @Time: 2023年07月21日 08:16
# @Author: orcakill
# @File: test_onmyoji_service.py
# @Description: 服务测试类
import warnings
from unittest import TestCase

from src.dao.mapper import select_game_account
from src.model.models import GameProjects, GameProjectsRelation, GameProject
from src.service.image_service import ImageService
from src.service.onmyoji_service import OnmyojiService
from src.utils.my_logger import logger


class TestOnmyojiService(TestCase):

    def test_initialization(self):
        """
        项目一：登录
        :return:
        """
        TestOnmyojiService.test_project(self, ['1'], "0", "登录")

    def test_daily_rewards(self):
        """
        项目2 每日奖励
        :return:
        """
        TestOnmyojiService.test_project(self, ['1'], '1', "每日奖励")

    def test_encounter_demons(self):
        """
        项目3 逢魔之时
        :return:
        """
        TestOnmyojiService.test_project(self, ['2', '3', '4', '5'], '0', "逢魔之时")

    def test_ghost_king(self):
        """
        项目4 地域鬼王
        :return:
        """
        TestOnmyojiService.test_project(self, ['2', '3', '4', '5'], '1', "地域鬼王")

    def test_foster_care(self):
        """
        项目5 式神寄养
        :return:
        """
        warnings.simplefilter('ignore', ResourceWarning)
        TestOnmyojiService.test_project(self, ['2'], '2', "式神寄养")

    def test_shack_house(self):
        """
        项目6 阴阳寮管理
        :return:
        """
        TestOnmyojiService.test_project(self, ['2', '3', '4', '5'], '0', "阴阳寮管理")

    def test_region_border(self):
        """
        项目7 阴阳寮突破
        :return:
        """
        TestOnmyojiService.test_project(self, ['2', '3', '4', '5'], '0', "阴阳寮突破")

    def test_border_fight(self):
        """
        项目8 个人突破
        :return:
        """
        TestOnmyojiService.test_project(self, ['4'], '1', "个人突破")

    def test_friends_manage(self):
        """
        项目9 好友管理
        :return:
        """
        TestOnmyojiService.test_project(self, ['2', '3', '4', '5'], '0', "好友管理")

    def test_friends_fight(self):
        """
        项目10 好友协战
        :return:
        """
        TestOnmyojiService.test_project(self, ['2', '3', '4', '5'], '0', "好友协战")

    def test_awakening(self):
        """
        项目11 觉醒10
        :return:
        """
        TestOnmyojiService.test_project(self, ['2', '3', '4', '5'], '0', "觉醒十")

    def test_soul_fight_one(self):
        """
        项目12 魂一
        :return:
        """
        TestOnmyojiService.test_project(self, ['2', '3', '4', '5'], '0', "魂一")

    def test_soul_fight_ten(self):
        """
        项目13 魂十
        :return:
        """
        TestOnmyojiService.test_project(self, ['2', '3', '4', '5'], '0', "魂十")

    def test_soul_fight_eleven(self):
        """
        项目14 魂十一
        :return:
        """
        TestOnmyojiService.test_project(self, ['1'], '0', "魂十一")

    def test_soul_fight_fire(self):
        """
        项目16 业原火
        :return:
        """
        TestOnmyojiService.test_project(self, ['1'], '0', "业原火")

    def test_soul_fight_sun(self):
        """
        项目17 日轮之陨
        :return:
        """
        TestOnmyojiService.test_project(self, ['1'], '1', "日轮之陨")

    def test_soul_fight_sea(self):
        """
        项目18 永生之海
        :return:
        """
        TestOnmyojiService.test_project(self, ['1'], '1', "永生之海")

    def test_explore(self):
        """
        项目21 探索
        :return:
        """
        TestOnmyojiService.test_project(self, ['1'], '0', "探索")

    def test_project(self, test_names, test_devices, project_name):
        """
        项目测试
        :param test_names:
        :param test_devices:
        :param project_name:
        :return:
        """
        # 初始化设备信息
        ImageService.auto_setup(test_devices)
        for i in range(len(test_names)):
            test_name = test_names[i]
            # 初始化测试任务信息
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = select_game_account(test_name)
            game_project = GameProject()
            game_project.project_name = project_name
            game_task = [game_projects, game_projects_relation, game_account, game_project]
            logger.debug("当前状态初始化{}", test_name)
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 项目 1、24 每日奖励领取
            if game_project.project_name in ["登录"]:
                OnmyojiService.initialization(game_task)
            # 项目 2
            elif game_project.project_name in ["每日奖励"]:
                OnmyojiService.daily_rewards(game_task)
            # 项目 3
            elif game_project.project_name in ["逢魔之时"]:
                OnmyojiService.encounter_demons(game_task)
            # 项目 4
            elif game_project.project_name in ["地域鬼王"]:
                OnmyojiService.ghost_king(game_task)
            # 项目 5
            elif game_project.project_name in ["式神寄养"]:
                OnmyojiService.foster_care(game_task)
            # 项目 5
            elif game_project.project_name in ["阴阳寮管理"]:
                OnmyojiService.shack_house(game_task)
            # 项目 7
            elif game_project.project_name in ["阴阳寮突破"]:
                OnmyojiService.region_border(game_task)
            # 项目 8
            elif game_project.project_name in ["个人突破"]:
                OnmyojiService.border_fight(game_task)
            # 项目 9
            elif game_project.project_name in ["好友管理"]:
                OnmyojiService.friends_manage(game_task)
            # 项目 10
            elif game_project.project_name in ["好友协战"]:
                OnmyojiService.friends_fight(game_task)
            # 项目 11
            elif game_project.project_name in ["觉醒十"]:
                OnmyojiService.awakening(game_task)
            # 项目 12,13,14,15
            elif game_project.project_name in ["魂一", "魂十", "魂十一", "魂十二"]:
                game_projects_relation.project_num_times = 2
                OnmyojiService.soul_fight(game_task)
            # 项目 16
            elif game_project.project_name in ["业原火"]:
                game_projects_relation.project_num_times = 2
                OnmyojiService.soul_fight_fire(game_task)
            # 项目 17
            elif game_project.project_name in ["日轮之陨"]:
                game_projects_relation.project_num_times = 50
                OnmyojiService.soul_fight_sun(game_task)
            # 项目 18
            elif game_project.project_name in ["永生之海"]:
                game_projects_relation.project_num_times =1
                OnmyojiService.soul_fight_sea(game_task,1)
            # 项目 21
            elif game_project.project_name in ["探索"]:
                game_projects_relation.project_num_times = 1
                OnmyojiService.explore_chapters(game_task)
