"""
# @Time: 2023年08月23日23:56
# @Author: orcakill
# @File: activity_service.py
# @Description: 活动
"""
import time

from src.model.enum import Onmyoji, Cvstrategy
from src.model.models import GameAccount
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.ocr_service import OcrService
from src.service.onmyoji_service import OnmyojiService
from src.utils.my_logger import logger

# 服务接口
image_service = ImageService()
complex_service = ComplexService()
ocr_service = OcrService()


class ActivityService:
    @staticmethod
    def current_activity(game_task: []):
        # 当前活动 2023-08-23 至 2023-08-30   爬塔-真火切磋
        ActivityService.climbing_tower_20230823(game_task)

    @staticmethod
    def current_lbs(game_task: []):
        # 当前活动 2023-08-23 至 2023-08-30   lbs鬼王
        ActivityService.lbs_20230823(game_task)

    @staticmethod
    def climbing_tower_20230823(game_task: []):
        """
        爬塔  真火切磋
        :param game_task: 任务信息
        :return:
        """
        game_account = GameAccount(game_task[2])
        logger.debug("爬塔-真火切磋-{}", game_account.role_name)
        # 初始化图片路径
        p_buy = r"活动\20230823\爬塔\购买"
        p_fight = r"活动\20230823\爬塔\挑战"
        p_fight_win = r"活动\20230823\爬塔\战斗胜利"
        p_fight_fail = r"活动\20230823\爬塔\战斗失败"
        p_fight_again = r"活动\20230823\爬塔\再次挑战"
        p_fight_quit = r"活动\20230823\爬塔\退出挑战"
        p_return = r"活动\20230823\爬塔\返回"
        p_reward = r"活动\20230823\爬塔\获得奖励"
        p_select = r"活动\20230823\爬塔\选定"
        p_soul_select = r"活动\20230823\爬塔\御魂选定"
        p_step1 = r"活动\20230823\爬塔\入口1"
        p_step2 = r"活动\20230823\爬塔\入口2"
        p_shiShenLu = r"活动\20230823\爬塔\式神录"
        p_top_plus_sign = r"活动\20230823\爬塔\顶部加号"
        p_unlock = r"活动\20230823\爬塔\解锁阵容"
        p_double_up_arrow = r"活动\20230823\爬塔\双向上箭头"
        p_gift = r"活动\20230823\爬塔\礼包"
        p_chat = r"活动\20230823\爬塔\左侧聊天"
        # 开始活动
        logger.debug("进入")
        image_service.touch(p_step1)
        image_service.touch(p_step2)
        logger.debug("判断是否有选定")
        is_select = image_service.exists(p_select)
        if is_select:
            image_service.touch(p_soul_select)
            image_service.touch(p_select)
        logger.debug("买票")
        coordinate1 = image_service.exists(p_top_plus_sign)
        coordinate2 = image_service.exists(p_shiShenLu)
        if coordinate1 and coordinate2:
            coordinate3 = (coordinate2[0], coordinate1[1])
            logger.debug("进入买票")
            image_service.touch_coordinate(coordinate3)
            logger.debug("最大票数")
            image_service.touch(p_double_up_arrow)
            logger.debug("购买")
            image_service.touch(p_buy)
            is_reward = complex_service.get_reward(p_reward)
            if not is_reward:
                logger.debug("没票了,点击一次礼包退出")
                complex_service.get_reward(p_gift)
        logger.debug("锁定阵容")
        image_service.touch(p_unlock)
        for i in range(240):
            logger.debug("{}:第{}次挑战", game_account.role_name, i + 1)
            is_fight = image_service.touch(p_fight)
            if not is_fight:
                logger.debug("挑战未点击成功，判断是否有退出挑战")
                image_service.touch(p_fight_quit)
                logger.debug("挑战未点击成功，判断是否进入左侧聊天")
                image_service.touch(p_chat)
            time.sleep(3)
            logger.debug("等待战斗结果")
            is_result = complex_service.fight_end(p_fight_win, p_fight_fail, p_fight_again, p_fight_quit, p_fight, None,60,
                                                  3)
            if is_result is None:
                is_gift = complex_service.get_reward(p_gift)
                if is_gift:
                    logger.debug("需要买票，可能已无票")
                    break
        logger.debug("返回首页")
        image_service.touch(p_return)
        image_service.touch(p_return)

    @staticmethod
    def lbs_20230823(game_task: []):
        """
        lbs鬼王 20230823
        :param game_task:
        :return:
        """
        p_RK = r"活动\20230823\LBS鬼王\LBS鬼王入口"
        p_RK1 = r"活动\20230823\LBS鬼王\入口1"
        p_ZB = r"活动\20230823\LBS鬼王\准备"
        p_CJ = r"活动\20230823\LBS鬼王\创建"
        p_fight_win = r"活动\20230823\LBS鬼王\战斗胜利"
        p_fight_fail = r"活动\20230823\LBS鬼王\战斗失败"
        p_fight_again = r"活动\20230823\LBS鬼王\再次挑战"
        p_fight_quit = r"活动\20230823\LBS鬼王\退出挑战"
        p_SYL = r"活动\20230823\LBS鬼王\所有人"
        p_TZ = r"活动\20230823\LBS鬼王\挑战"
        p_TEAM = r"活动\20230823\LBS鬼王\组队挑战"
        logger.debug("进入现世妖约")
        for i in range(50):
            logger.debug("点击LBS鬼王入口")
            is_entrance = image_service.touch(p_RK)
            if not is_entrance:
                logger.debug("点击首页入口")
                image_service.touch(p_RK1)
            logger.debug("点击组队挑战")
            image_service.touch(p_TEAM, wait=3, cvstrategy=Cvstrategy.default)
            logger.debug("点击所有人")
            image_service.touch(p_SYL)
            logger.debug("点击创建")
            image_service.touch(p_CJ, cvstrategy=Cvstrategy.default)
            logger.debug("点击挑战")
            is_fight = image_service.touch(p_TZ)
            if not is_fight:
                logger.debug("点击创建后，无挑战")
                is_team = image_service.exists(p_TEAM, wait=3, cvstrategy=Cvstrategy.default)
                if is_team:
                    logger.debug("有组队，可能无挑战次数，退出循环")
                    break
            logger.debug("点击准备")
            image_service.touch(p_ZB, wait=5)
            logger.debug("等待战斗结果")
            complex_service.fight_end(p_fight_win, p_fight_fail, p_fight_again, p_fight_quit, p_TEAM, None,300, 1)
        logger.debug("返回首页")
        image_service.touch(Onmyoji.comm_FH_YSJHDBSCH)
        image_service.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
        logger.debug("确认返回首页")
        OnmyojiService.return_home(game_task)
