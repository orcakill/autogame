"""
# @Time: 2023年08月31日01:40
# @Author: orcakill
# @File: impl_friends.py
# @Description: 好友协战
"""
import time

from src.model.enum import Onmyoji, Cvstrategy
from src.model.models import GameAccount
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service_onmyoji_impl import impl_awakening, impl_initialization
from src.utils.my_logger import logger


def friends_fight(game_task: []):
    """
    好友协战
    :param game_task: 任务信息
    :return:
    """
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
        ImageService.touch(Onmyoji.friends_HYTB)
        logger.debug("进入右侧协战")
        ImageService.touch(Onmyoji.friends_YCXZ)
        logger.debug("判断是否已完成协战，1次")
        is_cooperative_warfare = ImageService.exists(Onmyoji.friends_XZYM)
        if not is_cooperative_warfare:
            logger.debug("判断是否已完成协战，2次")
            is_cooperative_warfare = ImageService.exists(Onmyoji.friends_XZYM)
        if is_cooperative_warfare:
            logger.debug("已完成协战")
            break
        else:
            logger.debug("未完成协战，返回首页")
            ImageService.touch(Onmyoji.comm_FH_YSJZDHBSCH)
            logger.debug("确认返回首页")
            impl_initialization.return_home(game_task)
            if i_cooperative_warfare == 0:
                logger.debug("觉醒挑战")
                impl_awakening.awakening(game_task)
            logger.debug("好友协战-进入探索")
            ImageService.touch(Onmyoji.home_TS)
            logger.debug("好友协战-进入御魂")
            ImageService.touch(Onmyoji.soul_BQ_YHTB)
            logger.debug("好友协战-进入八岐大蛇")
            ImageService.touch(Onmyoji.soul_BQ_XZ)
            logger.debug("好友协战-八岐大蛇-选择层号")
            ComplexService.swipe_floor(Onmyoji.soul_BQ_CZ, Onmyoji.soul_BQ_HTEN, 1, 4)
            logger.debug("好友协战-开启御魂加成")
            is_top_addition = ComplexService.top_addition(Onmyoji.soul_BQ_JC, Onmyoji.soul_BQ_YHJC,
                                                          Onmyoji.soul_BQ_JCG,
                                                          Onmyoji.soul_BQ_JCG,
                                                          1)
            # 默认有协战式神
            is_assist_shikigami = True
            # 默认锁定阵容
            is_unlock = False
            for i in range(20):
                time_fight_start = time.time()
                logger.debug("好友协战-御魂-挑战{}次", i + 1)
                if i == 0:
                    logger.debug("好友协战-小号-协战-第一次")
                    logger.debug("解锁阵容")
                    is_unlock = ImageService.touch(Onmyoji.soul_BQ_JSZR, wait=3)
                    if not is_unlock:
                        is_unlock = ImageService.touch(Onmyoji.soul_BQ_JSZR, wait=3)
                        if is_unlock:
                            logger.debug("解锁阵容成功")
                        is_lock = ImageService.exists(Onmyoji.soul_BQ_SDZR, wait=3)
                        if is_lock:
                            logger.debug("已解锁，无需再解锁")
                        if not is_unlock and not is_lock:
                            logger.debug("无解锁阵容，无锁定阵容,退出")
                            break
                    logger.debug("判断左侧是否有御魂自选")
                    is_self_selection = ImageService.touch(Onmyoji.soul_BQ_YHZX)
                    if is_self_selection:
                        ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH)
                        logger.debug("返回")
                    logger.debug("挑战")
                    ImageService.touch(Onmyoji.soul_BQ_TZ, wait=3)
                    logger.debug("点击宠物")
                    for i_pets in range(3):
                        is_pets = ImageService.touch(Onmyoji.soul_BQ_CW, wait=5)
                        if is_pets:
                            logger.debug("点击喂食")
                            ImageService.touch(Onmyoji.soul_BQ_WS)
                            logger.debug("获得奖励")
                            ComplexService.get_reward(Onmyoji.soul_BQ_HDJL)
                        else:
                            logger.debug("喂食成功")
                            break
                    logger.debug("点击预设-御魂-白蛋队伍，清洗位置")
                    ImageService.touch(Onmyoji.soul_BQ_YS)
                    ImageService.touch(Onmyoji.soul_BQ_YSFZYH)
                    ImageService.touch(Onmyoji.soul_BQ_YSZRBD)
                    ImageService.touch(Onmyoji.soul_BQ_YSZRCZ)
                    logger.debug("点击预设-御魂-协战队伍")
                    ImageService.touch(Onmyoji.soul_BQ_YS)
                    ImageService.touch(Onmyoji.soul_BQ_YSFZYH)
                    ImageService.touch(Onmyoji.soul_BQ_YSZRXZ)
                    ImageService.touch(Onmyoji.soul_BQ_YSZRCZ)
                    logger.debug("点击地板")
                    ImageService.touch(Onmyoji.soul_BQ_DJDB)
                    logger.debug("判断是否有协战式神")
                    is_assist_shikigami = ImageService.exists(Onmyoji.soul_BQ_XZSS)
                    if is_assist_shikigami:
                        logger.debug("拖拽协战式神，更换白蛋")
                        for i_white in range(10):
                            is_white_egg = ImageService.exists(Onmyoji.soul_BQ_BD)
                            if is_white_egg:
                                ImageService.swipe(is_assist_shikigami, is_white_egg)
                            else:
                                logger.debug("更换白蛋完成")
                                break
                        logger.debug("准备完成")
                        ImageService.touch(Onmyoji.soul_BQ_ZB)
                        ComplexService.get_reward(Onmyoji.soul_BQ_FXBZ)
                        logger.debug("等待战斗结果")
                        ComplexService.fight_end(Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_ZDSB,
                                                 Onmyoji.soul_BQ_ZCTZ,
                                                 Onmyoji.soul_BQ_TCTZ, Onmyoji.soul_BQ_TZ, None, 120, 1)
                        time.sleep(3)
                        logger.debug("发现宝藏")
                        ComplexService.get_reward(Onmyoji.soul_BQ_FXBZ)
                        logger.debug("锁定阵容")
                        ImageService.touch(Onmyoji.soul_BQ_SDZR)
                    else:
                        for i_fail in range(3):
                            logger.debug("退出战斗")
                            ImageService.touch(Onmyoji.comm_FH_ZSJZKDZSHXJT)
                            logger.debug("确定")
                            ImageService.touch(Onmyoji.soul_BQ_QD)
                            logger.debug("战斗失败")
                            is_fail = ImageService.touch(Onmyoji.soul_BQ_ZDSB)
                            if is_fail:
                                break
                else:
                    if is_unlock:
                        logger.debug("锁定阵容")
                        ImageService.touch(Onmyoji.soul_BQ_SDZR)
                    logger.debug("点击挑战")
                    is_fight = ImageService.touch(Onmyoji.soul_BQ_TZ)
                    if not is_fight:
                        logger.debug("好友协战-判断是否还有八岐大蛇-未挑战")
                        ImageService.touch(Onmyoji.soul_BQ_TZ, wait=2)
                        logger.debug("好友协战-判断是否还有准备")
                        ImageService.touch(Onmyoji.soul_BQ_ZB)
                        logger.debug("发现宝藏")
                        ComplexService.get_reward(Onmyoji.soul_BQ_FXBZ)
                    logger.debug("点击准备")
                    is_unlock = ImageService.touch(Onmyoji.soul_BQ_ZB, wait=4)
                    logger.debug("好友协战-等待战斗结果")
                    is_result = ComplexService.fight_end(Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_ZDSB,
                                                         Onmyoji.soul_BQ_ZCTZ, Onmyoji.soul_BQ_TCTZ,
                                                         Onmyoji.soul_BQ_TZ, None, 120, 1)
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
                    if is_result in [Onmyoji.soul_BQ_ZCTZ, Onmyoji.soul_BQ_ZDSB]:
                        logger.debug("战斗失败，阵容有问题，结束循环")
                        break
                if not is_assist_shikigami:
                    logger.debug("无协战式神，结束循环")
                    break
            time.sleep(3)
            logger.debug("好友协战-关闭御魂加成")
            if is_top_addition:
                ComplexService.top_addition(Onmyoji.soul_BQ_JC, Onmyoji.soul_BQ_YHJC, Onmyoji.soul_BQ_JCG,
                                            Onmyoji.soul_BQ_JCG,
                                            0)
            logger.debug("好友协战-战斗结束，返回首页")
            ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
            logger.debug("好友协战-返回首页")
            ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
            logger.debug("确认返回首页")
            impl_initialization.return_home(game_task)
    logger.debug("好友协战-返回首页")
    ImageService.touch(Onmyoji.comm_FH_YSJZDHBSCH)
    logger.debug("确认返回首页")
    impl_initialization.return_home(game_task)
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


