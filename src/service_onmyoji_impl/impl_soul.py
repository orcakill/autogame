# @Time: 2023年09月01日 18:18
# @Author: orcakill
# @File: impl_soul.py
# @Description: 御魂战斗  八岐大蛇-魂一、魂十、魂十一、魂十二，业原火、
import time

from src.model.enum import Onmyoji
from src.model.models import GameProjectsRelation, GameProject
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service_onmyoji_impl import impl_initialization
from src.utils.my_logger import logger


def soul_fight(game_task: []):
    """
    御魂战斗  八岐大蛇
    魂一   不御魂开加成
    魂十   开御魂加成
    魂十一  开御魂加成
    :param game_task: 项目组信息
    :return:
    """
    # 开始时间
    time_start = time.time()
    # 战斗胜利次数
    num_win = 0
    # 战斗失败次数
    num_fail = 0
    # 战斗用时列表
    time_fight_list = []
    # 项目组项目关系
    game_projects_relation = GameProjectsRelation(game_task[1])
    # 项目信息
    game_project = GameProject(game_task[3])
    # 项目名称
    project_name = game_project.project_name
    # 项目战斗次数
    fight_time = game_projects_relation.project_num_times
    # 层数-默认八岐大蛇 魂十一
    fight_layer = Onmyoji.soul_BQ_HELEVEN
    # 滑动方向,默认向下滑动
    fight_swipe = 1
    if project_name == "魂一":
        fight_layer = Onmyoji.soul_BQ_HONE
    elif project_name == "魂十":
        fight_layer = Onmyoji.soul_BQ_HTEN
    logger.debug(project_name)
    for i in range(3):
        logger.debug("{}-进入探索", project_name)
        ImageService.touch(Onmyoji.home_TS)
        logger.debug("{}-点击御魂图标", project_name)
        ImageService.touch(Onmyoji.soul_BQ_YHTB)
        logger.debug("{}-选择", project_name)
        ImageService.touch(Onmyoji.soul_BQ_XZ)
        # 层号选择 魂一、魂十、魂十一
        logger.debug("{}-选择层号", project_name)
        ComplexService.swipe_floor(Onmyoji.soul_BQ_CZ, fight_layer, fight_swipe, 4)
        logger.debug("判断是否在{}首页", project_name)
        is_home = ImageService.touch(Onmyoji.soul_BQ_BQDSSY)
        if is_home:
            break
        else:
            ComplexService.refuse_reward()
    logger.debug("{}-开启加成", project_name)
    ComplexService.top_addition(Onmyoji.soul_BQ_JC, Onmyoji.soul_BQ_YHJC, Onmyoji.soul_BQ_JCK, Onmyoji.soul_BQ_JCG,
                                1)
    logger.debug("{}-锁定阵容", project_name)
    ImageService.touch(Onmyoji.soul_BQ_SDZR)
    # 默认锁定阵容
    is_lock = False
    for i in range(fight_time):
        time_fight_start = time.time()
        logger.debug("{}御魂-挑战{}次", project_name, i + 1)
        if is_lock:
            logger.debug("上一次战斗点击了准备，本次锁定阵容")
            ImageService.touch(Onmyoji.soul_BQ_SDZR)
        is_fight = ImageService.touch(Onmyoji.soul_BQ_TZ)
        if not is_fight:
            ComplexService.refuse_reward()
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
                                             Onmyoji.soul_BQ_TCTZ, Onmyoji.soul_BQ_TZ, None, 60, 1)
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
        logger.debug("本次{}，用时{}秒", project_name, round(time_fight_time))
        time_fight_list.append(time_fight_time)
    time.sleep(3)
    logger.debug("关闭御魂加成")
    ComplexService.top_addition(Onmyoji.soul_BQ_JC, Onmyoji.soul_BQ_YHJC, Onmyoji.soul_BQ_JCK, Onmyoji.soul_BQ_JCG,
                                0)
    logger.debug("{}-返回首页", project_name)
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    logger.debug("{}-返回首页", project_name)
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    logger.debug("确认返回首页")
    impl_initialization.return_home(game_task)
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


