"""
# @Time: 2023年11月30日17:51
# @Author: orcakill
# @File: impl_six.py
# @Description: 六道之门(月之海)
"""
import time

from src.model.enum import Onmyoji
from src.model.models import GameAccount, GameProject, GameDevices, GameProjectsRelation
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.utils.my_logger import logger


def sea_moon(game_task: []):
    # 开始时间
    time_start = time.time()
    # 项目信息
    (game_projects_relation, game_account,
     game_project, game_devices) = (GameProjectsRelation(game_task[1]), GameAccount(game_task[2]),
                                    GameProject(game_task[3]), GameDevices(game_task[4]))
    #  战斗次数
    fight_times = game_projects_relation.project_num_times
    logger.debug("检查是否是六道之门-月之海首页")
    is_home = ImageService.exists(Onmyoji.six_moon_YZHSY)
    is_open = ImageService.exists(Onmyoji.six_moon_KQ)
    if not is_home or not is_open:
        logger.debug("当前不是六道之门-月之海首页")
        logger.debug("拒接协战")
        ComplexService.refuse_reward()
        logger.debug("探索")
        ImageService.touch(Onmyoji.home_TS)
        logger.debug("六道之门入口")
        ImageService.touch(Onmyoji.six_moon_LDZMRK)
        logger.debug("月之海入口")
        is_six_moon = ImageService.touch(Onmyoji.six_moon_YZHRK)
        if not is_six_moon:
            logger.debug("无月之海入口，更替")
            ImageService.touch(Onmyoji.six_moon_GT)
            logger.debug("选择月之海")
            ImageService.touch(Onmyoji.six_moon_XZYZH)
            logger.debug("重新点击月之海入口")
            ImageService.touch(Onmyoji.six_moon_YZHRK)
        logger.debug("重新检查是否是六道之门-月之海首页")
        is_home = ImageService.exists(Onmyoji.six_moon_YZHSY)
        is_open = ImageService.exists(Onmyoji.six_moon_KQ)
    if is_home and is_open:
        logger.debug("月之海首页")
        for i in range(fight_times):
            logger.debug("第{}次月之海", i + 1)
            logger.debug("确定")
            ImageService.touch(Onmyoji.six_moon_QD)
            logger.debug("60体力开启")
            ImageService.touch(Onmyoji.six_moon_KQ60TL)
            logger.debug("选择柔风抱暖")
            ComplexService.touch_two(Onmyoji.six_moon_JN_RFBN, Onmyoji.six_moon_XZJN, 1, 1)
            for i_fight in range(20):
                logger.debug("第{}回合", i_fight)
                logger.debug("检查当前是否首领战")
                is_boss = ImageService.exists(Onmyoji.six_moon_YXXZ)
                if not is_boss:
                    logger.debug("处理回合事件")
                logger.debug("首领战")

    return True


def deal_event():
    """
    回合事件
    :return:
    """
    # 月之海，按星之屿、鏖战、神秘、混沌、宁息
    logger.debug("处理事件")
    logger.debug("获取当前事件")
    logger.debug("根据事件优先级选择点击")
    logger.debug("检查鏖战")
    is_event = ImageService.touch(Onmyoji.six_moon_SJ_AZ)
    if is_event:
        logger.debug("点击右侧普通")
        ImageService.touch_all_coordinate(Onmyoji.six_moon_PT, rank=2)
        logger.debug("点击挑战")
        ImageService.touch(Onmyoji.six_moon_TZ)
        logger.debug("等待战斗结束")
        ImageService.exists(Onmyoji.six_moon_WXZC)
        logger.debug("检查技能")
