"""
# @Time: 2023年08月31日01:12
# @Author: orcakill
# @File: impl_border.py
# @Description: 结界突破-阴阳寮突破、个人突破
"""
import time

from src.dao.mapper import Mapper
from src.model.enum import Onmyoji, Cvstrategy
from src.model.models import GameAccount, GameProjectsRelation, GameDevices, GameProject, GameProjectLog
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.impl_onmyoji_service import impl_initialization
from src.service.ocr_service import OcrService
from src.utils.my_logger import logger
from src.utils.utils_time import UtilsTime


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
    # 项目信息
    (game_projects_relation, game_account,
     game_project, game_devices) = (GameProjectsRelation(game_task[1]), GameAccount(game_task[2]),
                                    GameProject(game_task[3]), GameDevices(game_task[4]))
    # 结界突破战斗用时
    time_fight_list = []
    for i in range(3):
        logger.debug("进入探索")
        ImageService.touch(Onmyoji.home_TS)
        logger.debug("进入结界突破")
        ImageService.touch(Onmyoji.region_JJTPTB)
        logger.debug("进入寮突破")
        ImageService.touch(Onmyoji.region_YCYYL)
        logger.debug("判断是否有右侧阴阳寮")
        is_region_home = ImageService.exists(Onmyoji.region_YCYYL)
        if is_region_home:
            logger.debug("当前寮结界首页")
            break
        else:
            ComplexService.refuse_reward()
    logger.debug("检查寮结界是否已攻破")
    is_over = ImageService.exists(Onmyoji.region_TPJDM)
    logger.debug("锁定阵容")
    ImageService.touch(Onmyoji.region_SDZR)
    # 检查是否已攻破100%,已有则插入"阴阳寮已攻破"
    logger.debug("检查寮结界")
    is_fight = ImageService.exists(Onmyoji.region_LJJ, cvstrategy=Cvstrategy.default)
    logger.debug("检查寮结界挑战次数")
    is_fight_times = OcrService.get_word(Onmyoji.region_TZCS)
    # 有寮结界  有挑战次数
    if is_fight and is_fight_times is not None and is_fight_times != '0':
        logger.debug("阴阳寮突破开始")
        for i_fight in range(9):
            time_fight_start = time.time()
            logger.debug("阴阳寮突破{}次", i_fight + 1)
            if game_account.role_class == "0":
                logger.debug("大号-点击寮结界")
                ImageService.touch(Onmyoji.region_LJJ, cvstrategy=Cvstrategy.default)
            else:
                logger.debug("小号-点击寮结界，不打战败")
                ImageService.touch(Onmyoji.region_LJJ, cvstrategy=Cvstrategy.default)
            logger.debug("点击进攻")
            ImageService.touch(Onmyoji.region_JG)
            logger.debug("检查自动战斗")
            is_auto = ImageService.exists(Onmyoji.region_ZD, timeouts=10)
            if not is_auto:
                logger.debug("拒接悬赏")
                ComplexService.refuse_reward()
                logger.debug("点击可能存在的退出挑战")
                ImageService.touch(Onmyoji.region_TCTZ)
                logger.debug("点击可能存在的战斗失败")
                ImageService.touch(Onmyoji.region_ZDSB)
                logger.debug("再次点击寮结界")
                is_fight = ImageService.touch(Onmyoji.region_LJJ, cvstrategy=Cvstrategy.default)
                if not is_fight:
                    logger.debug("仍未找到寮结界")
                    is_break_through = ImageService.find_all(Onmyoji.region_GP)
                    if is_break_through and len(is_break_through) >= 8:
                        logger.debug("当前寮结界已全部攻破")
                        break
                logger.debug("再次点击进攻")
                ImageService.touch(Onmyoji.region_JG)
                logger.debug("再次检查自动战斗")
                is_auto = ImageService.exists(Onmyoji.region_ZD, timeouts=10)
            if not is_auto:
                logger.debug("未进入自动战斗，可能已被挑战,点击左侧突破进度")
                ImageService.touch(Onmyoji.region_ZCTPJD)
                logger.debug("寮结界挑战次数")
                is_fight_times = OcrService.get_word(Onmyoji.region_TZCS)
                if is_fight_times is not None and is_fight_times == '0':
                    logger.debug("寮结界次数为0")
                    break
            else:
                logger.debug("等待战斗结果")
                is_result = ComplexService.fight_end(Onmyoji.region_ZDSL, Onmyoji.region_ZDSB, Onmyoji.region_ZCTZ,
                                                     Onmyoji.region_TCTZ, Onmyoji.region_LJJ, Onmyoji.region_JG, 300, 2)
                if is_result in [Onmyoji.region_ZDSL, Onmyoji.region_TCTZ]:
                    num_win = num_win + 1
                elif is_result in [Onmyoji.border_ZCTZ, Onmyoji.border_ZDSB]:
                    num_fail = num_fail + 1
                elif is_result in [Onmyoji.comm_SL]:
                    logger.debug("失联")
                    break
                time_fight_end = time.time()
                time_fight_time = time_fight_end - time_fight_start
                logger.debug("本次阴阳寮突破，用时{}秒", round(time_fight_time))
                time_fight_list.append(time_fight_time)
    else:
        logger.debug("无寮结界或者无挑战次数")
    logger.debug("阴阳寮突破-返回首页")
    ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH)
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH, wait=2)
    logger.debug("阴阳寮突破-确认返回首页")
    impl_initialization.return_home(game_task)
    # 结束时间
    time_end = time.time()
    # 战斗总用时
    time_fight_all = round(sum(time_fight_list))
    # 总用时
    time_all = time_end - time_start
    # 战斗次数
    len_time_fight_list = len(time_fight_list)
    # 平均战斗用时
    time_fight_avg = 0
    if len_time_fight_list > 0:
        time_fight_avg = round(sum(time_fight_list) / len(time_fight_list), 3)
    # 记录项目执行结果
    game_project_log = GameProjectLog(project_id=game_project.id, role_id=game_account.id, devices_id=game_devices.id,
                                      result="阴阳寮突破", cost_time=int(time_all),
                                      fight_time=time_fight_all, fight_times=len_time_fight_list, fight_win=num_win,
                                      fight_fail=num_fail, fight_avg=time_fight_avg)
    if len_time_fight_list > 0:
        game_project_log.result = game_project_log.result + "战斗完成"
        logger.debug("本轮阴阳寮总用时{}秒，战斗总用时{}秒,平均战斗用时{}秒，挑战{}次，胜利{}次，失败{}次",
                     UtilsTime.convert_seconds(time_all), UtilsTime.convert_seconds(time_fight_all), time_fight_avg,
                     len_time_fight_list, num_win, num_fail)
    else:
        if is_over:
            game_project_log.result = game_project_log.result + "突破进度100%"
            logger.debug("突破进度100%，总用时{}秒", UtilsTime.convert_seconds(time_all))
        else:
            game_project_log.result = game_project_log.result + "无寮结界或无战斗次数"
            logger.debug("无寮结界或无战斗次数，总用时{}秒", UtilsTime.convert_seconds(time_all))
    Mapper.save_game_project_log(game_project_log)


