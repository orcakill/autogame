# @Time: 2023年09月01日 17:20
# @Author: orcakill
# @File: impl_reward.py
# @Description: 每日奖励
import time

from src.model.enum import Onmyoji
from src.model.models import GameAccount
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service_onmyoji_impl import impl_initialization
from src.utils.my_logger import logger


def daily_rewards(game_task: []):
    # 开始时间
    time_start = time.time()
    # 账号信息
    game_account = GameAccount(game_task[2])
    logger.debug(game_account.game_name)
    logger.debug("1.首页小纸人奖励")
    logger.debug("判断是否有签到小纸人")
    is_sign_in = ImageService.exists(Onmyoji.reward_QDXZR, timeouts=2)
    if is_sign_in:
        logger.debug("有签到小纸人")
        ImageService.touch_coordinate(is_sign_in)
        logger.debug("点击每日一签")
        ImageService.touch(Onmyoji.reward_MRYQ)
        logger.debug("点击退出挑战")
        ImageService.touch(Onmyoji.reward_TCTZ, wait=5)
        logger.debug("返回首页")
        ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH)
    else:
        ComplexService.refuse_reward()
    logger.debug("判断是否有体力小纸人")
    is_strength = ImageService.exists(Onmyoji.reward_TLXZR, timeouts=2, wait=3)
    if is_strength:
        logger.debug("有体力小纸人")
        ImageService.touch_coordinate(is_strength)
        logger.debug("获得体力奖励，退出")
        is_reward = ImageService.exists(Onmyoji.reward_HDJL, wait=3)
        if is_reward:
            ImageService.touch_coordinate((1 / 2 * is_reward[0], 1 / 2 * is_reward[1]))
    else:
        ComplexService.refuse_reward()
    logger.debug("判断是否有勾玉小纸人")
    is_jade = ImageService.exists(Onmyoji.reward_GYXZR, timeouts=2, wait=3)
    if is_jade:
        logger.debug("有勾玉小纸人")
        ImageService.touch_coordinate(is_jade)
        logger.debug("获得勾玉奖励，退出")
        is_reward = ImageService.exists(Onmyoji.reward_HDJL, wait=3)
        if is_reward:
            ImageService.touch_coordinate((1 / 2 * is_reward[0], 1 / 2 * is_reward[1]))
    else:
        ComplexService.refuse_reward()
    logger.debug("判断是否有御魂觉醒加成小纸人")
    is_soul_addition = ImageService.exists(Onmyoji.reward_YHJXJCXZR, timeouts=2, wait=3)
    if is_soul_addition:
        logger.debug("有御魂觉醒加成小纸人")
        ImageService.touch_coordinate(is_soul_addition)
        logger.debug("获得奖励，退出")
        is_reward = ImageService.exists(Onmyoji.reward_HDJL, wait=3)
        if is_reward:
            ImageService.touch_coordinate((1 / 2 * is_reward[0], 1 / 2 * is_reward[1]))
    logger.debug("返回首页")
    impl_initialization.return_home(game_task)
    logger.debug("2.邮箱奖励")
    is_mail = ImageService.exists(Onmyoji.reward_YX)
    if is_mail:
        logger.debug("点击邮箱")
        ImageService.touch_coordinate(is_mail)
        logger.debug("判断是否有全部领取")
        is_get = ImageService.exists(Onmyoji.reward_YXQBLQ, wait=3)
        if is_get:
            logger.debug("点击全部领取")
            ImageService.touch_coordinate(is_get)
            logger.debug("点击确定")
            ImageService.touch(Onmyoji.reward_QD, wait=3)
            logger.debug("获得奖励，退出")
            is_reward = ImageService.exists(Onmyoji.reward_HDJL, wait=3)
            if is_reward:
                ImageService.touch_coordinate((1 / 2 * is_reward[0], 1 / 2 * is_reward[1]))
        logger.debug("返回首页")
        ImageService.touch(Onmyoji.comm_FH_YSJZDHBSCH, wait=3)
    else:
        ComplexService.refuse_reward()
    logger.debug("3.礼包屋奖励")
    is_store = ImageService.exists(Onmyoji.store_SDTB)
    if is_store:
        logger.debug("点击商店图标")
        ImageService.touch_coordinate(is_store)
        logger.debug("判断是否有右上角返回")
        is_right = ImageService.exists(Onmyoji.comm_FH_YSJHDBSCH)
        if is_right:
            ImageService.touch_coordinate(is_right)
        logger.debug("点击礼包屋")
        ImageService.touch(Onmyoji.store_LBW)
        logger.debug("点击推荐")
        ImageService.touch(Onmyoji.store_TJ)
        logger.debug("判断是否有每日领取")
        is_day = ImageService.exists(Onmyoji.store_MRLQ, wait=2)
        if is_day:
            ImageService.touch_coordinate(is_day)
            logger.debug("获得每日免费奖励，退出")
            is_reward = ImageService.exists(Onmyoji.store_HDJL, wait=3)
            if is_reward:
                ImageService.touch_coordinate((1 / 2 * is_reward[0], 1 / 2 * is_reward[1]))
        else:
            logger.debug("无每日免费奖励")
        logger.debug("返回首页")
        ImageService.touch(Onmyoji.comm_FH_ZSJHKHSXYH)
        ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    else:
        ComplexService.refuse_reward()
    logger.debug("4.花合战奖励")
    is_flower_battle = ImageService.exists(Onmyoji.reward_HHZTB, is_click=True)
    if is_flower_battle:
        logger.debug("点击右侧任务")
        ImageService.touch(Onmyoji.reward_YCRW)
        logger.debug("点击全部领取")
        ImageService.exists(Onmyoji.reward_HHZQBLQ, is_click=True)
        logger.debug("获得奖励")
        ComplexService.get_reward(Onmyoji.reward_HDJL)
        logger.debug("返回首页")
        ImageService.touch(Onmyoji.comm_FH_ZSJLDBKBSXYH)
    else:
        ComplexService.refuse_reward()
    time_end = time.time() - time_start
    logger.info("每日奖励,用时{}秒", round(time_end))
