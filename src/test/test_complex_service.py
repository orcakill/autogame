# @Time: 2023年08月05日 15:48
# @Author: orcakill
# @File: test_ComplexService.py
# @Description: TODO
import datetime
import warnings
from unittest import TestCase

from src.dao.mapper import Mapper
from src.model.enum import Onmyoji, WinProcessName, WinClassName
from src.model.models import GameProjects, GameProjectsRelation, GameProject
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.impl_onmyoji_service import impl_house, impl_initialization, impl_explore, impl_six
from src.service.impl_onmyoji_service.impl_six import current_count, deal_event
from src.utils.my_logger import logger


class TestComplexService(TestCase):
    def test_auto_setup(self):
        """
         0 云手机-001
         1 夜神模拟器
         2 平板
         3 手机
         4 云手机-002
        :return:
        """
        ComplexService.auto_setup("1")

    def test_auto_setup_hwnd1(self):
        # 初始化
        # ComplexService.auto_setup("0",0)
        hwnd = ImageService.find_hwnd(WinProcessName.phone_exe, WinClassName.phone_home)
        logger.debug("句柄{}", hwnd)
        for i in hwnd:
            logger.debug("登录")
            ImageService.touch_windows(i, Onmyoji.phone_DL)

    def test_auto_setup_hwnd2(self):
        # 初始化
        # ComplexService.auto_setup("0",0)
        hwnd = ImageService.find_hwnd('notepad.exe', 'Notepad')
        logger.debug("句柄{}", hwnd)
        for i in hwnd:
            logger.debug("点击")
            ImageService.touch_windows(i, Onmyoji.phone_DL)

    def test_fight(self):
        ComplexService.auto_setup("0")
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
        ComplexService.auto_setup("0")
        logger.debug("开始")
        now = datetime.datetime.now()
        ComplexService.fight_end(Onmyoji.border_ZDSL, Onmyoji.border_ZDSB,
                                 Onmyoji.border_ZCTZ, Onmyoji.border_TCTZ, Onmyoji.border_GRJJ,
                                 None, 300, 1)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_swipe_floor(self):
        ComplexService.auto_setup("0")
        logger.debug("开始")
        now = datetime.datetime.now()
        ComplexService.swipe_floor(Onmyoji.awaken_C, Onmyoji.awaken_SC, 1, 5)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_top_addition(self):
        ComplexService.auto_setup("1")
        logger.debug("开始")
        now = datetime.datetime.now()
        type1 = 2
        if type1 == 0:
            logger.debug("觉醒加成")
            ComplexService.top_addition(Onmyoji.soul_BQ_JC, Onmyoji.soul_BQ_YHJC, Onmyoji.soul_BQ_JCK,
                                        Onmyoji.soul_BQ_JCG, 1)
        elif type1 == 1:
            logger.debug("御魂加成")
            ComplexService.top_addition(Onmyoji.soul_BQ_JC, Onmyoji.soul_BQ_YHJC, Onmyoji.soul_BQ_JCK,
                                        Onmyoji.soul_BQ_JCG, 1)
        elif type1 == 2:
            logger.debug("经验加成")
            ComplexService.top_addition(Onmyoji.explore_JC, Onmyoji.explore_JYJC, Onmyoji.explore_JCK,
                                        Onmyoji.explore_JCG, 0)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_debris_fight(self):
        """
        式神碎片
        :return: 
        """
        ComplexService.auto_setup("1")
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
        ComplexService.auto_setup("1")
        logger.debug("开始")
        now = datetime.datetime.now()
        impl_house.get_optimal_card()
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_card(self):
        logger.debug("结界卡识别")
        warnings.simplefilter('ignore', ResourceWarning)
        ComplexService.auto_setup("1")
        now = datetime.datetime.now()
        logger.debug(impl_house.get_card_type(Onmyoji.foster_JJK_TG, 0))
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_left_card(self):
        logger.debug("左侧结界卡识别")
        warnings.simplefilter('ignore', ResourceWarning)
        ComplexService.auto_setup("1")
        now = datetime.datetime.now()
        result = impl_house.get_card_left_type(Onmyoji.foster_JJK_WXTG)
        logger.debug(result)
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_card_word(self):
        logger.debug("结界卡识别")
        ComplexService.auto_setup("1")
        now = datetime.datetime.now()
        result = impl_house.get_card_type_word(Onmyoji.foster_JJK_LXTG, Onmyoji.foster_JJK_GYWZ, 0)
        logger.debug(result)
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_return_home(self):
        now = datetime.datetime.now()
        logger.debug("返回首页")
        # 初始化测试任务信息
        game_projects = GameProjects()
        game_projects_relation = GameProjectsRelation()
        game_account = Mapper.select_game_account("2")
        game_project = GameProject()
        game_project.project_name = "登录"
        game_task = [game_projects, game_projects_relation, game_account, game_project]
        ComplexService.auto_setup("1")
        impl_initialization.initialization(game_task, 1)
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_calculate_proportion(self):
        """
        计算比例
        :return:
        """
        ComplexService.auto_setup("1")
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

    def test_automatic_rotation_type_god(self):
        logger.debug("测试-开始")
        now = datetime.datetime.now()
        ComplexService.auto_setup("1")
        impl_explore.automatic_rotation_type_god()
        logger.debug("测试-结束")
        now1 = datetime.datetime.now()
        logger.debug(now1 - now)

    def test_six_moon_event(self):
        logger.debug("测试六道之门：月之海-回合事件")
        now = datetime.datetime.now()
        ComplexService.auto_setup("1")
        current_result = [("技能", "柔风抱暖")]
        for i in range(20):
            logger.debug("测试-第{}回合", i + 1)
            logger.debug("测试-当前秘宝")
            current_count(current_result, "秘宝")
            logger.debug("测试-当前技能")
            current_count(current_result, "技能")
            logger.debug("测试-回合事件")
            if i < 1:
                current_result = deal_event("月之海", current_result, 1)
            else:
                current_result = deal_event("月之海", current_result, 4)
            is_advance = ImageService.exists(Onmyoji.six_moon_KQ)
            if is_advance:
                logger.debug("月之海结束")
        logger.debug("测试-结束")
        now1 = datetime.datetime.now()
        logger.debug(now1 - now)

    def test_six_moon_skill(self):
        logger.debug("测试六道之门：月之海-选择技能")
        now = datetime.datetime.now()
        ComplexService.auto_setup("1")
        # 月之海，技能+优先级+当前等级，按柔风抱暖、六道暴虐、细雨化屏、妖力化身选取
        skill_list = [Onmyoji.six_moon_JN_RFBN, Onmyoji.six_moon_JN_LDBN, Onmyoji.six_moon_JN_XYHP,
                      Onmyoji.six_moon_JN_YLHS]
        impl_six.select_skills(skill_list, refresh_count=1)
        logger.debug("测试-结束")
        now1 = datetime.datetime.now()
        logger.debug(now1 - now)

    def test_six_moon_rare(self):
        logger.debug("测试六道之门：月之海-选择秘宝")
        now = datetime.datetime.now()
        ComplexService.auto_setup("1")
        # 月之海，秘宝,攻击御守，火之卷
        rare_list = [Onmyoji.six_moon_MB_GJYS, Onmyoji.six_moon_MB_HZJ]
        impl_six.select_skills(rare_list, refresh_count=3)
        logger.debug("测试-结束")
        now1 = datetime.datetime.now()
        logger.debug(now1 - now)

    def test_six_moon_check_skill(self):
        logger.debug("测试六道之门：月之海-多线程选择技能")
        now = datetime.datetime.now()
        ComplexService.auto_setup("1")
        # 月之海，技能+优先级+当前等级，按柔风抱暖、六道暴虐、细雨化屏、妖力化身选取
        skill_list = [Onmyoji.six_moon_JN_RFBN, Onmyoji.six_moon_JN_LDBN, Onmyoji.six_moon_JN_XYHP,
                      Onmyoji.six_moon_JN_YLHS]
        skill = impl_six.check_list(skill_list)
        logger.debug(skill)
        logger.debug("测试-结束")
        now1 = datetime.datetime.now()
        logger.debug(now1 - now)

    def test_six_moon_check_evnet(self):
        logger.debug("测试六道之门：月之海-多线程选择事件")
        now = datetime.datetime.now()
        ComplexService.auto_setup("1")
        # 月之海，技能+优先级+当前等级，按柔风抱暖、六道暴虐、细雨化屏、妖力化身选取
        event_list = [Onmyoji.six_moon_YXXZ, Onmyoji.six_moon_SJ_XZY, Onmyoji.six_moon_SJ_AZ, Onmyoji.six_moon_SJ_SM,
                      Onmyoji.six_moon_SJ_HD, Onmyoji.six_moon_SJ_NX]
        skill = impl_six.check_list(event_list)
        logger.debug(skill)
        logger.debug("测试-结束")
        now1 = datetime.datetime.now()
        logger.debug(now1 - now)

    def test_six_moon_check_rare(self):
        logger.debug("测试六道之门：月之海-多线程选择秘宝")
        now = datetime.datetime.now()
        ComplexService.auto_setup("1")
        # 月之海，秘宝,攻击御守，火之卷
        rare_list = [Onmyoji.six_moon_MB_GJYS, Onmyoji.six_moon_MB_HZJ]
        skill = impl_six.check_list(rare_list)
        logger.debug(skill)
        logger.debug("测试-结束")
        now1 = datetime.datetime.now()
        logger.debug(now1 - now)
