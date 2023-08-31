"""
# @Time: 2023年08月31日01:40
# @Author: orcakill
# @File: impl_friends.py
# @Description: 好友协战
"""
import time

from src.model.enum import Onmyoji
from src.model.models import GameAccount
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.ocr_service import OcrService
from src.utils.my_logger import logger

# 服务接口
image_service = ImageService()
complex_service = ComplexService()
ocr_service = OcrService()


def friends_fight(game_task: []):
    # 开始时间
    time_start = time.time()
    # 战斗胜利次数
    num_win = 0
    # 战斗失败次数
    num_fail = 0
    # 协战用时
    time_fight_list = []
    # 账号信息
    game_account = GameAccount(game_task[2])
    logger.debug(game_account.game_name)
    logger.debug("好友协战")
    for i_cooperative_warfare in range(3):
        logger.debug("进入好友界面")
        image_service.touch(Onmyoji.friends_HYTB)
        logger.debug("进入右侧协战")
        image_service.touch(Onmyoji.friends_YCXZ)
        is_cooperative_warfare = image_service.exists(Onmyoji.friends_XZYM)
        if is_cooperative_warfare:
            logger.debug("已完成协战")
            break
        else:
            logger.debug("未完成协战，返回首页")
            image_service.touch(Onmyoji.comm_FH_YSJZDHBSCH)
            logger.debug("好友协战-进入探索")
            image_service.touch(Onmyoji.home_TS)
            logger.debug("好友协战-进入御魂")
            image_service.touch(Onmyoji.soul_BQ_YHTB)
            logger.debug("好友协战-进入八岐大蛇")
            image_service.touch(Onmyoji.soul_BQ_XZ)
            logger.debug("好友协战-八岐大蛇-选择层号")
            complex_service.swipe_floor(Onmyoji.soul_BQ_CZ, Onmyoji.soul_BQ_HTEN, 1, 4)
            logger.debug("好友协战-开启御魂加成")
            is_top_addition = complex_service.top_addition(Onmyoji.soul_BQ_JC, Onmyoji.soul_BQ_YHJC,
                                                           Onmyoji.soul_BQ_JCG,
                                                           Onmyoji.soul_BQ_JCG,
                                                           1)
            # 默认有协战式神
            is_assist_shikigami = True
            for i in range(15):
                time_fight_start = time.time()
                logger.debug("好友协战-御魂-挑战{}次", i + 1)
                if i == 0:
                    logger.debug("好友协战-小号-协战-第一次")
                    logger.debug("解锁阵容")
                    image_service.touch(Onmyoji.soul_BQ_JSZR, wait=3)
                    logger.debug("挑战")
                    image_service.touch(Onmyoji.soul_BQ_TZ, wait=3)
                    logger.debug("点击宠物")
                    for i_pets in range(3):
                        is_pets = image_service.touch(Onmyoji.soul_BQ_CW, wait=5)
                        if is_pets:
                            logger.debug("点击喂食")
                            image_service.touch(Onmyoji.soul_BQ_WS)
                            logger.debug("获得奖励")
                            complex_service.get_reward(Onmyoji.soul_BQ_HDJL)
                        else:
                            logger.debug("喂食成功")
                            break
                    logger.debug("点击预设-御魂-白蛋队伍，清洗位置")
                    image_service.touch(Onmyoji.soul_BQ_YS)
                    image_service.touch(Onmyoji.soul_BQ_YSFZYH)
                    image_service.touch(Onmyoji.soul_BQ_YSZRBD)
                    image_service.touch(Onmyoji.soul_BQ_YSZRCZ)
                    logger.debug("点击预设-御魂-协战队伍")
                    image_service.touch(Onmyoji.soul_BQ_YS)
                    image_service.touch(Onmyoji.soul_BQ_YSFZYH)
                    image_service.touch(Onmyoji.soul_BQ_YSZRXZ)
                    image_service.touch(Onmyoji.soul_BQ_YSZRCZ)
                    logger.debug("点击地板")
                    image_service.touch(Onmyoji.soul_BQ_DJDB)
                    logger.debug("判断是否有协战式神")
                    is_assist_shikigami = image_service.exists(Onmyoji.soul_BQ_XZSS)
                    if is_assist_shikigami:
                        logger.debug("拖拽协战式神，更换白蛋")
                        for i_white in range(10):
                            is_white_egg = image_service.exists(Onmyoji.soul_BQ_BD)
                            if is_white_egg:
                                image_service.swipe(is_assist_shikigami, is_white_egg)
                            else:
                                logger.debug("更换白蛋完成")
                                break
                        logger.debug("准备完成")
                        image_service.touch(Onmyoji.soul_BQ_ZB)
                        logger.debug("等待战斗结果")
                        complex_service.fight_end(Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_ZDSB,
                                                  Onmyoji.soul_BQ_ZCTZ,
                                                  Onmyoji.soul_BQ_TCTZ, Onmyoji.soul_BQ_TZ, 120, 1)
                        time.sleep(5)
                        logger.debug("发现宝藏")
                        complex_service.get_reward(Onmyoji.soul_BQ_FXBZ)
                        logger.debug("锁定阵容")
                        image_service.touch(Onmyoji.soul_BQ_SDZR)
                    else:
                        for i_fail in range(3):
                            logger.debug("退出战斗")
                            image_service.touch(Onmyoji.comm_FH_ZSJZKDZSHXJT)
                            logger.debug("确定")
                            image_service.touch(Onmyoji.soul_BQ_QD)
                            logger.debug("战斗失败")
                            is_fail = image_service.touch(Onmyoji.soul_BQ_ZDSB)
                            if is_fail:
                                break
                else:
                    logger.debug("锁定阵容")
                    image_service.touch(Onmyoji.soul_BQ_SDZR)
                    logger.debug("点击挑战")
                    is_fight = image_service.touch(Onmyoji.soul_BQ_TZ)
                    if not is_fight:
                        logger.debug("好友协战-判断是否还有八岐大蛇-未挑战")
                        image_service.touch(Onmyoji.soul_BQ_TZ, wait=2)
                        logger.debug("好友协战-判断是否还有准备")
                        image_service.touch(Onmyoji.soul_BQ_ZB)
                        logger.debug("发现宝藏")
                        complex_service.get_reward(Onmyoji.soul_BQ_FXBZ)
                    logger.debug("点击准备")
                    image_service.touch(Onmyoji.soul_BQ_ZB, wait=3)
                    logger.debug("好友协战-等待战斗结果")
                    is_result = complex_service.fight_end(Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_ZDSB,
                                                          Onmyoji.soul_BQ_ZCTZ, Onmyoji.soul_BQ_TCTZ,
                                                          Onmyoji.soul_BQ_TZ, 120, 1)
                    if is_result in [Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_TCTZ]:
                        logger.debug("好友协战-战斗胜利")
                        num_win = num_win + 1
                    elif is_result == Onmyoji.soul_BQ_ZCTZ:
                        logger.debug("好友协战-战斗失败")
                        num_fail = num_fail + 1
                    time_fight_end = time.time()
                    time_fight_time = time_fight_end - time_fight_start
                    logger.debug("本次好友协战，用时{}秒", round(time_fight_time))
                    time_fight_list.append(time_fight_time)
                    if is_result == Onmyoji.border_ZCTZ:
                        logger.debug("战斗失败，阵容有问题，结束循环")
                        break
                if not is_assist_shikigami:
                    logger.debug("无协战式神，结束循环")
                    break
            time.sleep(3)
            logger.debug("好友协战-关闭御魂加成")
            if is_top_addition:
                complex_service.top_addition(Onmyoji.soul_BQ_JC, Onmyoji.soul_BQ_YHJC, Onmyoji.soul_BQ_JCG,
                                             Onmyoji.soul_BQ_JCG,
                                             0)
            logger.debug("好友协战-战斗结束，返回首页")
            image_service.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
            logger.debug("好友协战-返回首页")
            image_service.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    logger.debug("好友协战-返回首页")
    image_service.touch(Onmyoji.comm_FH_YSJZDHBSCH)
    # 结束时间
    time_end = time.time()
    # 战斗总用时
    time_fight_all = round(sum(time_fight_list))
    # 战斗次数
    len_time_fight_list = len(time_fight_list)
    # 平均战斗用时
    time_fight_avg = 0
    # 总用时
    time_all = time_end - time_start
    if len_time_fight_list > 0:
        time_fight_avg = round(sum(time_fight_list) / len(time_fight_list), 3)
    logger.debug("本轮好友协战总用时{}秒，战斗总用时{}秒,平均战斗用时{}秒，挑战{}次，胜利{}次，失败{}次",
                 round(time_all, 3),
                 time_fight_all, time_fight_avg, len_time_fight_list, num_win, num_fail)
