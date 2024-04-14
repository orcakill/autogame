# @Time: 2023年09月19日 11:53
# @Author: orcakill
# @File: impl_pvp.py
# @Description: 斗技
import datetime
import time

from src.dao.mapper import Mapper
from src.model.enum import Onmyoji
from src.model.models import GameProjectsRelation, GameAccount, GameProject, GameDevices, GameProjectLog
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.impl_onmyoji_service import impl_initialization
from src.utils.my_logger import logger
from src.utils.utils_time import UtilsTime


def pvp(game_task):
    """
    斗技 名士以下
    :param game_task: 任务信息
    :return: 
    """
    # 开始时间
    time_start = time.time()
    # 项目信息
    (game_projects_relation, game_account,
     game_project, game_devices) = (GameProjectsRelation(game_task[1]), GameAccount(game_task[2]),
                                    GameProject(game_task[3]), GameDevices(game_task[4]))
    # 战斗失败次数
    num_fail = 0
    # 战斗胜利次数
    num_win = 0
    # 战斗用时列表
    time_fight_list = []
    # 项目组项目关系
    game_projects_relation = GameProjectsRelation(game_task[1])
    # 项目战斗次数
    fight_time = 10
    if game_projects_relation.project_num_times:
        logger.debug("任务执行次数{}", game_projects_relation.project_num_times)
        fight_time = game_projects_relation.project_num_times
    now = datetime.datetime.now()
    current_hour = now.hour
    # 判断是否有庭院
    is_courtyard = False
    # 默认不在斗技首页
    is_home = False
    if 12 <= current_hour <= 22:
        for i in range(3):
            logger.debug("斗技-进入町中")
            ImageService.touch(Onmyoji.home_DZ)
            logger.debug("斗技-判断是否有庭院")
            is_courtyard = ImageService.exists(Onmyoji.contend_TY)
            if is_courtyard:
                logger.debug("旧版町中，点击旧版斗技入口")
                ImageService.touch(Onmyoji.contend_JBDJRK)
            logger.debug("点击可能存在的确定")
            ImageService.touch(Onmyoji.contend_QD, wait=5)
            logger.debug("判断是否在斗技首页")
            is_home = ImageService.touch(Onmyoji.contend_DJSY)
            if is_home:
                break
            else:
                ComplexService.refuse_reward()
        if is_home:
            for i in range(fight_time):
                time_fight_start = time.time()
                logger.debug("判断是否有练习")
                is_practice = ImageService.exists(Onmyoji.contend_LX)
                if is_practice:
                    logger.debug("练习，无法战斗")
                    break
                logger.debug("斗技-挑战{}次", i + 1)
                is_fight = ImageService.touch(Onmyoji.contend_TZ)
                if not is_fight:
                    # 拒接悬赏
                    ComplexService.refuse_reward()
                    logger.debug("斗技-点击可能的准备")
                    ImageService.touch(Onmyoji.contend_ZB)
                    logger.debug("斗技-点击可能的退出挑战")
                    ImageService.touch(Onmyoji.contend_TCTZ)
                    logger.debug("斗技-点击可能存在的段位晋升")
                    ComplexService.get_reward(Onmyoji.contend_DWJS)
                    logger.debug("斗技-再次点击挑战")
                    ImageService.touch(Onmyoji.contend_TZ)
                logger.debug("等待5s")
                time.sleep(5)
                for i_auto in range(10):
                    logger.debug("战前准备{}", i_auto + 1)
                    logger.debug("点击自动选择")
                    ImageService.touch(Onmyoji.contend_ZDXZ)
                    logger.debug("点击可能存在的准备")
                    ImageService.touch(Onmyoji.contend_ZB)
                    logger.debug("点击可能存在的手动战斗，进入自动战斗")
                    ImageService.touch(Onmyoji.contend_SDZD)
                    logger.debug("判断是否进入自动战斗")
                    is_auto = ImageService.exists(Onmyoji.contend_ZDZD)
                    if is_auto:
                        break
                    logger.debug("判断是否直接战斗胜利")
                    is_win = ImageService.exists(Onmyoji.contend_ZDSL)
                    if is_win:
                        break
                    logger.debug("判断还在挑战页面")
                    is_fight = ImageService.exists(Onmyoji.contend_TZ)
                    if is_fight:
                        logger.debug("再次点击挑战")
                        ImageService.touch(Onmyoji.contend_TZ)
                logger.debug("斗技-等待战斗结果")
                is_result = ComplexService.fight_end(Onmyoji.contend_BDTC, Onmyoji.contend_ZDSB, Onmyoji.contend_ZDSB,
                                                     Onmyoji.contend_ZDSL, Onmyoji.contend_TZ, None, 600, 2)
                if i < 6:
                    logger.debug("战斗次数小于5,点击可能存在的退出挑战")
                    ImageService.touch(Onmyoji.contend_TCTZ)
                logger.debug("点击可能存在的段位晋升")
                ComplexService.get_reward(Onmyoji.contend_DWJS)
                # 记录战斗结果
                if is_result in [Onmyoji.contend_ZDSL, Onmyoji.contend_BDTC]:
                    logger.debug("斗技-战斗胜利")
                    num_win = num_win + 1
                elif is_result in [Onmyoji.contend_ZDSB]:
                    logger.debug("斗技-战斗失败")
                    num_fail = num_fail + 1
                time_fight_end = time.time()
                time_fight_time = time_fight_end - time_fight_start
                logger.debug("本次斗技，用时{}秒", round(time_fight_time))
                time_fight_list.append(time_fight_time)
        else:
            logger.debug("不在斗技首页")
        logger.debug("斗技-返回首页")
        ImageService.touch(Onmyoji.comm_FH_ZSJHKZDHSXYH)
        ImageService.touch(Onmyoji.comm_FH_ZSJHKZDHSXYH)
        if is_courtyard:
            logger.debug("点击庭院返回首页")
            ImageService.touch(Onmyoji.contend_TY)
        time.sleep(5)
        logger.debug("斗技-确认返回首页")
        impl_initialization.return_home(game_task)
    else:
        logger.debug("不在斗技战斗时间")
    # 斗技-结束时间
    time_end = time.time()
    # 斗技-总用时
    time_all = time_end - time_start
    # 斗技-战斗次数
    len_time_fight_list = len(time_fight_list)
    # 斗技-战斗总用时
    time_fight_all = round(sum(time_fight_list))
    # 斗技-平均战斗用时
    time_fight_avg = 0
    if len_time_fight_list > 0:
        logger.debug("斗技-计算平均战斗用时")
        time_fight_avg = round(sum(time_fight_list) / len(time_fight_list), 3)
    # 记录项目执行结果
    game_project_log = GameProjectLog(project_id=game_project.id, role_id=game_account.id, devices_id=game_devices.id,
                                      result='斗技完成', cost_time=int(time_all),
                                      fight_time=time_fight_all, fight_times=len_time_fight_list, fight_win=num_win,
                                      fight_fail=num_fail,
                                      fight_avg=time_fight_avg)
    Mapper.save_game_project_log(game_project_log)
    logger.debug("本轮斗技挑战，总用时{}秒，战斗总用时{}秒,平均战斗用时{}秒，挑战{}次，胜利{}次，失败{}次",
                 UtilsTime.convert_seconds(time_all), time_fight_all, time_fight_avg, len_time_fight_list, num_win,
                 num_fail)