def border_fight(game_task: [], fight_times: int = 40):
    """
    结界突破 border
    :param fight_times: 默认战斗次数
    :param game_task: 项目信息
    :return:
    """
    # 项目信息
    (game_projects_relation, game_account,
     game_project, game_devices) = (GameProjectsRelation(game_task[1]), GameAccount(game_task[2]),
                                    GameProject(game_task[3]), GameDevices(game_task[4]))
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
    # 默认锁定阵容
    is_unlock = False
    is_border_home = False
    for i in range(3):
        logger.debug(game_account.role_name)
        logger.debug("进入探索")
        ImageService.touch(Onmyoji.home_TS)
        logger.debug("进入结界突破")
        ImageService.touch(Onmyoji.border_JJTPTB)
        is_border_home = ImageService.exists(Onmyoji.border_JJSY)
        if is_border_home:
            logger.debug("进入结界首页")
            break
        else:
            ComplexService.refuse_reward()
    if is_border_home:
        logger.debug("结界首页")
        for i in range(fight_times):
            time_fight_start = time.time()
            logger.debug("结界突破{}次", i + 1)
            if time.time() - time_start_border > 40 * 60:
                logger.debug("战斗时间超40分钟，强制结束")
                break
            if i == 0:
                logger.debug("第一次战斗，获取当前结界挑战劵数")
                num_securities = OcrService.get_word(Onmyoji.border_JJTZJQY)
                if num_securities == "0":
                    logger.debug("无结界挑战劵")
                    break
            if num_false % 3 == 0 and num_false > 0:
                logger.debug("战斗失败累计{}次，3的倍数,判断是否有战败标志", num_false)
                is_fail = ImageService.exists(Onmyoji.border_ZBBZ, timeouts=3)
                if is_fail:
                    logger.debug("判断是否有刷新")
                    is_rush = ImageService.exists(Onmyoji.border_SX)
                    if is_rush:
                        logger.debug("有战败标志，战斗失败累计{}次，3的倍数，点击刷新", num_false)
                        ImageService.touch(Onmyoji.border_SX, wait=2)
                        logger.debug("点击刷新确定")
                        ImageService.touch(Onmyoji.border_SXQD, wait=2)
            # 保级，打9退4
            logger.debug("统计攻破次数")
            num_break = ImageService.find_all_num(Onmyoji.border_GP)
            logger.debug("当前攻破数{}", num_break)
            if num_break and num_break == 8:
                logger.debug("保级")
                logger.debug("保级前获取当前结界挑战劵数")
                num_securities = OcrService.get_word(Onmyoji.border_JJTZJQY)
                if num_securities == "0":
                    logger.debug("无结界挑战劵，退出循环")
                    break
                else:
                    logger.debug("有结界挑战劵，保级")
                    retreat_class(0)
            if is_unlock:
                logger.debug("锁定阵容")
                ImageService.touch(Onmyoji.border_SDZR)
            logger.debug("点击个人结界")
            ImageService.touch(Onmyoji.border_GRJJ, cvstrategy=Cvstrategy.default, wait=2)
            logger.debug("点击进攻")
            ImageService.touch(Onmyoji.border_JG, cvstrategy=Cvstrategy.default, wait=2)
            logger.debug("检查自动战斗")
            is_auto = ImageService.exists(Onmyoji.region_ZD, timeouts=10)
            if not is_auto:
                logger.debug("拒接悬赏")
                ComplexService.refuse_reward()
                logger.debug("点击可能存在的退出挑战")
                ImageService.touch(Onmyoji.border_TCTZ)
                logger.debug("再次点击个人结界")
                ImageService.touch(Onmyoji.border_GRJJ, cvstrategy=Cvstrategy.default, wait=2)
                logger.debug("再次点击进攻")
                ImageService.touch(Onmyoji.border_JG, cvstrategy=Cvstrategy.default, wait=2)
                logger.debug("再次检查自动战斗")
                is_auto = ImageService.exists(Onmyoji.region_ZD, timeouts=10)
                logger.debug("可能已无结界挑战劵,点击消耗")
                ImageService.touch(Onmyoji.border_XH)
                logger.debug("判断是否存在结界挑战劵0/30")
                is_securities = OcrService.get_word(Onmyoji.border_JJTZJQY)
                if is_securities == "0":
                    logger.debug("无结界挑战劵，跳出循环")
                    break
            if is_auto:
                logger.debug("点击准备")
                is_unlock = ImageService.touch(Onmyoji.border_ZB, wait=10)
                logger.debug("等待战斗结果")
                is_result = ComplexService.fight_end(Onmyoji.border_ZDSL, Onmyoji.border_ZDSB, Onmyoji.border_ZCTZ,
                                                     Onmyoji.border_TCTZ, Onmyoji.border_GRJJ, Onmyoji.border_JG, 300,
                                                     1)
                logger.debug("再点击一次退出挑战")
                ImageService.touch(Onmyoji.border_TCTZ, wait=3)
                if is_result in [Onmyoji.border_ZDSL, Onmyoji.border_TCTZ]:
                    num_win = num_win + 1
                elif is_result in [Onmyoji.border_ZCTZ, Onmyoji.border_ZDSB]:
                    num_false = num_false + 1
                elif is_result in [Onmyoji.border_GRJJ, Onmyoji.border_JG]:
                    logger.debug("判断是否仍有进攻")
                    is_attack1 = ImageService.exists(Onmyoji.border_JG, wait=5, timeouts=2, is_click=True)
                    if is_attack1:
                        logger.debug("可能已无结界挑战劵,点击消耗退出")
                        ImageService.touch(Onmyoji.border_XH)
                        logger.debug("判断是否存在结界挑战劵0/30")
                        is_securities = OcrService.get_word(Onmyoji.border_JJTZJQY)
                        if is_securities == "0":
                            logger.debug("无结界挑战劵，跳出循环")
                            break
                elif is_result in [Onmyoji.comm_SL]:
                    logger.debug("失联掉线")
                    break
                time_fight_end = time.time()
                time_fight = time_fight_end - time_fight_start
                logger.debug("本次结界突破战斗结束，用时{}秒", round(time_fight, 3))
                time_fight_list.append(time_fight)
    else:
        logger.debug("未进入结界首页")
    logger.debug("返回探索界面")
    ImageService.touch(Onmyoji.comm_FH_YSJZDHBSCH)
    logger.debug("返回首页")
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    logger.debug("确认返回首页")
    impl_initialization.return_home(game_task)
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
    # 记录项目执行结果
    game_project_log = GameProjectLog(project_id=game_project.id, role_id=game_account.id, devices_id=game_devices.id,
                                      result=game_project.project_name, cost_time=int(time_all),
                                      fight_time=time_fight_all, fight_times=len_time_fight_list, fight_win=num_win,
                                      fight_fail=num_false, fight_avg=time_fight_avg)
    Mapper.save_game_project_log(game_project_log)
    logger.debug(
        "本轮结界突破战斗结束，总用时{}，结界挑战劵{}张，战斗总用时{}秒,战斗次数{}次，胜利{}次，失败{}次，平均用时{}秒",
        UtilsTime.convert_seconds(time_all), num_securities, time_fight_all, len_time_fight_list, num_win, num_false,
        time_fight_avg)


