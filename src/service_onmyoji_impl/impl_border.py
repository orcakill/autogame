"""
# @Time: 2023年08月31日01:12
# @Author: orcakill
# @File: impl_border.py
# @Description: 结界突破-阴阳寮突破、个人突破
"""
import time

from src.model.enum import Onmyoji, Cvstrategy
from src.model.models import GameAccount
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.ocr_service import OcrService
from src.utils.my_logger import logger


def region_border(game_task: []):
    """
    阴阳寮突破
    :param game_task: 任务信息
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
    # 账号信息
    game_account = GameAccount(game_task[2])
    logger.debug(game_account.game_name)
    logger.debug("进入探索")
    ImageService.touch(Onmyoji.home_TS)
    logger.debug("进入结界突破")
    ImageService.touch(Onmyoji.region_JJTPTB)
    logger.debug("进入寮突破")
    ImageService.touch(Onmyoji.region_YCYYL)
    logger.debug("锁定阵容")
    ImageService.touch(Onmyoji.region_SDZR)
    logger.debug("判断有寮结界")
    is_fight = ImageService.exists(Onmyoji.region_LJJ, cvstrategy=Cvstrategy.default)
    logger.debug("判断是否无寮结界挑战")
    is_fight_times = ImageService.exists(Onmyoji.region_WTZCS)
    # 有寮结界  没有零的挑战次数
    if is_fight and not is_fight_times:
        logger.debug("阴阳寮突破开始")
        for i_fight in range(9):
            time_fight_start = time.time()
            logger.debug("阴阳寮突破{}次", i_fight + 1)
            logger.debug("点击寮结界")
            ImageService.touch(Onmyoji.region_LJJ, cvstrategy=Cvstrategy.default)
            logger.debug("点击进攻")
            is_attack = ImageService.touch(Onmyoji.region_JG)
            if not is_attack:
                logger.debug("再次点击寮结界")
                ImageService.touch(Onmyoji.region_LJJ, cvstrategy=Cvstrategy.default)
                logger.debug("再次点击进攻")
                ImageService.touch(Onmyoji.region_JG)
            logger.debug("判断是否还有进攻")
            is_attack = ImageService.exists(Onmyoji.region_JG, wait=3)
            if is_attack:
                logger.debug("可能已被挑战,点击左侧突破进度")
                ImageService.touch(Onmyoji.region_ZCTPJD)
            else:
                logger.debug("等待战斗结果")
                is_result = ComplexService.fight_end(Onmyoji.region_ZDSL, Onmyoji.region_ZDSB, Onmyoji.region_ZCTZ,
                                                     Onmyoji.region_TCTZ, Onmyoji.region_LJJ, 300, 2)
                if is_result in [Onmyoji.region_ZDSL, Onmyoji.region_TCTZ]:
                    num_win = num_win + 1
                elif is_result == Onmyoji.border_ZCTZ:
                    num_fail = num_fail + 1
                time_fight_end = time.time()
                time_fight_time = time_fight_end - time_fight_start
                logger.debug("本次阴阳寮突破，用时{}秒", round(time_fight_time))
                time_fight_list.append(time_fight_time)
    else:
        logger.debug("无寮结界或者无挑战次数")
    logger.debug("返回首页")
    ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH)
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH, wait=2)
    logger.debug("确认返回首页")
    ComplexService.return_home(game_task)
    # 结束时间
    time_end = time.time()
    # 总用时
    time_all = time_end - time_start
    # 战斗总用时
    time_fight_all = round(sum(time_fight_list))
    # 战斗次数
    len_time_fight_list = len(time_fight_list)
    # 平均战斗用时
    time_fight_avg = 0
    if len_time_fight_list > 0:
        time_fight_avg = round(sum(time_fight_list) / len(time_fight_list), 3)
    if is_fight and not is_fight_times:
        logger.debug("本轮阴阳寮总用时{}秒，战斗总用时{}秒,平均战斗用时{}秒，挑战{}次，胜利{}次，失败{}次",
                     round(time_all, 3),
                     time_fight_all, time_fight_avg, len_time_fight_list, num_win, num_fail)
    else:
        logger.debug("无寮结界或无战斗次数，总用时{}秒", time_all)


def border_fight(game_task: [], fight_times: int = 40):
    """
    结界突破 border
    :param fight_times: 默认战斗次数
    :param game_task: 项目信息
    :return:
    """
    # 账号信息
    game_account = GameAccount(game_task[2])
    # 战斗胜利次数
    num_win = 0
    # 战斗失败次数
    num_false = 0
    # 结界挑战劵数
    num_securities = 0
    # 结界突破起始时间
    time_start_border = time.time()
    # 结界突破战斗用时
    time_fight_list = []
    logger.debug(game_account.game_name)
    logger.debug("进入探索")
    ImageService.touch(Onmyoji.home_TS)
    logger.debug("进入结界突破")
    ImageService.touch(Onmyoji.border_JJTPTB)
    for i in range(fight_times):
        time_fight_start = time.time()
        logger.debug("结界突破{}次", i + 1)
        if i == 0:
            logger.debug("第一次战斗，获取当前结界挑战劵数")
            num_securities = OcrService.border_bond()
            if num_securities == "0":
                logger.debug("无结界挑战劵")
                break
        if num_false % 3 == 0 and num_false != 0:
            logger.debug("战斗失败累计{}次，3的倍数,判断是否有战败标志", num_false)
            is_fail = ImageService.exists(Onmyoji.border_ZBBZ, timeouts=3)
            if is_fail:
                logger.debug("判断是否有刷新")
                is_rush = ImageService.exists(Onmyoji.border_SX)
                if is_rush:
                    logger.debug("有战败标志，战斗失败累计{}次，3的倍数，点击刷新", num_false)
                    ImageService.touch(Onmyoji.border_SX, wait=2)
                    ImageService.touch(Onmyoji.border_SXQD, wait=2)
        for i_attack in range(3):
            logger.debug("点击个人结界")
            ImageService.touch(Onmyoji.border_GRJJ, cvstrategy=Cvstrategy.default, wait=2)
            logger.debug("点击进攻")
            is_attack = ImageService.touch(Onmyoji.border_JG, cvstrategy=Cvstrategy.default, wait=1)
            if is_attack:
                break
        logger.debug("点击准备")
        ImageService.touch(Onmyoji.border_ZB, timeouts=3)
        logger.debug("等待战斗结果")
        is_result = ComplexService.fight_end(Onmyoji.border_ZDSL, Onmyoji.border_ZDSB,
                                             Onmyoji.border_ZCTZ, Onmyoji.border_TCTZ, Onmyoji.border_GRJJ,
                                             300, 1)
        logger.debug("再点击一次退出挑战")
        ImageService.touch(Onmyoji.border_TCTZ, wait=2, timeouts=1)
        if is_result in [Onmyoji.border_ZDSL, Onmyoji.border_TCTZ]:
            num_win = num_win + 1
        elif is_result == Onmyoji.border_ZCTZ:
            num_false = num_false + 1
        elif is_result == Onmyoji.border_GRJJ or is_result is None:
            logger.debug("判断是否仍有进攻")
            is_attack1 = ImageService.exists(Onmyoji.border_JG, wait=5, timeouts=2, is_click=True)
            if is_attack1:
                logger.debug("可能已无结界挑战劵,点击消耗退出")
                ImageService.touch(Onmyoji.border_XH)
                logger.debug("判断是否存在结界挑战劵0/30")
                is_securities = OcrService.border_bond()
                if is_securities == "0":
                    logger.debug("无结界挑战劵，跳出循环")
                    break
        time_fight_end = time.time()
        time_fight = time_fight_end - time_fight_start
        logger.debug("本次结界突破战斗结束，用时{}秒", round(time_fight, 3))
        time_fight_list.append(time_fight)
    logger.debug("返回探索界面")
    ImageService.touch(Onmyoji.comm_FH_YSJZDHBSCH)
    logger.debug("返回首页")
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    time_end_border = time.time()
    # 总用时
    time_all = round(time_end_border - time_start_border, 3)
    # 战斗总用时
    time_fight_all = round(sum(time_fight_list))
    # 战斗次数
    len_time_fight_list = len(time_fight_list)
    # 平均战斗用时
    time_fight_avg = 0
    if len_time_fight_list > 0:
        time_fight_avg = round(sum(time_fight_list) / len(time_fight_list), 3)
    logger.debug(
        "本轮结界突破战斗结束，总用时{}秒，结界挑战劵{}张，战斗总用时{}秒,战斗次数{}次，胜利{}次，失败{}次，平均用时{}秒",
        time_all, num_securities, time_fight_all, len_time_fight_list, num_win, num_false, time_fight_avg)
