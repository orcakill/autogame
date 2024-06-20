"""
# @Time: 2023年08月31日01:40
# @Author: orcakill
# @File: impl_friends.py
# @Description: 好友协战
"""
import time

from src.dao.mapper import Mapper
from src.model.enum import Onmyoji, Cvstrategy
from src.model.models import GameAccount, GameProjectsRelation, GameProjects, GameProject, GameDevices, GameProjectLog
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.impl_onmyoji_service import impl_awakening, impl_initialization
from src.service.ocr_service import OcrService
from src.utils.my_logger import logger
from src.utils.utils_time import UtilsTime


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
    game_projects = GameProjects(game_task[0])
    game_projects_relation = GameProjectsRelation(game_task[1])
    game_account = GameAccount(game_task[2])
    game_project = GameProject(game_task[3])
    game_devices = GameDevices(game_task[4])
    logger.debug(game_account.role_name)
    logger.debug("好友协战")
    for i_cooperative_warfare in range(2):
        logger.debug("协战开始,第{}次", i_cooperative_warfare + 1)
        logger.debug("确认首页")
        ComplexService.refuse_reward()
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
            logger.debug("已完成协战，返回首页")
            ImageService.touch(Onmyoji.comm_FH_YSJZDHBSCH)
            continue
        else:
            logger.debug("未完成协战，返回首页")
            ImageService.touch(Onmyoji.comm_FH_YSJZDHBSCH)
        logger.debug("好友魂十协战-进入探索")
        ImageService.touch(Onmyoji.home_TS)
        logger.debug("点击御魂图标")
        ImageService.touch(Onmyoji.soul_BQ_YHTB)
        logger.debug("选择")
        ImageService.touch(Onmyoji.soul_BQ_XZ)
        logger.debug("点击可能存在的八岐大蛇眼睛")
        ImageService.touch(Onmyoji.soul_BQ_BQDSYJ)
        # 层号选择 魂一、魂十、魂十一
        logger.debug("选择层号")
        ComplexService.swipe_floor(Onmyoji.soul_BQ_CZ, Onmyoji.soul_BQ_HTEN, 1, 4)
        logger.debug("判断是否在八岐大蛇首页")
        is_home = ImageService.exists(Onmyoji.soul_BQ_BQDSSY)
        if not is_home:
            break
        logger.debug("好友协战-开启御魂加成")
        ComplexService.top_addition(Onmyoji.soul_BQ_JC, Onmyoji.soul_BQ_YHJC,
                                    Onmyoji.soul_BQ_JCK, Onmyoji.soul_BQ_JCG, 1)
        logger.debug("判断右侧是否有御魂自选")
        is_self_selection = ImageService.touch(Onmyoji.soul_BQ_YHZX)
        if is_self_selection:
            logger.debug("返回")
            ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH)
        # 默认有协战式神
        is_assist_shikigami = True
        # 默认锁定阵容
        is_unlock = False
        for i in range(16):
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
                logger.debug("判断右侧是否有御魂自选")
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
                ImageService.touch(Onmyoji.soul_BQ_DJDB, timeouts=10)
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
                    logger.debug("点击准备")
                    ImageService.touch(Onmyoji.soul_BQ_ZB)
            else:
                logger.debug("其它次数挑战")
                if is_unlock:
                    logger.debug("锁定阵容")
                    ImageService.touch(Onmyoji.soul_BQ_SDZR)
                    is_unlock = False
                logger.debug("点击挑战")
                ImageService.touch(Onmyoji.soul_BQ_TZ)
            if not is_assist_shikigami:
                logger.debug("无协战式神，结束循环")
                logger.debug("返回一次")
                ImageService.touch(Onmyoji.comm_FH_ZSJZKDZSHXJT)
                logger.debug("返回两次")
                ImageService.touch(Onmyoji.comm_FH_ZSJZKDZSHXJT)
                logger.debug("确认")
                ImageService.touch(Onmyoji.soul_BQ_QR)
                logger.debug("战斗失败")
                ImageService.touch(Onmyoji.soul_BQ_ZDSB)
                logger.debug("锁定阵容")
                ImageService.touch(Onmyoji.soul_BQ_SDZR, wait=5)
                break
            logger.debug("进入自动战斗")
            is_auto = ImageService.exists(Onmyoji.soul_BQ_ZD, timeouts=10)
            if not is_auto:
                logger.debug("拒接协战")
                ComplexService.refuse_reward()
                logger.debug("加成取消")
                ImageService.touch(Onmyoji.soul_BQ_JCQX)
                logger.debug("退出挑战")
                ComplexService.get_reward(Onmyoji.soul_BQ_TCTZ)
                logger.debug("发现宝藏")
                ComplexService.get_reward(Onmyoji.soul_BQ_FXBZ)
                logger.debug("检查是否存在御魂自选")
                is_select_soul = ImageService.exists(Onmyoji.soul_BQ_SYJC)
                if is_select_soul:
                    logger.debug("点击御魂自选返回")
                    ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH)
                logger.debug("检查是否超时,重新开启加成")
                logger.debug("重新点击八岐大蛇挑战")
                ImageService.touch(Onmyoji.soul_BQ_TZ, wait=2)
                logger.debug("重新点击准备")
                is_unlock = ImageService.touch(Onmyoji.soul_BQ_ZB, wait=4)
                logger.debug("重新检查自动战斗")
                is_auto = ImageService.exists(Onmyoji.soul_BQ_ZD, timeouts=10)
            if is_auto:
                logger.debug("好友协战-等待战斗结果")
                is_result = ComplexService.fight_end(Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_ZDSB,
                                                     Onmyoji.soul_BQ_ZCTZ, Onmyoji.soul_BQ_TCTZ,
                                                     Onmyoji.soul_BQ_TZ, None, 120, 1)
                if i == 0:
                    logger.debug("第一次战斗结束，发现宝藏")
                    ComplexService.get_reward(Onmyoji.soul_BQ_FXBZ)
                    logger.debug("锁定阵容")
                    ImageService.touch(Onmyoji.soul_BQ_SDZR)
                if is_result in [Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_TCTZ]:
                    logger.debug("好友协战-战斗胜利")
                    num_win = num_win + 1
                elif is_result in [Onmyoji.soul_BQ_ZCTZ, Onmyoji.soul_BQ_ZDSB]:
                    logger.debug("好友协战-战斗失败")
                    num_fail = num_fail + 1
                time_fight_end = time.time()
                time_fight_time = time_fight_end - time_fight_start
                logger.debug("本次好友协战，用时{}秒", round(time_fight_time))
                time_fight_list.append(time_fight_time)
                if is_result in [Onmyoji.soul_BQ_ZCTZ, Onmyoji.soul_BQ_ZDSB]:
                    logger.debug("战斗失败，阵容有问题，结束循环")
                    break
            else:
                logger.debug("不在自动战斗中")
        time.sleep(3)
        logger.debug("好友协战-关闭御魂加成")
        ComplexService.top_addition(Onmyoji.soul_BQ_JC, Onmyoji.soul_BQ_YHJC, Onmyoji.soul_BQ_JCK,
                                    Onmyoji.soul_BQ_JCG, 0)
        logger.debug("加成取消")
        ImageService.touch(Onmyoji.soul_BQ_JCQX)
        logger.debug("拒接悬赏")
        ComplexService.refuse_reward()
        logger.debug("好友协战-战斗结束，返回首页")
        ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
        logger.debug("好友协战-返回首页")
        ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH, wait=5)
        ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH, wait=5)
        logger.debug("好友协战-确认返回首页")
        impl_initialization.return_home(game_task)
    logger.debug("返回首页")
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
    # 记录项目执行结果
    game_project_log = GameProjectLog(project_id=game_project.id, role_id=game_account.id, devices_id=game_devices.id,
                                      result='好友协战', cost_time=int(time_all),
                                      fight_time=time_fight_all, fight_times=len_time_fight_list, fight_win=num_win,
                                      fight_fail=num_fail,
                                      fight_avg=time_fight_avg)
    Mapper.save_game_project_log(game_project_log)
    logger.debug("本轮好友协战总用时{}秒，战斗总用时{}秒,平均战斗用时{}秒，挑战{}次，胜利{}次，失败{}次",
                 UtilsTime.convert_seconds(time_all), UtilsTime.convert_seconds(time_fight_all), time_fight_avg,
                 len_time_fight_list, num_win, num_fail)


