# @Time: 2023年07月21日 08:16
# @Author: orcakill
# @File: test_onmyoji_service.py
# @Description: 服务测试类
from unittest import TestCase

from src.controller.onmyoji_controller import OnmyojiController
from src.dao.mapper_extend import MapperExtend
from src.model.models import GameProjectsRelation, GameProject, GameAccount, GameProjects, GameDevice
from src.service.complex_service import ComplexService
from src.service.onmyoji_service import OnmyojiService
from src.service.windows_service import WindowsService
from src.utils.my_logger import logger


class TestOnmyojiService(TestCase):

    def test_all(self):
        """
        项目一：登录
        0 云手机-001
        1 夜神模拟器
        2 平板
        3 手机
        4 云手机-002
        :return:
        """
        TestOnmyojiService.test_all_project("1,2,3,4,5", "3")

    def test_initialization(self):
        """
        项目一：登录
        0 云手机-001
        1 夜神模拟器
        2 平板
        3 手机
        4 云手机-002
        :return:
        """
        TestOnmyojiService.test_project('1', "2", "登录")

    def test_initialization1(self):
        """
        项目一：登录
        :return:
        """
        TestOnmyojiService.test_project('2,3,4,5', "4", "登录")

    def test_daily_rewards(self):
        """
        项目2 每日奖励
        :return:
        """
        TestOnmyojiService.test_project('1', '0', "每日奖励")

    def test_encounter_demons(self):
        """
        项目3 逢魔之时
        :return:
        """
        TestOnmyojiService.test_project('1', '0', "逢魔之时")

    def test_ghost_king(self):
        """
        项目4 地域鬼王
        :return:
        """
        TestOnmyojiService.test_project('4,5', '1', "地域鬼王")

    def test_foster_care(self):
        """
        项目5 式神寄养
        :return:；
        """
        TestOnmyojiService.test_project('1', '2', "式神寄养")

    def test_shack_house(self):
        """
        项目6 阴阳寮管理
        :return:
        """
        TestOnmyojiService.test_project('2,3,4,5', '1', "阴阳寮管理")

    def test_region_border(self):
        """
        项目7 阴阳寮突破
        :return:
        """
        TestOnmyojiService.test_project('1', '0', "阴阳寮突破")

    def test_border_fight(self):
        """
        项目8 个人突破
        :return:
        """
        TestOnmyojiService.test_project('1', '0', "个人突破")

    def test_border_fight1(self):
        """
        项目8 个人突破
        :return:
        """
        TestOnmyojiService.test_project('1', '2', "个人突破")

    def test_friends_manage(self):
        """
        项目9 好友管理
        :return:
        """
        TestOnmyojiService.test_project('2,3,4,5', '0', "好友管理")

    def test_friends_fight(self):
        """
        项目10 好友协战
        :return:
        """
        TestOnmyojiService.test_project('2,3,4,5', '4', "好友协战")

    def test_awakening(self):
        """
        项目11 觉醒10
        :return:
        """
        TestOnmyojiService.test_project('2,3,4,5', '1', "觉醒十", fight_times=20)

    def test_soul_fight_one(self):
        """
        项目12 魂一
        :return:
        """
        TestOnmyojiService.test_project('2,3,4,5', '0', "魂一")

    def test_soul_fight_ten(self):
        """
        项目13 魂十
        :return:
        """
        TestOnmyojiService.test_project('2,3,4,5', '0', "魂十")

    def test_soul_fight_eleven(self):
        """
        项目14 魂十一
        :return:
        """
        TestOnmyojiService.test_project('1', '2', "魂十一", fight_times=10)

    def test_soul_fight_fire(self):
        """
        项目16 业原火
        :return:
        """
        TestOnmyojiService.test_project('2,3,4,5', '0', "业原火")

    def test_soul_fight_sun(self):
        """
        项目17 日轮之陨
        :return:
        """
        TestOnmyojiService.test_project('1', '0', "日轮之陨", fight_times=50)

    def test_soul_fight_sea(self):
        """
        项目18 永生之海
        :return:
        """
        TestOnmyojiService.test_project('2,3,4,5', '1', "永生之海")

    def test_pvp(self):
        """
        项目19 斗技   
        :return:
        """
        TestOnmyojiService.test_project('1', '2', "斗技", fight_times=100)

    def test_soul_arrange(self):

        """
        项目20 御魂整理
        :return:
        """

        TestOnmyojiService.test_project('1', '2', "御魂整理")

    def test_explore(self):
        """
        项目21 探索
        :return:
        """
        TestOnmyojiService.test_project('1', '0', "探索")

    def test_spirit(self):
        """
        项目22 御灵
        :return:
        """
        TestOnmyojiService.test_project('2,3,4,5', '2', "御灵")

    def test_deed(self):
        """
        项目23 契灵
        :return:
        """
        TestOnmyojiService.test_project('2,3,4,5', '1', "契灵")

    def test_six_moon(self):
        """
        项目27 六道之门-月之海
        :return:
        """
        WindowsService.limit_cpu_percentage(30)
        TestOnmyojiService.test_project('1', '2', "月之海", fight_times=1)

    @staticmethod
    def test_all_project(test_names, test_devices):
        logger.debug("查找所有项目")
        project = MapperExtend.select_game_project("", "")
        logger.debug("循环执行所有项目，部分项目免测试")
        test_reports = []
        num_report = 0
        for i in range(len(project)):
            game_project = GameProject(project[i])
            game_project_num = game_project.project_num
            game_project_name = game_project.project_name
            names_list = test_names.split(",")
            for j in range(len(names_list)):
                name = names_list[j]
                if game_project_name in ['月之海']:
                    logger.debug("所有账号不测试该项目：{}", game_project_name)
                    continue
                if name in ['1'] and game_project_name in ['好友协战']:
                    logger.debug("大号不执行该项目：{}", game_project_name)
                    continue
                if name in ['2', '3', '4', '5'] and game_project_name in ['魂十', '魂十一', '魂十二', '业原火',
                                                                          '日轮之陨', '永生之海']:
                    logger.debug("小号不执行该项目：{}", game_project_name)
                    continue
                num_report = num_report + 1
                logger.info("测试项目{}:{}", game_project_num, game_project_name)
                result = TestOnmyojiService.test_project(name, test_devices, game_project_name)
                result_report = [num_report, name, game_project_name, result]
                test_reports.append(result_report)
                logger.debug("打印报告")
                for k in range(len(test_reports)):
                    logger.debug(test_reports[k])
        logger.debug("最终打印报告")
        for i in range(len(test_reports)):
            logger.debug(test_reports[i])

    @staticmethod
    def test_project(test_names, test_devices, project_name, fight_times: int = 1, chapter: int = 28,
                     difficulty: int = 1):
        """
        项目测试
        :param test_names:
        :param test_devices:
        :param project_name:
        :return:
        """
        # 初始化项目组信息
        WindowsService.limit_cpu_percentage(30)
        game_tasks = OnmyojiController.create_tasks(test_devices, test_names, "", project_name)
        result = False
        for i in range(len(game_tasks)):
            game_task = game_tasks[i]
            logger.debug("初始化项目信息")
            game_projects, game_projects_relation = GameProjects(game_task[0]), GameProjectsRelation(game_task[1])
            game_account = GameAccount(game_task[2])
            game_project = GameProject(game_task[3])
            game_device = GameDevice(game_task[4])
            game_task = [game_projects, game_projects_relation, game_account, game_project, game_device]
            logger.debug("当前状态初始化:{}", game_account.role_name)
            # 连接设备
            ComplexService.auto_setup(test_devices)
            # 当前状态初始化
            OnmyojiService.initialization(game_task)
            # 项目 1、
            if game_project.project_name in ["登录"]:
                result = OnmyojiService.initialization(game_task)
            # 项目 2、24 每日奖励领取
            elif game_project.project_name in ["每日奖励"]:
                result = OnmyojiService.daily_rewards(game_task)
            # 项目 3
            elif game_project.project_name in ["逢魔之时"]:
                result = OnmyojiService.encounter_demons(game_task)
            # 项目 4
            elif game_project.project_name in ["地域鬼王"]:
                result = OnmyojiService.ghost_king(game_task)
            # 项目 5
            elif game_project.project_name in ["式神寄养"]:
                result = OnmyojiService.foster_care(game_task)
            # 项目 5
            elif game_project.project_name in ["阴阳寮管理"]:
                result = OnmyojiService.shack_house(game_task)
            # 项目 7
            elif game_project.project_name in ["阴阳寮突破"]:
                result = OnmyojiService.region_border(game_task)
            # 项目 8
            elif game_project.project_name in ["个人突破"]:
                result = OnmyojiService.border_fight(game_task)
            # 项目 9
            elif game_project.project_name in ["好友管理"]:
                result = OnmyojiService.friends_manage(game_task)
            # 项目 10
            elif game_project.project_name in ["好友协战"]:
                game_projects_relation.project_num_times = fight_times
                game_task = [game_projects, game_projects_relation, game_account, game_project, game_device]
                result = OnmyojiService.friends_fight(game_task)
            # 项目 11
            elif game_project.project_name in ["觉醒十"]:
                game_projects_relation.project_num_times = fight_times
                game_task = [game_projects, game_projects_relation, game_account, game_project, game_device]
                result = OnmyojiService.awakening(game_task)
            # 项目 12,13,14,15
            elif game_project.project_name in ["魂一", "魂十", "魂十一", "魂十二"]:
                game_projects_relation.project_num_times = fight_times
                game_task = [game_projects, game_projects_relation, game_account, game_project, game_device]
                result = OnmyojiService.soul_fight(game_task)
            # 项目 16
            elif game_project.project_name in ["业原火"]:
                game_projects_relation.project_num_times = fight_times
                game_task = [game_projects, game_projects_relation, game_account, game_project, game_device]
                result = OnmyojiService.soul_fight_fire(game_task)
            # 项目 17
            elif game_project.project_name in ["日轮之陨"]:
                game_projects_relation.project_num_times = fight_times
                game_task = [game_projects, game_projects_relation, game_account, game_project, game_device]
                result = OnmyojiService.soul_fight_sun(game_task)
            # 项目 18
            elif game_project.project_name in ["永生之海"]:
                game_projects_relation.project_num_times = fight_times
                game_task = [game_projects, game_projects_relation, game_account, game_project, game_device]
                result = OnmyojiService.soul_fight_sea(game_task, 1)
            # 项目 19
            elif game_project.project_name in ["斗技"]:
                game_projects_relation.project_num_times = fight_times
                game_task = [game_projects, game_projects_relation, game_account, game_project, game_device]
                result = OnmyojiService.pvp(game_task)
            # 项目 20
            elif game_project.project_name in ["御魂整理"]:
                result = OnmyojiService.soul_arrange(game_task)
            # 项目 21
            elif game_project.project_name in ["探索"]:
                game_projects_relation.project_num_times = fight_times
                game_task = [game_projects, game_projects_relation, game_account, game_project, game_device]
                result = OnmyojiService.explore_chapters(game_task, chapter=chapter, difficulty=difficulty)
            # 项目 22
            elif game_project.project_name in ["御灵"]:
                game_projects_relation.project_num_times = fight_times
                game_task = [game_projects, game_projects_relation, game_account, game_project, game_device]
                result = OnmyojiService.spirit_fight(game_task)
            # 项目 23
            elif game_project.project_name in ["契灵"]:
                result = OnmyojiService.deed_spirit(game_task)
            elif game_project.project_name in ["当前活动"]:
                result = OnmyojiService.current_activity(game_task)
            # 项目 27
            elif game_project.project_name in ["月之海"]:
                result = OnmyojiService.six_moon(game_task)
        return result
