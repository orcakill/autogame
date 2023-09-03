# @Time: 2023年09月01日 17:23
# @Author: orcakill
# @File: impl_awakening.py
# @Description: 觉醒
import datetime
import time

from src.model.enum import Onmyoji
from src.model.models import GameAccount, GameProjectsRelation
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.utils.my_logger import logger


def awakening(game_task: [], awakening_type: int = 0):
    """
        觉醒十 风、火、水、雷（默认雷）  开加成，选觉醒阵容
        :param awakening_times: 觉醒次数
        :param awakening_type: 默认类型
        :param game_task:  任务信息
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
    # 项目组项目关系
    game_projects_relation = GameProjectsRelation(game_task[1])
    # 账号信息
    game_account = GameAccount(game_task[2])
    fight_time = game_projects_relation.project_num_times
    if fight_time is None:
        fight_time = 1
    # 获取当前日期
    today = datetime.date.today()
    # 获取本日是周几（周一为0，周日为6）
    weekday = today.weekday() + 1
    logger.debug(game_account.game_name)
    logger.debug("进入探索")
    ImageService.touch(Onmyoji.home_TS)
    logger.debug("进入觉醒")
    is_awakening = ImageService.touch(Onmyoji.awaken_JXBT)
    if not is_awakening:
        logger.debug("未进入觉醒")
        time.sleep(30)
        logger.debug("进入探索")
        ImageService.touch(Onmyoji.home_TS)
        logger.debug("进入觉醒")
        ImageService.touch(Onmyoji.awaken_JXBT)
    logger.debug("本日周{}", weekday)
    if awakening_type != 0:
        logger.debug("修改麒麟类型")
        weekday = awakening_type
    if weekday == 1:
        logger.debug("火麒麟")
        ImageService.touch(Onmyoji.awaken_QL_H)
    elif weekday == 2:
        logger.debug("风麒麟")
        ImageService.touch(Onmyoji.awaken_QL_F)
    elif weekday == 3:
        logger.debug("水麒麟")
        ImageService.touch(Onmyoji.awaken_QL_S)
    else:
        logger.debug("雷麒麟")
        ImageService.touch(Onmyoji.awaken_QL_L)
    logger.debug("选择层号")
    ComplexService.swipe_floor(Onmyoji.awaken_C, Onmyoji.awaken_SC, 1, 4)
    logger.debug("开启加成")
    ComplexService.top_addition(Onmyoji.awaken_JC, Onmyoji.awaken_JXJC, Onmyoji.awaken_JCG, Onmyoji.awaken_JCG, 1)
    logger.debug("锁定阵容")
    ImageService.touch(Onmyoji.awaken_SDZR)
    # 是否有准备按钮
    is_prepare = False
    for i in range(fight_time):
        time_fight_start = time.time()
        logger.debug("觉醒挑战{}次", i + 1)
        if is_prepare:
            logger.debug("锁定阵容")
            ImageService.touch(Onmyoji.awaken_SDZR)
        is_fight = ImageService.touch(Onmyoji.awaken_TZ)
        logger.debug("点击准备")
        is_prepare = ImageService.touch(Onmyoji.awaken_ZB, wait=5)
        if not is_fight:
            logger.debug("再次点击挑战")
            ImageService.touch(Onmyoji.awaken_TZ, wait=2)
            logger.debug("点击准备")
            ImageService.touch(Onmyoji.awaken_ZB, wait=5)
        logger.debug("等待战斗结果")
        ComplexService.fight_end(Onmyoji.awaken_ZDSL, Onmyoji.awaken_ZDSB, Onmyoji.awaken_ZCTZ,
                                 Onmyoji.awaken_TCTZ, Onmyoji.awaken_TZ, 60, 2)
        time_fight_end = time.time()
        time_fight_time = time_fight_end - time_fight_start
        logger.debug("本次觉醒挑战，用时{}秒", round(time_fight_time))
        time_fight_list.append(time_fight_time)
    time.sleep(2)
    logger.debug("关闭觉醒加成")
    ComplexService.top_addition(Onmyoji.awaken_JC, Onmyoji.awaken_JXJC, Onmyoji.awaken_JCG, Onmyoji.awaken_JCG, 0)
    logger.debug("觉醒-返回首页")
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    logger.debug("觉醒-返回首页")
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    # 结束时间
    time_end = time.time()
    # 总用时
    time_all = time_end - time_start
    # 战斗次数
    len_time_fight_list = len(time_fight_list)
    # 战斗总用时
    time_fight_all = round(sum(time_fight_list))
    # 平均战斗用时
    time_fight_avg = 0
    if len_time_fight_list > 0:
        time_fight_avg = round(sum(time_fight_list) / len(time_fight_list), 3)
    logger.debug("本轮觉醒十总用时{}秒，战斗总用时{}秒,平均战斗用时{}秒，挑战{}次，胜利{}次，失败{}次",
                 round(time_all, 3), time_fight_all, time_fight_avg, len_time_fight_list, num_win, num_fail)
