"""
# @Time: 2023年08月31日01:12
# @Author: orcakill
# @File: impl_region_border.py
# @Description: 阴阳寮突破
"""
import time

from src.model.enum import Onmyoji, Cvstrategy
from src.model.models import GameAccount
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.ocr_service import OcrService
from src.service.onmyoji_service_impl import impl_return_home
from src.utils.my_logger import logger

# 服务接口
image_service = ImageService()
complex_service = ComplexService()
ocr_service = OcrService()


def region_border(game_task: []):
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
    image_service.touch(Onmyoji.home_TS)
    logger.debug("进入结界突破")
    image_service.touch(Onmyoji.region_JJTPTB)
    logger.debug("进入寮突破")
    image_service.touch(Onmyoji.region_YCYYL)
    logger.debug("锁定阵容")
    image_service.touch(Onmyoji.region_SDZR)
    logger.debug("判断有寮结界")
    is_fight = image_service.exists(Onmyoji.region_LJJ, cvstrategy=Cvstrategy.default)
    logger.debug("判断是否无寮结界挑战")
    is_fight_times = image_service.exists(Onmyoji.region_WTZCS)
    # 有寮结界  没有零的挑战次数
    if is_fight and not is_fight_times:
        logger.debug("阴阳寮突破开始")
        for i_fight in range(9):
            time_fight_start = time.time()
            logger.debug("阴阳寮突破{}次", i_fight + 1)
            logger.debug("点击寮结界")
            image_service.touch(Onmyoji.region_LJJ, cvstrategy=Cvstrategy.default)
            logger.debug("点击进攻")
            is_attack = image_service.touch(Onmyoji.region_JG)
            if not is_attack:
                logger.debug("再次点击寮结界")
                image_service.touch(Onmyoji.region_LJJ, cvstrategy=Cvstrategy.default)
                logger.debug("再次点击进攻")
                image_service.touch(Onmyoji.region_JG)
            logger.debug("判断是否还有进攻")
            is_attack = image_service.exists(Onmyoji.region_JG, wait=3)
            if is_attack:
                logger.debug("可能已被挑战,点击左侧突破进度")
                image_service.touch(Onmyoji.region_ZCTPJD)
            else:
                logger.debug("等待战斗结果")
                is_result = complex_service.fight_end(Onmyoji.region_ZDSL, Onmyoji.region_ZDSB, Onmyoji.region_ZCTZ,
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
    image_service.touch(Onmyoji.comm_FH_YSJHDBSCH)
    image_service.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH, wait=2)
    logger.debug("确认返回首页")
    impl_return_home.return_home(game_task)
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
