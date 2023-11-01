"""
# @Time: 2023年09月04日23:44
# @Author: orcakill
# @File: impl_deed.py
# @Description: 契灵
"""
import time

from src.dao.mapper import Mapper
from src.model.enum import Onmyoji
from src.model.models import GameAccount, GameDevices, GameProject, GameProjectLog, GameProjectsRelation
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.ocr_service import OcrService
from src.service_onmyoji_impl import impl_initialization
from src.utils.my_logger import logger
from src.utils.utils_time import UtilsTime


def deed_spirit(game_task: []):
    """
    契灵，默认镇墓兽，使用
    :return:
    """
    time_start = time.time()
    # 项目信息
    (game_projects_relation, game_account,
     game_project, game_devices) = (GameProjectsRelation(game_task[1]), GameAccount(game_task[2]),
                                    GameProject(game_task[3]), GameDevices(game_task[4]))
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
    if is_deed:
        # 判断是否有契灵，无则使用鸣契石召唤5次并战斗，直至无鸣契石，之后探查50次，清理探查出
        logger.debug("当前契灵首页")
        logger.debug("1.鸣契石召唤，契灵战斗")
        for i_stone in range(1, 31):
            logger.debug("检查鸣契石数")
            num_stone = OcrService.get_word(Onmyoji.deed_MQSS)
            if num_stone:
                if num_stone != '0':
                    logger.debug("鸣契石契灵召唤,5次")
                    for i_call in range(6):
                        logger.debug("鸣契石契灵召唤,第{}次", i_call + 1)
                        ImageService.touch(Onmyoji.deed_MQZH)
                        logger.debug("镇墓兽")
                        ImageService.touch(Onmyoji.deed_ZHZMS)
                        logger.debug("召唤确认")
                        is_confirm = ImageService.touch(Onmyoji.deed_ZHQR)
                        if not is_confirm:
                            logger.debug("可能地图已满契灵,或者无鸣契石")
                            break
                    deed_fight()
                else:
                    logger.debug("无鸣契石")
        logger.debug("2.探查50次")
        for i_exploration in range(50):
            logger.debug("点击探查{}", i_exploration + 1)
            ImageService.touch(Onmyoji.deed_TC)
            logger.debug("等待战斗结果")
            is_result = ComplexService.fight_end(Onmyoji.deed_ZDSL, Onmyoji.deed_ZDSB, Onmyoji.deed_ZCTZ,
                                                 Onmyoji.deed_TCTZ, Onmyoji.deed_TC, None, 60, 4)
            if is_result in [Onmyoji.deed_ZDSB, Onmyoji.deed_ZCTZ]:
                logger.debug("阵容问题，退出循环")
                break
            elif is_result in [Onmyoji.deed_TC]:
                logger.debug("契灵已满")
                break
        logger.debug("3.探查后契灵战斗")
        deed_fight()
    logger.debug("确认返回首页")
    impl_initialization.return_home(game_task)
    time_all = time.time() - time_start
    # 记录项目执行结果
    game_project_log = GameProjectLog(project_id=game_project.id, role_id=game_account.id, devices_id=game_devices.id,
                                      result='当前状态初始化', cost_time=int(time_all))
    Mapper.save_game_project_log(game_project_log)
    logger.debug("契灵战斗，{}", UtilsTime.convert_seconds(time_all))


def deed_fight():
    """
    契灵战斗
    :return:
    """
    is_unlock = False
    for i in range(1, 50):
        logger.debug("检查契灵地图，判断当前是否存在契灵")
        is_boss = ImageService.exists(Onmyoji.deed_QL)
        if is_boss:
            logger.debug("地图存在契灵,点击地图上契灵")
            ImageService.touch_coordinate(is_boss)
        logger.debug("判断当前是否是契灵结契界面")
        is_fight = ImageService.exists(Onmyoji.deed_QLJQYM)
        if is_fight:
            logger.debug("契灵结契界面")
            if is_unlock or i == 1:
                ImageService.touch(Onmyoji.deed_SDZR)
            logger.debug("点击契灵挑战")
            ImageService.touch(Onmyoji.deed_QLTZ)
            is_auto = ImageService.exists(Onmyoji.deed_ZDZD, timeouts=5)
            if not is_auto:
                ComplexService.refuse_reward()
                logger.debug("重新点击契灵挑战")
                ImageService.touch(Onmyoji.deed_QLTZ)
                logger.debug("点击准备")
                is_unlock = ImageService.touch(Onmyoji.deed_ZB)
            is_result = ComplexService.fight_end(Onmyoji.deed_ZDSL, Onmyoji.deed_ZDSL, Onmyoji.deed_ZCTZ,
                                                 Onmyoji.deed_TCTZ, Onmyoji.deed_QLTZ, None, 300, 2)
            if is_result in [Onmyoji.deed_ZDSB, Onmyoji.deed_ZCTZ]:
                logger.debug("阵容问题，退出循环")
                break
        else:
            logger.debug("不存在契灵")
            break