def retreat_class(fight_type: int = 0):
    """
    保级 退4,不刷新
    退级 退9，刷新
    :return:
    """
    num_break = 1
    if fight_type == 0:
        logger.debug("保级开始")
    elif fight_type == 1:
        logger.debug("退级开始")
        num_break = 12
    is_border = ImageService.exists(Onmyoji.border_GRJJ, cvstrategy=Cvstrategy.default)
    if is_border:
        logger.debug("有个人结界，解锁阵容")
        is_unlock = ImageService.touch(Onmyoji.border_JSZR)
        if is_unlock:
            logger.debug("点击个人结界")
            ImageService.touch(Onmyoji.border_GRJJ, cvstrategy=Cvstrategy.default)
            logger.debug("点击进攻")
            ImageService.touch(Onmyoji.border_JG)
            logger.debug("再次挑战{}次", num_break)
            for i_fight in range(num_break):
                logger.debug("{}次退出", i_fight + 1)
                ComplexService.refuse_reward()
                logger.debug("点击左上角退出")
                ImageService.touch(Onmyoji.comm_FH_ZSJZKDZSHXJT, timeouts=15)
                logger.debug("点击确认")
                ImageService.touch(Onmyoji.border_TCQR)
                logger.debug("点击再次挑战")
                ImageService.touch(Onmyoji.border_ZCTZ)
                logger.debug("点击确定")
                ImageService.touch(Onmyoji.border_SXQD)
                if i_fight == num_break - 1:
                    logger.debug("{}次退出", i_fight + 2)
                    for i_quit in range(3):
                        logger.debug("点击左上角退出")
                        ImageService.touch(Onmyoji.comm_FH_ZSJZKDZSHXJT)
                        logger.debug("点击确认")
                        ImageService.touch(Onmyoji.border_TCQR)
                        logger.debug("点击战斗失败")
                        ImageService.touch(Onmyoji.border_ZDSB)
                        logger.debug("锁定阵容")
                        is_lock = ImageService.touch(Onmyoji.border_SDZR)
                        if is_lock:
                            logger.debug("锁定阵容成功")
                            break
            if fight_type == 1:
                logger.debug("退级-点击刷新")
                ImageService.touch(Onmyoji.border_SX)
                logger.debug("退级-点击确定")
                ImageService.touch(Onmyoji.border_SXQD)
        else:
            logger.debug("未解锁")
        logger.debug("保级/退级结束")
