# @Time: 2023年09月19日 10:56
# @Author: orcakill
# @File: impl_spirit.py
# @Description: 御灵三层
import datetime
import time

from src.dao.mapper import Mapper
from src.model.enum import Onmyoji
from src.model.models import GameProjectsRelation, GameProjectLog, GameAccount, GameDevices, GameProject
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service_onmyoji_impl import impl_initialization
from src.utils.my_logger import logger


def spirit_fight(game_task: []):
    """
    御灵 三层 根据星期判断类型 周一无 周二神龙 周三白藏主 周四黑豹 周五孔雀 周六周日黑豹
    :param game_task: 任务信息
    :return: 
    """
    # 开始时间
    time_start = time.time()
    # 战斗胜利次数
    num_win = 0
    # 战斗失败次数
    num_fail = 0
    (game_projects_relation, game_account,
     game_project, game_devices) = (GameProjectsRelation(game_task[1]), GameAccount(game_task[2]),
                                    GameProject(game_task[3]), GameDevices(game_task[4]))
    # 项目战斗次数
    if game_projects_relation.project_num_times:
        fight_time = game_projects_relation.project_num_times
    else:
        fight_time = 60
    # 战斗用时列表
    time_fight_list = []
    # 获取本日
    today = datetime.date.today()
    # 获取本日是周几（周一为0，周日为6），所以加1
    weekday = today.weekday() + 1
    if weekday != 1:
        for i in range(3):
            logger.debug("御灵-进入探索")
            ImageService.touch(Onmyoji.home_TS)
            logger.debug("御灵-点击御灵图标")
            ImageService.touch(Onmyoji.spirit_YLTB)
            logger.debug("御灵-选择")
            if weekday == 2:
                logger.debug("御灵神龙")
                ImageService.touch(Onmyoji.spirit_YLSL)
            elif weekday == 3:
                logger.debug("御灵白藏主")
                ImageService.touch(Onmyoji.spirit_YLBZZ)
            elif weekday == 5:
                logger.debug("御灵孔雀")
                ImageService.touch(Onmyoji.spirit_YLKQ)
            else:
                logger.debug("御灵黑豹")
                ImageService.touch(Onmyoji.spirit_YLHB)
            logger.debug("御灵-选择三层")
            ImageService.touch(Onmyoji.spirit_SC)
            logger.debug("判断是否在御灵首页")
            is_home = ImageService.touch(Onmyoji.spirit_YLSY)
            if is_home:
                break
            else:
                ComplexService.refuse_reward()
        logger.debug("锁定阵容")
        ImageService.touch(Onmyoji.spirit_SDZR)
        # 默认锁定阵容
        is_lock = False
        for i in range(fight_time):
            time_fight_start = time.time()
            logger.debug("御灵-挑战{}次", i + 1)
            if is_lock:
                logger.debug("御灵-本次锁定阵容")
                ImageService.touch(Onmyoji.spirit_SDZR)
            is_fight = ImageService.touch(Onmyoji.spirit_TZ)
            if not is_fight:
                # 拒接悬赏
                ComplexService.refuse_reward()
                logger.debug("御灵-点击可能的准备")
                is_lock = ImageService.touch(Onmyoji.spirit_ZB)
            logger.debug("御灵-等待战斗结果")
            is_result = ComplexService.fight_end(Onmyoji.spirit_ZDSL, Onmyoji.spirit_ZDSB, Onmyoji.spirit_ZCTZ,
                                                 Onmyoji.spirit_TCTZ, Onmyoji.spirit_TZ, None, 100, 2)
            # 记录战斗结果
            if is_result in [Onmyoji.spirit_ZDSL, Onmyoji.spirit_TCTZ]:
                logger.debug("御灵-战斗胜利")
                num_win = num_win + 1
            elif is_result in [Onmyoji.spirit_ZCTZ]:
                logger.debug("御灵-战斗失败")
                num_fail = num_fail + 1
            time_fight_end = time.time()
            time_fight_time = time_fight_end - time_fight_start
            logger.debug("本次御灵，用时{}秒", round(time_fight_time))
            time_fight_list.append(time_fight_time)
            if is_result in [Onmyoji.spirit_ZCTZ]:
                logger.debug("御灵-战斗失败,退出循环")
                break
        logger.debug("御灵-返回首页")
        ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
        logger.debug("御灵-返回首页")
        ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
        logger.debug("御灵-确认返回首页")
        impl_initialization.return_home(game_task)
    else:
        logger.debug("当前周一，不打御灵")
    # 御灵-结束时间
    time_end = time.time()
    # 御灵-总用时
    time_all = time_end - time_start
    # 御灵-战斗次数
    len_time_fight_list = len(time_fight_list)
    # 御灵-战斗总用时
    time_fight_all = round(sum(time_fight_list))
    # 御灵-平均战斗用时
    time_fight_avg = 0

    if len_time_fight_list > 0:
        logger.debug("御灵-计算平均战斗用时")
        time_fight_avg = round(sum(time_fight_list) / len(time_fight_list), 3)
    # 记录项目执行结果
    game_project_log = GameProjectLog(project_id=game_project.id, role_id=game_account.id, devices_id=game_devices.id,
                                      result='觉醒战斗完成', cost_time=int(time_all),
                                      fight_times=time_fight_all, fight_win=num_win, fight_fail=num_fail,
                                      fight_avg=time_fight_avg)
    Mapper.save_game_project_log(game_project_log)
    logger.debug("本轮御灵挑战，总用时{}秒，战斗总用时{}秒,平均战斗用时{}秒，挑战{}次，胜利{}次，失败{}次",
                 round(time_all, 3), time_fight_all, time_fight_avg, len_time_fight_list, num_win, num_fail)
