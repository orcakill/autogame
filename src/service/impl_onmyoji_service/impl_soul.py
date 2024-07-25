# @Time: 2023年09月01日 18:18
# @Author: orcakill
# @File: impl_soul.py
# @Description: 御魂战斗  八岐大蛇-魂一、魂十、魂十一、魂十二，业原火、
import datetime
import time

from src.dao.mapper import Mapper
from src.model.enum import Onmyoji
from src.model.models import GameProjectsRelation, GameProject, GameAccount, GameDevice, GameProjectLog
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.impl_onmyoji_service import impl_initialization
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
    # 战斗用时列表
    time_fight_list = []
    # 项目信息
    (game_projects_relation, game_account,
     game_project, game_devices) = (GameProjectsRelation(game_task[1]), GameAccount(game_task[2]),
                                    GameProject(game_task[3]), GameDevice(game_task[4]))
    # 项目名称
    project_name = game_project.project_name
    # 项目战斗次数
    fight_time = game_projects_relation.project_num_times
    if fight_time is None:
        fight_time = 40
    # 层数-默认八岐大蛇 魂十一
    fight_layer = Onmyoji.soul_BQ_HELEVEN
    # 滑动方向,默认向下滑动
    fight_swipe = 1
    # 战斗胜利次数
    num_win = 0
    # 战斗失败次数
    num_fail = 0
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
    logger.debug("判断右侧是否有御魂自选")
    is_self_selection = ImageService.touch(Onmyoji.soul_BQ_YHZX)
    if is_self_selection:
        logger.debug("返回")
        ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH)
        # 默认锁定阵容
    is_unlock = False
    for i in range(fight_time):
        time_fight_start = time.time()
        logger.debug("{}御魂-挑战{}次", project_name, i + 1)
        if is_unlock:
            logger.debug("本次锁定阵容")
            ImageService.touch(Onmyoji.soul_BQ_SDZR)
        ImageService.touch(Onmyoji.soul_BQ_TZ)
        logger.debug("检查是否自动战斗中")
        is_auto = ImageService.exists(Onmyoji.soul_BQ_ZD, timeouts=10)
        if not is_auto:
            logger.debug("拒接悬赏")
            ComplexService.refuse_reward()
            logger.debug("点击可能的准备")
            is_unlock = ImageService.touch(Onmyoji.soul_BQ_ZB)
            logger.debug("检查是否存在御魂自选")
            is_select_soul = ImageService.exists(Onmyoji.soul_BQ_SYJC)
            if is_select_soul:
                logger.debug("点击御魂自选返回")
                ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH)
            logger.debug("检查是否超时,重新开启加成")
            ImageService.touch(Onmyoji.soul_BQ_QD)
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
    # 记录项目执行结果
    game_project_log = GameProjectLog(project_id=game_project.id, account_id=game_account.id, device_id=game_devices.id,
                                      result='八岐大蛇战斗完成', cost_time=int(time_all),
                                      fight_time=time_fight_all, fight_times=len_time_fight_list, fight_win=num_win,
                                      fight_fail=num_fail,
                                      fight_avg=time_fight_avg)
    Mapper.save_game_project_log(game_project_log)
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
    # 战斗失败次数
    num_fail = 0
    # 战斗用时列表
    time_fight_list = []
    # 项目信息
    (game_projects_relation, game_account,
     game_project, game_devices) = (GameProjectsRelation(game_task[1]), GameAccount(game_task[2]),
                                    GameProject(game_task[3]), GameDevice(game_task[4]))
    # 项目战斗次数
    fight_time = game_projects_relation.project_num_times
    # 战斗胜利次数
    num_win = 0
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
    # 记录项目执行结果
    game_project_log = GameProjectLog(project_id=game_project.id, account_id=game_account.id, device_id=game_devices.id,
                                      result='业原火完成', cost_time=int(time_all),
                                      fight_time=time_fight_all, fight_times=len_time_fight_list, fight_win=num_win,
                                      fight_fail=num_fail,
                                      fight_avg=time_fight_avg)
    Mapper.save_game_project_log(game_project_log)
    logger.debug("本轮{}御魂挑战，总用时{}秒，战斗总用时{}秒,平均战斗用时{}秒，挑战{}次，胜利{}次，失败{}次",
                 game_project.project_name, round(time_all, 3), time_fight_all, time_fight_avg, len_time_fight_list,
                 num_win, num_fail)