def soul_fight_fire(game_task: []):
    """
    业原火
    :param game_task: 项目组信息
    :return:
    """
    # 开始时间
    time_start = time.time()
    # 战斗胜利次数
    num_win = 0
    # 战斗失败次数
    num_fail = 0
    # 战斗用时列表
    time_fight_list = []
    # 项目组项目关系
    game_projects_relation = GameProjectsRelation(game_task[1])
    # 项目信息
    game_project = GameProject(game_task[3])
    # 项目战斗次数
    fight_time = game_projects_relation.project_num_times
    for i in range(3):
        logger.debug("业原火-进入探索")
        ImageService.touch(Onmyoji.home_TS)
        logger.debug("业原火-点击御魂图标")
        ImageService.touch(Onmyoji.soul_YYH_YHTB)
        logger.debug("业原火-选择")
        ImageService.touch(Onmyoji.soul_YYH_YYHTB)
        logger.debug("业原火-选择三层")
        ImageService.touch(Onmyoji.soul_YYH_SC)
        logger.debug("判断是否在业原火首页")
        is_home = ImageService.touch(Onmyoji.soul_YYH_YYHSY)
        if is_home:
            break
        else:
            ComplexService.refuse_reward()
    logger.debug("锁定阵容")
    ImageService.touch(Onmyoji.soul_YYH_SDZR)
    # 默认锁定阵容
    is_lock = False
    for i in range(fight_time):
        time_fight_start = time.time()
        logger.debug("业原火-挑战{}次", i + 1)
        if is_lock:
            logger.debug("业原火-本次锁定阵容")
            ImageService.touch(Onmyoji.soul_BQ_SDZR)
        is_fight = ImageService.touch(Onmyoji.soul_BQ_TZ)
        if not is_fight:
            # 拒接悬赏
            ComplexService.refuse_reward()
            logger.debug("业原火-点击可能的准备")
            is_lock = ImageService.touch(Onmyoji.soul_BQ_ZB)
        logger.debug("业原火-等待战斗结果")
        is_result = ComplexService.fight_end(Onmyoji.soul_YYH_ZDSL, Onmyoji.soul_YYH_ZDSB, Onmyoji.soul_YYH_ZCTZ,
                                             Onmyoji.soul_YYH_TCTZ, Onmyoji.soul_YYH_TZ, None, 100, 2)
        # 记录战斗结果
        if is_result in [Onmyoji.soul_YYH_ZDSL, Onmyoji.soul_YYH_TCTZ]:
            logger.debug("业原火-战斗胜利")
            num_win = num_win + 1
        elif is_result in [Onmyoji.soul_YYH_ZCTZ]:
            logger.debug("业原火-战斗失败")
            num_fail = num_fail + 1
        elif is_result in [Onmyoji.soul_YYH_TZ]:
            logger.debug("业原火-未挑战,可能无痴劵,再点击2次")
            ImageService.touch(Onmyoji.soul_BQ_TZ, wait=5)
            is_fight = ImageService.touch(Onmyoji.soul_BQ_TZ, wait=5)
            if is_fight:
                logger.debug("无痴劵，退出战斗循环")
                break
        time_fight_end = time.time()
        time_fight_time = time_fight_end - time_fight_start
        logger.debug("本次业原火，用时{}秒", round(time_fight_time))
        time_fight_list.append(time_fight_time)
    logger.debug("业原火-返回首页")
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    logger.debug("业原火-返回首页")
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    logger.debug("业原火-确认返回首页")
    impl_initialization.return_home(game_task)
    # 业原火-结束时间
    time_end = time.time()
    # 业原火-总用时
    time_all = time_end - time_start
    # 业原火-战斗次数
    len_time_fight_list = len(time_fight_list)
    # 业原火-战斗总用时
    time_fight_all = round(sum(time_fight_list))
    # 业原火-平均战斗用时
    time_fight_avg = 0
    if len_time_fight_list > 0:
        logger.debug("业原火-计算平均战斗用时")
        time_fight_avg = round(sum(time_fight_list) / len(time_fight_list), 3)
    logger.debug("本轮{}御魂挑战，总用时{}秒，战斗总用时{}秒,平均战斗用时{}秒，挑战{}次，胜利{}次，失败{}次",
                 game_project.project_name, round(time_all, 3), time_fight_all, time_fight_avg, len_time_fight_list,
                 num_win, num_fail)
