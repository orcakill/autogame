# @Time: 2023年09月01日 18:18
# @Author: orcakill
# @File: impl_soul.py
# @Description: 御魂战斗  八岐大蛇-魂一、魂十、魂十一、魂十二，业原火、
import time

from src.model.enum import Onmyoji
from src.model.models import GameAccount, GameProjectsRelation, GameProject
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.utils.my_logger import logger


def soul_fight(game_task: []):
    """
    御魂战斗  八岐大蛇
    魂一  第一次战斗检查协战，有协战上协战，没协战直接退出到首页，不开加成
    魂十  第一次战斗检查协战，有协战上协战，开加成，
    魂十一  不检查协战，不上协战，开加成
    :param game_task: 项目组信息
    :return:
    """
    # 开始时间
    time_start = time.time()
    # 战斗胜利次数
    num_win = 0
    # 战斗失败次数
    num_fail = 0
    # 结界突破战斗用时
    time_fight_list = []
    game_projects_relation = GameProjectsRelation(game_task[1])
    game_account = GameAccount(game_task[2])
    logger.debug(game_account.game_name)
    game_project = GameProject(game_task[3])
    fight_time = game_projects_relation.project_num_times
    logger.debug("进入探索")
    ImageService.touch(Onmyoji.home_TS)
    logger.debug("进入御魂")
    ImageService.touch(Onmyoji.soul_BQ_YHTB)
    logger.debug("进入八岐大蛇")
    ImageService.touch(Onmyoji.soul_BQ_XZ)
    logger.debug("开启加成")
    logger.debug("八岐大蛇-选择层号")
    if game_project.project_name == "魂一":
        ComplexService.swipe_floor(Onmyoji.soul_BQ_CZ, Onmyoji.soul_BQ_HONE, 0, 4)
    elif game_project.project_name == "魂十":
        ComplexService.swipe_floor(Onmyoji.soul_BQ_CZ, Onmyoji.soul_BQ_HTEN, 1, 4)
    elif game_project.project_name == "魂十一":
        ComplexService.swipe_floor(Onmyoji.soul_BQ_CZ, Onmyoji.soul_BQ_HELEVEN, 1, 4)
    logger.debug("开启御魂加成")
    ComplexService.top_addition(Onmyoji.soul_BQ_JC, Onmyoji.soul_BQ_YHJC, Onmyoji.soul_BQ_JCG, Onmyoji.soul_BQ_JCG,
                                1)
    logger.debug("锁定阵容")
    ImageService.touch(Onmyoji.soul_BQ_SDZR)
    # 默认锁定阵容
    is_lock = False
    for i in range(fight_time):
        time_fight_start = time.time()
        logger.debug("御魂-挑战{}次", i + 1)
        if is_lock:
            logger.debug("可能存在锁定阵容")
            ImageService.touch(Onmyoji.soul_BQ_SDZR)
        is_fight = ImageService.touch(Onmyoji.soul_BQ_TZ)
        if not is_fight:
            logger.debug("点击可能的准备")
            is_lock = ImageService.touch(Onmyoji.soul_BQ_ZB)
        if i == 0:
            logger.debug("喂食")
            is_pets = ImageService.touch(Onmyoji.soul_BQ_CW, wait=5)
            if is_pets:
                logger.debug("点击喂食")
                ImageService.touch(Onmyoji.soul_BQ_WS)
                logger.debug("获得奖励")
                ComplexService.get_reward(Onmyoji.soul_BQ_HDJL)
        logger.debug("等待战斗结果")
        is_result = ComplexService.fight_end(Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_ZDSB, Onmyoji.soul_BQ_ZCTZ,
                                             Onmyoji.soul_BQ_TCTZ, Onmyoji.soul_BQ_TZ, 60, 1)
        # 记录战斗结果
        if is_result in [Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_TCTZ]:
            num_win = num_win + 1
        elif is_result in [Onmyoji.soul_BQ_ZCTZ]:
            num_fail = num_fail + 1
        if i == 0:
            logger.debug("发现宝藏")
            ComplexService.get_reward(Onmyoji.soul_BQ_FXBZ)
        time_fight_end = time.time()
        time_fight_time = time_fight_end - time_fight_start
        logger.debug("本次{}，用时{}秒", game_project.project_name, round(time_fight_time))
        time_fight_list.append(time_fight_time)
    time.sleep(3)
    logger.debug("关闭御魂加成")
    ComplexService.top_addition(Onmyoji.soul_BQ_JC, Onmyoji.soul_BQ_YHJC, Onmyoji.soul_BQ_JCG, Onmyoji.soul_BQ_JCG,
                                0)
    logger.debug("御魂-返回首页")
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    logger.debug("御魂-返回首页")
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    # 御魂结束时间
    time_end = time.time()
    # 御魂总用时
    time_all = time_end - time_start
    # 御魂战斗总用时
    time_fight_all = round(sum(time_fight_list))
    # 御魂战斗次数
    len_time_fight_list = len(time_fight_list)
    # 御魂平均战斗用时
    time_fight_avg = 0
    if len_time_fight_list > 0:
        time_fight_avg = round(sum(time_fight_list) / len(time_fight_list), 3)
    logger.debug("本轮{}御魂挑战，总用时{}秒，战斗总用时{}秒,平均战斗用时{}秒，挑战{}次，胜利{}次，失败{}次",
                 game_project.project_name, round(time_all, 3), time_fight_all, time_fight_avg, len_time_fight_list,
                 num_win, num_fail)