def soul_fight_sun(game_task: []):
    """
    日轮之陨
    :param game_task: 项目组信息
    :return:
    """
    # 开始时间
    time_start = time.time()
    # 战斗胜利次数
    num_win = 0
    # 战斗失败次数
    num_fail = 0
    # 项目信息
    (game_projects_relation, game_account,
     game_project, game_devices) = (GameProjectsRelation(game_task[1]), GameAccount(game_task[2]),
                                    GameProject(game_task[3]), GameDevice(game_task[4]))
    # 项目战斗次数
    fight_time = game_projects_relation.project_num_times
    if not fight_time or fight_time is None:
        fight_time = 50
    # 战斗用时列表
    time_fight_list = []
    for i in range(3):
        logger.debug("日轮之陨-进入探索")
        ImageService.touch(Onmyoji.home_TS)
        logger.debug("日轮之陨-点击御魂图标")
        ImageService.touch(Onmyoji.soul_RLZY_YHTB)
        logger.debug("日轮之陨-选择")
        ImageService.touch(Onmyoji.soul_RLZY_XZ)
        logger.debug("日轮之陨-选择三层")
        ImageService.touch(Onmyoji.soul_RLZY_SC)
        logger.debug("判断是否在日轮之陨首页")
        is_home = ImageService.exists(Onmyoji.soul_RLZY_RLZYSY)
        if is_home:
            break
        else:
            ComplexService.refuse_reward()
    logger.debug("锁定阵容")
    ImageService.touch(Onmyoji.soul_RLZY_SDZR)
    # 默认锁定阵容
    is_lock = False
    for i in range(fight_time):
        time_fight_start = time.time()
        logger.debug("判断是否无加成次数")
        is_add = ImageService.exists(Onmyoji.soul_RLZY_WJC, threshold=0.9)
        if is_add:
            logger.debug("无加成,退出")
            break
        logger.debug("日轮之陨-挑战{}次", i + 1)
        if is_lock:
            logger.debug("日轮之陨-本次锁定阵容")
            ImageService.touch(Onmyoji.soul_BQ_SDZR)
        is_fight = ImageService.touch(Onmyoji.soul_BQ_TZ)
        if not is_fight:
            # 拒接悬赏
            ComplexService.refuse_reward()
            logger.debug("日轮之陨-点击可能的准备")
            is_lock = ImageService.touch(Onmyoji.soul_BQ_ZB)
        logger.debug("日轮之陨-等待战斗结果")
        is_result = ComplexService.fight_end(Onmyoji.soul_RLZY_ZDSL, Onmyoji.soul_RLZY_ZDSB, Onmyoji.soul_RLZY_ZCTZ,
                                             Onmyoji.soul_RLZY_TCTZ, Onmyoji.soul_RLZY_TZ, None, 100, 2)
        # 记录战斗结果
        if is_result in [Onmyoji.soul_RLZY_ZDSL, Onmyoji.soul_RLZY_TCTZ]:
            logger.debug("日轮之陨-战斗胜利")
            num_win = num_win + 1
        elif is_result in [Onmyoji.soul_RLZY_ZCTZ]:
            logger.debug("日轮之陨-战斗失败")
            num_fail = num_fail + 1
        elif is_result in [Onmyoji.soul_RLZY_TZ]:
            logger.debug("日轮之陨-未挑战,可能无痴劵,再点击2次")
            ImageService.touch(Onmyoji.soul_BQ_TZ, wait=5)
            is_fight = ImageService.touch(Onmyoji.soul_BQ_TZ, wait=5)
            if is_fight:
                logger.debug("无痴劵，退出战斗循环")
                break
        time_fight_end = time.time()
        time_fight_time = time_fight_end - time_fight_start
        logger.debug("本次日轮之陨，用时{}秒", round(time_fight_time))
        time_fight_list.append(time_fight_time)
        if is_result in [Onmyoji.soul_RLZY_ZCTZ]:
            logger.debug("战斗失败，退出循环")
            break
    logger.debug("日轮之陨-返回首页")
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    logger.debug("日轮之陨-返回首页")
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    logger.debug("日轮之陨-确认返回首页")
    impl_initialization.return_home(game_task)
    # 日轮之陨-结束时间
    time_end = time.time()
    # 日轮之陨-总用时
    time_all = time_end - time_start
    # 日轮之陨-战斗次数
    len_time_fight_list = len(time_fight_list)
    # 日轮之陨-战斗总用时
    time_fight_all = round(sum(time_fight_list))
    # 日轮之陨-平均战斗用时
    time_fight_avg = 0
    if len_time_fight_list > 0:
        logger.debug("日轮之陨-计算平均战斗用时")
        time_fight_avg = round(sum(time_fight_list) / len(time_fight_list), 3)
    # 记录项目执行结果
    game_project_log = GameProjectLog(project_id=game_project.id, account_id=game_account.id, device_id=game_devices.id,
                                      result='日轮之陨完成', cost_time=int(time_all),
                                      fight_time=time_fight_all, fight_times=len_time_fight_list, fight_win=num_win,
                                      fight_fail=num_fail,
                                      fight_avg=time_fight_avg)
    Mapper.save_game_project_log(game_project_log)
    logger.debug("本轮日轮之陨御魂挑战，总用时{}秒，战斗总用时{}秒,平均战斗用时{}秒，挑战{}次，胜利{}次，失败{}次",
                 round(time_all, 3), time_fight_all, time_fight_avg, len_time_fight_list, num_win, num_fail)


