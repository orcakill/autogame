# @Time: 2023年08月05日 15:48
# @Author: orcakill
# @File: test_ComplexService.py
# @Description: TODO
import datetime
import warnings
from unittest import TestCase

from src.dao.mapper import select_game_account
from src.model.enum import Onmyoji
from src.model.models import GameProjects, GameProjectsRelation, GameProject
from src.service.airtest_service import AirtestService
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.windows_service import WindowsService
from src.service_onmyoji_impl import impl_house, impl_initialization
from src.utils.my_logger import logger


class TestComplexService(TestCase):

    def test_fight(self):
        AirtestService.auto_setup("0")
        fight_fight = Onmyoji.awaken_TZ
        fight_win = Onmyoji.awaken_ZDSL
        fight_fail = Onmyoji.awaken_ZDSB
        fight_again = Onmyoji.awaken_ZCTZ
        fight_end = Onmyoji.awaken_TCTZ
        logger.debug("开始")
        now = datetime.datetime.now()
        for i in range(10):
            logger.debug("测试，挑战{}次", i + 1)
            is_fight = ImageService.touch(fight_fight)
            if is_fight:
                logger.debug("判断是否未挑战")
                is_fight = ImageService.touch(fight_fight, wait=2)
                if is_fight:
                    logger.debug("再次点击挑战")
            logger.debug("等待战斗结果")
            ComplexService.fight_end(fight_win, fight_fail, fight_again, fight_end, fight_fight, None, 60, 1)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_fight_end(self):
        AirtestService.auto_setup("0")
        logger.debug("开始")
        now = datetime.datetime.now()
        ComplexService.fight_end(Onmyoji.border_ZDSL, Onmyoji.border_ZDSB,
                                 Onmyoji.border_ZCTZ, Onmyoji.border_TCTZ, Onmyoji.border_GRJJ,
                                 None, 300, 1)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_swipe_floor(self):
        AirtestService.auto_setup("0")
        logger.debug("开始")
        now = datetime.datetime.now()
        ComplexService.swipe_floor(Onmyoji.awaken_C, Onmyoji.awaken_SC, 1, 5)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_top_addition(self):
        AirtestService.auto_setup("2")
        logger.debug("开始")
        now = datetime.datetime.now()
        ComplexService.top_addition(Onmyoji.soul_BQ_JC, Onmyoji.soul_BQ_YHJC, Onmyoji.soul_BQ_JCK, Onmyoji.soul_BQ_JCG,
                                    0)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_debris_fight(self):
        """
        式神碎片
        :return: 
        """
        AirtestService.auto_setup("1")
        logger.debug("开始")
        now = datetime.datetime.now()
        for i in range(20):
            ImageService.touch(Onmyoji.explore_SPTZ)
            ComplexService.fight_end(Onmyoji.explore_ZDSL, Onmyoji.explore_ZDSB, Onmyoji.explore_ZCTZ,
                                     Onmyoji.explore_TCTZ, Onmyoji.explore_SPTZ, None, 60, 1)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_faster(self):
        """
        寄养检查
        :return:
        """
        logger.debug("寄养列表检查")
        WindowsService.limit_cpu_percentage(30)
        ImageService.auto_setup("1")
        logger.debug("开始")
        now = datetime.datetime.now()
        impl_house.get_optimal_card()
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_card(self):
        logger.debug("结界卡识别")
        warnings.simplefilter('ignore', ResourceWarning)
        ImageService.auto_setup("1")
        now = datetime.datetime.now()
        logger.debug(impl_house.get_card_type(Onmyoji.foster_JJK_TG, 0))
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_left_card(self):
        logger.debug("左侧结界卡识别")
        warnings.simplefilter('ignore', ResourceWarning)
        ImageService.auto_setup("1")
        now = datetime.datetime.now()
        result = impl_house.get_card_left_type(Onmyoji.foster_JJK_WXTG)
        logger.debug(result)
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_return_home(self):
        now = datetime.datetime.now()
        logger.debug("返回首页")
        # 初始化测试任务信息
        game_projects = GameProjects()
        game_projects_relation = GameProjectsRelation()
        game_account = select_game_account("2")
        game_project = GameProject()
        game_project.project_name = "登录"
        game_task = [game_projects, game_projects_relation, game_account, game_project]
        ImageService.auto_setup("1")
        impl_initialization.initialization(game_task, 1)
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_calculate_proportion(self):
        """
        计算比例
        :return:
        """
        ImageService.auto_setup("1")
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("测试-开始")
        logger.debug("测试-开获取上方好友坐标")
        coordinate_friend = ImageService.exists(Onmyoji.foster_SFHY)
        logger.debug("测试-开获取上方跨区坐标")
        coordinate_region = ImageService.exists(Onmyoji.foster_SFKQ)
        logger.debug("测试-开计算起始位置1,测试系数")
        coordinate_difference = (coordinate_region[0] - coordinate_friend[0])
        coordinate_difference1 = 0.8228571428571428 * (coordinate_region[0] - coordinate_friend[0])
        coordinate_start = (coordinate_region[0], coordinate_region[1])
        logger.debug(coordinate_difference1)
        logger.debug(coordinate_start)
        logger.debug("测试-开计算起始位置2")
        coordinate_end = (coordinate_region[0], coordinate_region[1] + coordinate_difference)
        logger.debug(coordinate_end)
        c1 = ImageService.exists(Onmyoji.test_TEST1)
        c2 = ImageService.exists(Onmyoji.test_TEST2)
        logger.debug(c1)
        logger.debug(c2)
        logger.debug((c2[1] - c1[1]) / (3 * coordinate_difference))
        logger.debug("测试-开结束")
        now1 = datetime.datetime.now()
        logger.debug(now1 - now)