def friends_manage(game_task: []):
    # 开始时间
    time_start = time.time()
    # 账号信息
    game_account = GameAccount(game_task[2])
    logger.debug(game_account.game_name)
    logger.debug("进入好友界面")
    is_friends = ImageService.touch(Onmyoji.friends_HYTB)
    for i_fetter in range(5):
        logger.debug("判断有无好友羁绊提升")
        is_fetter = ImageService.exists(Onmyoji.friends_HYJBTS)
        if is_fetter:
            ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH)
        else:
            break
    logger.debug("好友友情点收取")
    if is_friends:
        logger.debug("点击好友-右侧好友")
        ImageService.touch(Onmyoji.friends_YCHY)
        logger.debug("点击左下好友")
        ImageService.touch(Onmyoji.friends_ZXHY)
        logger.debug("点击一键收取")
        is_collect = ImageService.exists(Onmyoji.friends_YJSQ, is_click=True)
        if is_collect:
            logger.debug("获得奖励")
            ComplexService.get_reward(Onmyoji.friends_HDJL)
        else:
            logger.debug("无一键收取")
    logger.debug("吉闻祝福")
    ImageService.touch(Onmyoji.friends_JW)
    logger.debug("一键祝福")
    is_blessing = ImageService.exists(Onmyoji.friends_YJZF, is_click=True)
    if is_blessing:
        logger.debug("祝福按钮")
        ImageService.touch(Onmyoji.friends_ZFAN)
        logger.debug("获得奖励")
        ComplexService.get_reward(Onmyoji.friends_HDJL)
    else:
        logger.debug("无一键祝福")
    logger.debug("返回到好友界面")
    ImageService.touch(Onmyoji.comm_FH_YSJZDHBSCH)
    logger.debug("好友添加")
    is_friend_is_full = ImageService.exists(Onmyoji.friends_HYYM, cvstrategy=Cvstrategy.default)
    if not is_friend_is_full:
        logger.debug("好友不满200，进入添加")
        ImageService.touch(Onmyoji.friends_YCTJ)
        for i_add in range(20):
            logger.debug("点击添加好友")
            is_add = ImageService.touch(Onmyoji.friends_TJHY, cvstrategy=Cvstrategy.default)
            if is_add:
                logger.debug("申请")
                ImageService.touch(Onmyoji.friends_SQ)
            else:
                logger.debug("无添加按钮")
                break
    logger.debug("返回首页")
    ImageService.touch(Onmyoji.comm_FH_YSJZDHBSCH)
    time_end = time.time() - time_start
    logger.info("好友管理,用时{}秒", round(time_end))