def soul_fight_sea(game_task: [], fight: int = 0):
    """
    永生之海
    :param fight: 战斗开关，0 为根据掉落御魂时间来  1强制战斗
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
    # 项目信息
    (game_projects_relation, game_account,
     game_project, game_devices) = (GameProjectsRelation(game_task[1]), GameAccount(game_task[2]),
                                    GameProject(game_task[3]), GameDevice(game_task[4]))
    today = datetime.date.today()
    # 项目战斗次数
    fight_time = game_projects_relation.project_num_times
    if not fight_time or fight_time is None:
        fight_time = 50
    # 获取本日是周几（周一为0，周日为6）
    weekday = today.weekday() + 1
    if weekday == 5 or fight == 1:
        for i in range(3):
            logger.debug("永生之海-进入探索")
            ImageService.touch(Onmyoji.home_TS)
            logger.debug("永生之海-点击御魂图标")
            ImageService.touch(Onmyoji.soul_YSZH_YHTB)
            logger.debug("永生之海-选择")
            ImageService.touch(Onmyoji.soul_YSZH_XZ)
            logger.debug("永生之海-选择四层")
            ImageService.touch(Onmyoji.soul_YSZH_SC)
            logger.debug("判断是否在永生之海首页")
            is_home = ImageService.touch(Onmyoji.soul_YSZH_YSZHSY)
            if is_home:
                break
            else:
                ComplexService.refuse_reward()
        logger.debug("锁定阵容")
        ImageService.touch(Onmyoji.soul_YSZH_SDZR)
        # 默认锁定阵容
        is_lock = False
        for i in range(fight_time):
            time_fight_start = time.time()
            logger.debug("判断是否无加成次数")
            is_add = ImageService.touch(Onmyoji.soul_YSZH_WJC)
            if is_add:
                logger.debug("无加成,退出")
                break
            logger.debug("永生之海-挑战{}次", i + 1)
            if is_lock:
                logger.debug("永生之海-本次锁定阵容")
                ImageService.touch(Onmyoji.soul_BQ_SDZR)
            is_fight = ImageService.touch(Onmyoji.soul_BQ_TZ)
            if not is_fight:
                # 拒接悬赏
                ComplexService.refuse_reward()
                logger.debug("永生之海-点击可能的准备")
                is_lock = ImageService.touch(Onmyoji.soul_BQ_ZB)
            logger.debug("永生之海-等待战斗结果")
            is_result = ComplexService.fight_end(Onmyoji.soul_YSZH_ZDSL, Onmyoji.soul_YSZH_ZDSB, Onmyoji.soul_YSZH_ZCTZ,
                                                 Onmyoji.soul_YSZH_TCTZ, Onmyoji.soul_YSZH_TZ, None, 100, 2)
            # 记录战斗结果
            if is_result in [Onmyoji.soul_YSZH_ZDSL, Onmyoji.soul_YSZH_TCTZ]:
                logger.debug("永生之海-战斗胜利")
                num_win = num_win + 1
            elif is_result in [Onmyoji.soul_YSZH_ZCTZ]:
                logger.debug("永生之海-战斗失败,退出循环")
                num_fail = num_fail + 1
                break
            time_fight_end = time.time()
            time_fight_time = time_fight_end - time_fight_start
            logger.debug("本次永生之海，用时{}秒", round(time_fight_time))
            time_fight_list.append(time_fight_time)
            if is_result in [Onmyoji.soul_YSZH_ZCTZ]:
                logger.debug("永生之海-战斗失败,退出循环")
                break
        logger.debug("永生之海-返回首页")
        ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
        logger.debug("永生之海-返回首页")
        ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
        logger.debug("永生之海-确认返回首页")
        impl_initialization.return_home(game_task)
    # 永生之海-结束时间
    time_end = time.time()
    # 永生之海-总用时
    time_all = time_end - time_start
    # 永生之海-战斗次数
    len_time_fight_list = len(time_fight_list)
    # 永生之海-战斗总用时
    time_fight_all = round(sum(time_fight_list))
    # 永生之海-平均战斗用时
    time_fight_avg = 0
    if len_time_fight_list > 0:
        logger.debug("永生之海-计算平均战斗用时")
        time_fight_avg = round(sum(time_fight_list) / len(time_fight_list), 3)
    # 记录项目执行结果
    game_project_log = GameProjectLog(project_id=game_project.id, account_id=game_account.id, device_id=game_devices.id,
                                      result='永生之海战斗完成', cost_time=int(time_all),
                                      fight_time=time_fight_all, fight_times=len_time_fight_list, fight_win=num_win,
                                      fight_fail=num_fail,
                                      fight_avg=time_fight_avg)
    Mapper.save_game_project_log(game_project_log)
    logger.debug("本轮永生之海御魂挑战，总用时{}秒，战斗总用时{}秒,平均战斗用时{}秒，挑战{}次，胜利{}次，失败{}次",
                 round(time_all, 3), time_fight_all, time_fight_avg, len_time_fight_list, num_win, num_fail)
