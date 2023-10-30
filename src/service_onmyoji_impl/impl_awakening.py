# @Time: 2023年09月01日 17:23
# @Author: orcakill
# @File: impl_awakening.py
# @Description: 觉醒
import datetime
import time

from src.model.enum import Onmyoji
from src.model.models import GameProjectsRelation
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service_onmyoji_impl import impl_initialization
from src.utils.my_logger import logger
from src.utils.utils_time import UtilsTime


def awakening(game_task: [], awakening_type: int = 0):
    """
        觉醒十 风、火、水、雷（默认雷）  开加成，选觉醒阵容
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
    # 战斗次数
    fight_time = game_projects_relation.project_num_times or 2
    # 获取当前日期
    today = datetime.date.today()
    # 获取本日是周几（周一为0，周日为6）
    weekday = today.weekday() + 1
    logger.debug("本日周{}", weekday)
    if awakening_type != 0:
        logger.debug("修改麒麟类型")
        weekday = awakening_type
    if weekday == 1:
        logger.debug("火麒麟")
        weekday_type = Onmyoji.awaken_QL_H
    elif weekday == 2:
        logger.debug("风麒麟")
        weekday_type = Onmyoji.awaken_QL_F
    elif weekday == 3:
        logger.debug("水麒麟")
        weekday_type = Onmyoji.awaken_QL_S
    else:
        logger.debug("雷麒麟")
        weekday_type = Onmyoji.awaken_QL_L
    logger.debug("1.战斗前准备")
    for i_come in range(3):
        logger.debug("进入探索")
        ImageService.touch(Onmyoji.home_TS)
        logger.debug("进入觉醒")
        ImageService.touch(Onmyoji.awaken_JXBT)
        logger.debug("选择麒麟")
        is_awakening = ImageService.touch(weekday_type)
        if is_awakening:
            logger.debug("确定进入觉醒")
            break
    logger.debug("选择层号")
    is_layer_number = ComplexService.swipe_floor(Onmyoji.awaken_C, Onmyoji.awaken_SC, 1, 4)
    if not is_layer_number:
        logger.debug("未找到层号，不战斗")
    else:
        logger.debug("开启加成")
        ComplexService.top_addition(Onmyoji.awaken_JC, Onmyoji.awaken_JXJC, Onmyoji.awaken_JCK, Onmyoji.awaken_JCG, 1)
        logger.debug("2.战斗")
        # 锁定阵容,默认锁定
        is_unlock = False
        for i in range(fight_time):
            time_fight_start = time.time()
            logger.debug("觉醒挑战{}次", i + 1)
            if is_unlock:
                logger.debug("锁定阵容")
                ImageService.touch(Onmyoji.awaken_SDZR)
                is_unlock = False
            logger.debug("挑战")
            ImageService.touch(Onmyoji.awaken_TZ)
            logger.debug("自动战斗")
            is_auto = ImageService.exists(Onmyoji.awaken_ZD, timeouts=10)
            if not is_auto:
                logger.debug("点击可能存在的悬赏封印")
                ComplexService.refuse_reward()
                logger.debug("点击可能存在的退出挑战")
                ImageService.touch(Onmyoji.awaken_TCTZ)
                logger.debug("再次点击挑战")
                ImageService.touch(Onmyoji.awaken_TZ, wait=2)
                logger.debug("再次点击准备")
                is_unlock = ImageService.touch(Onmyoji.awaken_ZB, wait=5)
                logger.debug("再次检查自动战斗")
                is_auto = ImageService.exists(Onmyoji.awaken_ZD)
            if is_auto:
                logger.debug("等待战斗结果")
                is_result = ComplexService.fight_end(Onmyoji.awaken_ZDSL, Onmyoji.awaken_ZDSB, Onmyoji.awaken_ZCTZ,
                                                     Onmyoji.awaken_TCTZ, Onmyoji.awaken_TZ, None, 60, 2)
                if is_result in [Onmyoji.awaken_ZDSL, Onmyoji.awaken_TCTZ]:
                    num_win = num_win + 1
                elif is_result in [Onmyoji.awaken_ZCTZ, Onmyoji.awaken_ZDSB]:
                    num_fail = num_fail + 1
                time_fight_end = time.time()
                time_fight_time = time_fight_end - time_fight_start
                logger.debug("本次觉醒挑战，用时{}秒", round(time_fight_time))
                time_fight_list.append(time_fight_time)
            else:
                logger.debug("不在自动战斗中，跳过等待战斗结果")
    logger.debug("3.重置到首页")
    time.sleep(2)
    logger.debug("点击可能存在的退出挑战")
    ImageService.touch(Onmyoji.awaken_TCTZ, wait=2)
    logger.debug("关闭觉醒加成")
    ComplexService.top_addition(Onmyoji.awaken_JC, Onmyoji.awaken_JXJC, Onmyoji.awaken_JCK, Onmyoji.awaken_JCG, 0)
    logger.debug("觉醒-返回首页")
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    logger.debug("确认返回首页")
    impl_initialization.return_home(game_task)
    logger.debug("4.战斗结算")
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
                 UtilsTime.convert_seconds(time_all), UtilsTime.convert_seconds(time_fight_all), time_fight_avg,
                 len_time_fight_list, num_win, num_fail)