def friends_manage(game_task: []):
    # 开始时间
    time_start = time.time()
    # 项目信息
    (game_projects_relation, game_account,
     game_project, game_devices) = (GameProjectsRelation(game_task[1]), GameAccount(game_task[2]),
                                    GameProject(game_task[3]), GameDevices(game_task[4]))
    logger.debug(game_account.role_name)
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
        logger.debug("点击输入祝福语")
        is_text = ImageService.touch(Onmyoji.friends_SRZFZY)
        if is_text:
            ImageService.text("666")
        logger.debug("祝福按钮")
        ImageService.touch(Onmyoji.friends_ZFAN)
        ImageService.touch(Onmyoji.friends_ZFAN)
        logger.debug("获得奖励")
        ComplexService.get_reward(Onmyoji.friends_HDJL)
    else:
        logger.debug("无一键祝福")
    logger.debug("返回到好友界面")
    ImageService.touch(Onmyoji.comm_FH_YSJZDHBSCH)
    logger.debug("好友添加")
    logger.debug("获取好友数")
    result_friend = OcrService.get_word(Onmyoji.friends_HYSQY)
    if result_friend:
        if result_friend != '200':
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
    logger.debug("确认返回首页")
    impl_initialization.return_home(game_task)
    time_all = time.time() - time_start
    # 记录项目执行结果
    game_project_log = GameProjectLog(project_id=game_project.id, role_id=game_account.id, devices_id=game_devices.id,
                                      result='好友管理', cost_time=int(time_all))
    Mapper.save_game_project_log(game_project_log)
    logger.debug("好友管理,用时{}秒", round(time_all))
