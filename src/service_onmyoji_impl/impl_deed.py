"""
# @Time: 2023年09月04日23:44
# @Author: orcakill
# @File: impl_deed.py
# @Description: 契灵
"""
import time

from src.model.enum import Onmyoji
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service_onmyoji_impl import impl_initialization
from src.utils.my_logger import logger
from src.utils.utils_time import UtilsTime


def deed_spirit(game_task: []):
    """
    契灵，默认镇墓兽，使用
    :return:
    """
    time_start = time.time()
    # 契灵图标可点击，默认不可点击
    is_deed = False
    for i_come in range(2):
        logger.debug("进入探索")
        ImageService.touch(Onmyoji.home_TS)
        logger.debug("进入契灵")
        is_deed = ImageService.touch(Onmyoji.deed_QLTB)
        if is_deed:
            break
        else:
            ComplexService.refuse_reward()
    logger.debug("判断是否契灵首页")
    is_deed_home = ImageService.exists(Onmyoji.deed_QLSY)
    if is_deed and is_deed_home:
        # 判断是否有契灵，无则使用鸣契石召唤5次并战斗，直至无鸣契石，之后探查50次，清理探查出
        logger.debug("当前契灵首页")
        logger.debug("鸣契石召唤，契灵战斗")
        for i_stone in range(5):
            logger.debug("第{}次召唤")
            ImageService.touch(Onmyoji.deed_MQZH)
            logger.debug("镇墓兽")
            ImageService.touch(Onmyoji.deed_ZHZMS)
            logger.debug("召唤确认")
            ImageService.touch(Onmyoji.deed_ZHQR)
        logger.debug("鸣契石契灵战斗")
        deed_fight()
        logger.debug("探查50次")
        for i_exploration in range(50):
            logger.debug("点击探查{}", i_exploration + 1)
            ImageService.touch(Onmyoji.deed_TC)
            logger.debug("等待战斗结果")
            ComplexService.fight_end(Onmyoji.deed_ZDSL, Onmyoji.deed_ZDSB, Onmyoji.deed_ZCTZ,
                                     Onmyoji.deed_TCTZ, Onmyoji.deed_TC, None, 60, 4)
        logger.debug("探查契灵战斗")
        deed_fight()
    logger.debug("确认返回首页")
    impl_initialization.return_home(game_task)
    time_all = time.time() - time_start
    logger.debug("契灵战斗，{}", UtilsTime.convert_seconds(time_all))


def deed_fight():
    """
    契灵战斗
    :return:
    """
    for i in range(6):
        logger.debug("判断当前是否存在契灵 1契灵地图 2 契灵界面")
        is_boss = ImageService.exists(Onmyoji.deed_QL)
        is_fight = ImageService.exists(Onmyoji.deed_QLTZ)
        if is_boss or is_fight:
            if is_boss:
                logger.debug("地图存在契灵,点击地图上契灵")
                ImageService.touch(Onmyoji.deed_QL)
            if is_fight:
                logger.debug("契灵结契界面")
            logger.debug("点击契灵挑战")
            is_fight = ImageService.touch(Onmyoji.deed_QLTZ)
            if not is_fight:
                ComplexService.refuse_reward()
                logger.debug("重新点击契灵挑战")
                ImageService.touch(Onmyoji.deed_QLTZ)
            ComplexService.fight_end(Onmyoji.deed_ZDSL, Onmyoji.deed_ZDSL, Onmyoji.deed_ZCTZ, Onmyoji.deed_TCTZ,
                                     Onmyoji.deed_QLTZ, None, 300, 2)
        else:
            logger.debug("不存在契灵")
            break
