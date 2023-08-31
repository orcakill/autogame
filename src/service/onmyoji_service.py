# @Time: 2023年05月31日 17:51
# @Author: orcakill
# @File: onmyoji_service.py
# @Description: 服务接口
import datetime
import os
import time

from src.model.enum import Onmyoji, Cvstrategy
from src.model.models import GameAccount, GameProjectsRelation, GameProject
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.ocr_service import OcrService
from src.service_onmyoji_impl import impl_border, impl_friends
from src.service_onmyoji_impl import impl_house
from src.utils.my_logger import logger

# 服务接口
image_service = ImageService()
complex_service = ComplexService()
ocr_service = OcrService()


class OnmyojiService:

    @staticmethod
    def initialization(game_task: []):
        """
        项目1 当前状态初始化
        :param game_task: 任务信息
        :return:
        """
        # 开始时间
        time_start = time.time()
        # 账号信息
        game_account = GameAccount(game_task[2])
        # 判断是否是待登录账号首页
        logger.debug("初始化-判断当前状态")
        # 当前状态 账号首页 1，2,3，4
        #        其它，不在账号首页
        account_index = os.path.join(Onmyoji.user_SYTX, game_account.id)
        is_index = image_service.exists(account_index)
        is_explore = image_service.exists(Onmyoji.home_TS)
        if not is_index or not is_explore:
            logger.debug("不在账号首页")
            # 不在账号首页的其它，重启app，根据账号选择用户、服务器、开始游戏
            logger.debug("启动阴阳师app")
            image_service.restart_app("com.netease.onmyoji")
            logger.debug("等待20秒")
            time.sleep(20)
            logger.debug("判断是否存在适龄提示")
            is_ageAppropriateReminder = image_service.exists(Onmyoji.login_SLTS, timeouts=5)
            # 不存在适龄提示
            if not is_ageAppropriateReminder:
                logger.debug("不存在适龄提示")
                for i_ageAppropriateReminder in range(5):
                    logger.debug("点击可能存在的重新打开应用")
                    image_service.touch(Onmyoji.login_CXDKYY)
                    logger.debug("点击左上角，防止有开场动画")
                    image_service.touch_coordinate([10, 10])
                    logger.debug("接受协议")
                    image_service.touch(Onmyoji.login_JSXY)
                    logger.debug("点击公告返回")
                    image_service.touch(Onmyoji.comm_FH_YSJGGCH)
                    logger.debug("重新判断适龄提示")
                    is_ageAppropriateReminder = image_service.exists(Onmyoji.login_SLTS)
                    if is_ageAppropriateReminder:
                        break
                    logger.debug("等待10秒")
                    time.sleep(10)
            logger.debug("接受协议")
            image_service.touch(Onmyoji.login_JSXY)
            logger.debug("登录账号")
            logger.debug("判断当前账号选择")
            is_account_select = image_service.exists(Onmyoji.login_WYYX)
            if not is_account_select:
                logger.debug("用户中心")
                image_service.touch(Onmyoji.login_YHZX, wait=2)
                logger.debug("切换账号")
                image_service.touch(Onmyoji.login_QHZH, cvstrategy=Cvstrategy.default, wait=2)
            logger.debug("常用")
            is_used = image_service.touch(Onmyoji.login_CY, cvstrategy=Cvstrategy.default, wait=2)
            if not is_used:
                logger.debug("用户中心")
                image_service.touch(Onmyoji.login_YHZX, wait=2)
                logger.debug("再次切换账号")
                image_service.touch(Onmyoji.login_QHZH, cvstrategy=Cvstrategy.default, wait=2)
                logger.debug("再此点击常用")
                image_service.touch(Onmyoji.login_CY, cvstrategy=Cvstrategy.default, wait=2)
            logger.debug("选择账号")
            account = os.path.join(Onmyoji.user_XZZH, game_account.account_name)
            image_service.touch(account, cvstrategy=Cvstrategy.default, wait=2)
            logger.debug("登录")
            image_service.touch(Onmyoji.login_DLAN, cvstrategy=Cvstrategy.default, wait=3)
            logger.debug("接受协议")
            image_service.touch(Onmyoji.login_JSXY, wait=3)
            logger.debug("切换服务器")
            image_service.touch(Onmyoji.login_QHFWQ, cvstrategy=Cvstrategy.default, wait=3)
            logger.debug("点击小三角")
            pos_TCS = image_service.exists(Onmyoji.login_TYCS, wait=2)
            pos_JSX = image_service.exists(Onmyoji.login_ZXJS, wait=2)
            if not pos_TCS or not pos_JSX:
                logger.debug("没找到小三角，重新判断是否已点击切换服务器")
                for i_triangle in range(5):
                    logger.debug("点击切换服务器")
                    image_service.touch(Onmyoji.login_QHFWQ, cvstrategy=Cvstrategy.default, wait=3)
                    logger.debug("判断是否有小三角")
                    pos_TCS = image_service.exists(Onmyoji.login_TYCS, wait=2)
                    pos_JSX = image_service.exists(Onmyoji.login_ZXJS, wait=2)
                    if pos_TCS and pos_JSX:
                        break
            if pos_TCS and pos_JSX:
                logger.debug("有小三角")
                image_service.touch_coordinate((pos_TCS[0], pos_JSX[1]))
            logger.debug("选择服务器:{}", game_account.game_region)
            server = os.path.join(Onmyoji.login_FWQ, game_account.game_region)
            is_select = image_service.touch(server, wait=2)
            if not is_select:
                logger.debug("未选择服务器")
            logger.debug("开始游戏")
            is_start = image_service.touch(Onmyoji.login_KSYX, wait=2)
            if not is_start:
                logger.debug("未开始游戏，点击服务器")
                image_service.touch(server, wait=2)
                logger.debug("再次点击开始游戏")
                image_service.touch(Onmyoji.login_KSYX, wait=2)
            time.sleep(15)
        logger.debug("{}首页,判断底部菜单", game_account.game_name)
        is_openBottom = image_service.exists(Onmyoji.home_DBCDDK)
        if not is_openBottom:
            for i_openBottom in range(4):
                logger.debug("当前页面无底部菜单打开")
                logger.debug("点击可能存在的底部菜单")
                image_service.touch(Onmyoji.home_DBCD, timeouts=3)
                is_openBottom = image_service.exists(Onmyoji.home_DBCDDK)
                if is_openBottom:
                    logger.debug("底部菜单已打开")
                    break
                logger.debug("点击可能存在的右上角返回")
                image_service.touch(Onmyoji.comm_FH_YSJHDBSCH, timeouts=3)
                logger.debug("点击可能存在的左上角返回")
                image_service.touch(Onmyoji.comm_FH_ZSJHKZDHSXYH, timeouts=3)
                logger.debug("点击可能存在的下载")
                image_service.touch(Onmyoji.home_XZ, timeouts=3)
                logger.debug("点击可能存在的取消，不打开加成")
                image_service.touch(Onmyoji.home_QX, timeouts=3)
                logger.debug("点击可能存在的底部菜单")
                image_service.touch(Onmyoji.home_DBCD, timeouts=3)
                logger.debug("重新判断是否存在底部菜单打开")
                is_openBottom = image_service.exists(Onmyoji.home_DBCDDK)
                if is_openBottom:
                    logger.debug("底部菜单已打开")
                    break
        logger.debug("重新判断是否在账号首页")
        is_index = image_service.exists(account_index)
        # 结束时间
        time_end = time.time()
        # 总用时
        time_all = time_end - time_start
        if is_index:
            logger.info("初始化当前状态完成:{}，用时{}秒", game_account.game_name, round(time_all))
            return True
        else:
            logger.info("初始化当前状态失败:{}，用时{}秒", game_account.game_name, round(time_all))
            return False

    @staticmethod
    def soul_fight(game_task: []):
        """
        御魂战斗  八岐大蛇
        魂一  第一次战斗检查协战，有协战上协战，没协战直接退出到首页，不开加成
        魂十  第一次战斗检查协战，有协战上协战，开加成，
        魂十一  不检查协战，不上协战，开加成
        :param game_task: 项目组信息
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
        game_projects_relation = GameProjectsRelation(game_task[1])
        game_account = GameAccount(game_task[2])
        logger.debug(game_account.game_name)
        game_project = GameProject(game_task[3])
        fight_time = game_projects_relation.project_num_times
        logger.debug("进入探索")
        image_service.touch(Onmyoji.home_TS)
        logger.debug("进入御魂")
        image_service.touch(Onmyoji.soul_BQ_YHTB)
        logger.debug("进入八岐大蛇")
        image_service.touch(Onmyoji.soul_BQ_XZ)
        logger.debug("开启加成")
        logger.debug("八岐大蛇-选择层号")
        if game_project.project_name == "魂一":
            complex_service.swipe_floor(Onmyoji.soul_BQ_CZ, Onmyoji.soul_BQ_HONE, 0, 4)
        elif game_project.project_name == "魂十":
            complex_service.swipe_floor(Onmyoji.soul_BQ_CZ, Onmyoji.soul_BQ_HTEN, 1, 4)
        elif game_project.project_name == "魂十一":
            complex_service.swipe_floor(Onmyoji.soul_BQ_CZ, Onmyoji.soul_BQ_HELEVEN, 1, 4)
        logger.debug("开启御魂加成")
        complex_service.top_addition(Onmyoji.soul_BQ_JC, Onmyoji.soul_BQ_YHJC, Onmyoji.soul_BQ_JCG, Onmyoji.soul_BQ_JCG,
                                     1)
        logger.debug("锁定阵容")
        image_service.touch(Onmyoji.soul_BQ_SDZR)
        # 默认锁定阵容
        is_lock = False
        for i in range(fight_time):
            time_fight_start = time.time()
            logger.debug("御魂-挑战{}次", i + 1)
            if is_lock:
                logger.debug("可能存在锁定阵容")
                image_service.touch(Onmyoji.soul_BQ_SDZR)
            is_fight = image_service.touch(Onmyoji.soul_BQ_TZ)
            if not is_fight:
                logger.debug("点击可能的准备")
                is_lock = image_service.touch(Onmyoji.soul_BQ_ZB)
            if i == 0:
                logger.debug("喂食")
                is_pets = image_service.touch(Onmyoji.soul_BQ_CW, wait=5)
                if is_pets:
                    logger.debug("点击喂食")
                    image_service.touch(Onmyoji.soul_BQ_WS)
                    logger.debug("获得奖励")
                    complex_service.get_reward(Onmyoji.soul_BQ_HDJL)
            logger.debug("等待战斗结果")
            is_result = complex_service.fight_end(Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_ZDSB, Onmyoji.soul_BQ_ZCTZ,
                                                  Onmyoji.soul_BQ_TCTZ, Onmyoji.soul_BQ_TZ, 60, 1)
            # 记录战斗结果
            if is_result in [Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_TCTZ]:
                num_win = num_win + 1
            elif is_result in [Onmyoji.soul_BQ_ZCTZ]:
                num_fail = num_fail + 1
            if i == 0:
                logger.debug("发现宝藏")
                complex_service.get_reward(Onmyoji.soul_BQ_FXBZ)
            time_fight_end = time.time()
            time_fight_time = time_fight_end - time_fight_start
            logger.debug("本次{}，用时{}秒", game_project.project_name, round(time_fight_time))
            time_fight_list.append(time_fight_time)
        time.sleep(3)
        logger.debug("关闭御魂加成")
        complex_service.top_addition(Onmyoji.soul_BQ_JC, Onmyoji.soul_BQ_YHJC, Onmyoji.soul_BQ_JCG, Onmyoji.soul_BQ_JCG,
                                     0)
        logger.debug("御魂-返回首页")
        image_service.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
        logger.debug("御魂-返回首页")
        image_service.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
        # 御魂结束时间
        time_end = time.time()
        # 御魂总用时
        time_all = time_end - time_start
        # 御魂战斗总用时
        time_fight_all = round(sum(time_fight_list))
        # 御魂战斗次数
        len_time_fight_list = len(time_fight_list)
        # 御魂平均战斗用时
        time_fight_avg = 0
        if len_time_fight_list > 0:
            time_fight_avg = round(sum(time_fight_list) / len(time_fight_list), 3)
        logger.debug("本轮{}御魂挑战，总用时{}秒，战斗总用时{}秒,平均战斗用时{}秒，挑战{}次，胜利{}次，失败{}次",
                     game_project.project_name, round(time_all, 3), time_fight_all, time_fight_avg, len_time_fight_list,
                     num_win, num_fail)

    @staticmethod
    def soul_fight_thug():
        """
        御魂打手
        :return:
        """
        for i in range(1000):
            logger.debug("御魂组队第{}次识别", i + 1)
            complex_service.fight_end(Onmyoji.soul_BQ_JSTXDS, Onmyoji.soul_BQ_TCTZ, Onmyoji.soul_BQ_ZDSB,
                                      Onmyoji.soul_BQ_ZDSB, Onmyoji.soul_BQ_TZ, 60, 1)
            time.sleep(1)

    @staticmethod
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
        image_service.touch(Onmyoji.home_TS)
        logger.debug("进入结界突破")
        image_service.touch(Onmyoji.border_JJTPTB)
        for i in range(fight_times):
            time_fight_start = time.time()
            logger.debug("结界突破{}次", i + 1)
            if i == 0:
                logger.debug("第一次战斗，获取当前结界挑战劵数")
                num_securities = ocr_service.border_bond()
                if num_securities == "0":
                    logger.debug("无结界挑战劵")
                    break
            if num_false % 3 == 0 and num_false != 0:
                logger.debug("战斗失败累计{}次，3的倍数,判断是否有战败标志", num_false)
                is_fail = image_service.exists(Onmyoji.border_ZBBZ, timeouts=3)
                if is_fail:
                    logger.debug("判断是否有刷新")
                    is_rush = image_service.exists(Onmyoji.border_SX)
                    if is_rush:
                        logger.debug("有战败标志，战斗失败累计{}次，3的倍数，点击刷新", num_false)
                        image_service.touch(Onmyoji.border_SX, wait=2)
                        image_service.touch(Onmyoji.border_SXQD, wait=2)
            for i_attack in range(3):
                logger.debug("点击个人结界")
                image_service.touch(Onmyoji.border_GRJJ, cvstrategy=Cvstrategy.default, wait=2)
                logger.debug("点击进攻")
                is_attack = image_service.touch(Onmyoji.border_JG, cvstrategy=Cvstrategy.default, wait=1)
                if is_attack:
                    break
            logger.debug("点击准备")
            image_service.touch(Onmyoji.border_ZB, timeouts=3)
            logger.debug("等待战斗结果")
            is_result = complex_service.fight_end(Onmyoji.border_ZDSL, Onmyoji.border_ZDSB,
                                                  Onmyoji.border_ZCTZ, Onmyoji.border_TCTZ, Onmyoji.border_GRJJ,
                                                  300, 1)
            logger.debug("再点击一次退出挑战")
            image_service.touch(Onmyoji.border_TCTZ, wait=2, timeouts=1)
            if is_result in [Onmyoji.border_ZDSL, Onmyoji.border_TCTZ]:
                num_win = num_win + 1
            elif is_result == Onmyoji.border_ZCTZ:
                num_false = num_false + 1
            elif is_result == Onmyoji.border_GRJJ or is_result is None:
                logger.debug("判断是否仍有进攻")
                is_attack1 = image_service.exists(Onmyoji.border_JG, wait=5, timeouts=2, is_click=True)
                if is_attack1:
                    logger.debug("可能已无结界挑战劵,点击消耗退出")
                    image_service.touch(Onmyoji.border_XH)
                    logger.debug("判断是否存在结界挑战劵0/30")
                    is_securities = ocr_service.border_bond()
                    if is_securities == "0":
                        logger.debug("无结界挑战劵，跳出循环")
                        break
            time_fight_end = time.time()
            time_fight = time_fight_end - time_fight_start
            logger.debug("本次结界突破战斗结束，用时{}秒", round(time_fight, 3))
            time_fight_list.append(time_fight)
        logger.debug("返回探索界面")
        image_service.touch(Onmyoji.comm_FH_YSJZDHBSCH)
        logger.debug("返回首页")
        image_service.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
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

    @staticmethod
    def awakening(game_task: [], awakening_type: int = 0):
        """
            觉醒十 风、火、水、雷（默认雷）  开加成，选觉醒阵容
            :param awakening_type: 默认类型
            :param game_task:  任务信息
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
        # 项目组项目关系
        game_projects_relation = GameProjectsRelation(game_task[1])
        # 账号信息
        game_account = GameAccount(game_task[2])
        fight_time = game_projects_relation.project_num_times
        if fight_time is None:
            fight_time = 1
        # 获取当前日期
        today = datetime.date.today()
        # 获取本日是周几（周一为0，周日为6）
        weekday = today.weekday() + 1
        logger.debug(game_account.game_name)
        logger.debug("进入探索")
        image_service.touch(Onmyoji.home_TS)
        logger.debug("进入觉醒")
        image_service.touch(Onmyoji.awaken_JXBT)
        logger.debug("本日周{}", weekday)
        if awakening_type != 0:
            logger.debug("修改麒麟类型")
            weekday = awakening_type
        if weekday == 1:
            logger.debug("火麒麟")
            image_service.touch(Onmyoji.awaken_QL_H)
        elif weekday == 2:
            logger.debug("风麒麟")
            image_service.touch(Onmyoji.awaken_QL_F)
        elif weekday == 3:
            logger.debug("水麒麟")
            image_service.touch(Onmyoji.awaken_QL_S)
        else:
            logger.debug("雷麒麟")
            image_service.touch(Onmyoji.awaken_QL_L)
        logger.debug("选择层号")
        complex_service.swipe_floor(Onmyoji.awaken_C, Onmyoji.awaken_SC, 1, 4)
        logger.debug("开启加成")
        complex_service.top_addition(Onmyoji.awaken_JC, Onmyoji.awaken_JXJC, Onmyoji.awaken_JCG, Onmyoji.awaken_JCG, 1)
        logger.debug("锁定阵容")
        image_service.touch(Onmyoji.awaken_SDZR)
        for i in range(fight_time):
            time_fight_start = time.time()
            logger.debug("觉醒挑战{}次", i + 1)
            is_fight = image_service.touch(Onmyoji.awaken_TZ)
            logger.debug("点击准备")
            image_service.touch(Onmyoji.awaken_ZB, wait=2)
            if not is_fight:
                logger.debug("再次点击挑战")
                image_service.touch(Onmyoji.awaken_TZ, wait=2)
                logger.debug("点击准备")
                image_service.touch(Onmyoji.awaken_ZB, wait=2)
            logger.debug("等待战斗结果")
            complex_service.fight_end(Onmyoji.awaken_ZDSL, Onmyoji.awaken_ZDSB, Onmyoji.awaken_ZCTZ,
                                      Onmyoji.awaken_TCTZ, Onmyoji.awaken_TZ, 60, 1)
            time_fight_end = time.time()
            time_fight_time = time_fight_end - time_fight_start
            logger.debug("本次阴阳寮突破，用时{}秒", round(time_fight_time))
            time_fight_list.append(time_fight_time)
        time.sleep(2)
        logger.debug("关闭觉醒加成")
        complex_service.top_addition(Onmyoji.awaken_JC, Onmyoji.awaken_JXJC, Onmyoji.awaken_JCG, Onmyoji.awaken_JCG, 0)
        logger.debug("觉醒-返回首页")
        image_service.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
        logger.debug("觉醒-返回首页")
        image_service.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
        # 结束时间
        time_end = time.time()
        # 总用时
        time_all = time_end - time_start
        # 战斗次数
        len_time_fight_list = len(time_fight_list)
        # 战斗总用时
        time_fight_all = round(sum(time_fight_list))
        # 平均战斗用时
        time_fight_avg = 0
        if len_time_fight_list > 0:
            time_fight_avg = round(sum(time_fight_list) / len(time_fight_list), 3)
        logger.debug("本轮觉醒十总用时{}秒，战斗总用时{}秒,平均战斗用时{}秒，挑战{}次，胜利{}次，失败{}次",
                     round(time_all, 3), time_fight_all, time_fight_avg, len_time_fight_list, num_win, num_fail)

    @staticmethod
    def daily_rewards(game_task: []):
        # 开始时间
        time_start = time.time()
        # 账号信息
        game_account = GameAccount(game_task[2])
        logger.debug(game_account.game_name)
        logger.debug("1-首页小纸人奖励")
        logger.debug("判断是否有签到小纸人")
        is_sign_in = image_service.exists(Onmyoji.reward_QDXZR, timeouts=2)
        if is_sign_in:
            logger.debug("有签到小纸人")
            image_service.touch_coordinate(is_sign_in)
            logger.debug("点击每日一签")
            image_service.touch(Onmyoji.reward_MRYQ)
            logger.debug("点击退出挑战")
            image_service.touch(Onmyoji.reward_TCTZ)
            logger.debug("返回首页")
            image_service.touch(Onmyoji.comm_FH_YSJHDBSCH)
        logger.debug("判断是否有体力小纸人")
        is_strength = image_service.exists(Onmyoji.reward_TLXZR, timeouts=2, wait=3)
        if is_strength:
            logger.debug("有体力小纸人")
            image_service.touch_coordinate(is_strength)
            logger.debug("获得体力奖励，退出")
            is_reward = image_service.exists(Onmyoji.reward_HDJL, wait=3)
            if is_reward:
                image_service.touch_coordinate((1 / 2 * is_reward[0], 1 / 2 * is_reward[1]))
        logger.debug("判断是否有勾玉小纸人")
        is_jade = image_service.exists(Onmyoji.reward_GYXZR, timeouts=2, wait=3)
        if is_jade:
            logger.debug("有勾玉小纸人")
            image_service.touch_coordinate(is_jade)
            logger.debug("获得勾玉奖励，退出")
            is_reward = image_service.exists(Onmyoji.reward_HDJL, wait=3)
            if is_reward:
                image_service.touch_coordinate((1 / 2 * is_reward[0], 1 / 2 * is_reward[1]))
        logger.debug("判断是否有御魂觉醒加成小纸人")
        is_soul_addition = image_service.exists(Onmyoji.reward_YHJXJCXZR, timeouts=2, wait=3)
        if is_soul_addition:
            logger.debug("有御魂觉醒加成小纸人")
            image_service.touch_coordinate(is_soul_addition)
            logger.debug("获得奖励，退出")
            is_reward = image_service.exists(Onmyoji.reward_HDJL, wait=3)
            if is_reward:
                image_service.touch_coordinate((1 / 2 * is_reward[0], 1 / 2 * is_reward[1]))
        logger.debug("返回首页")
        ComplexService.return_home(game_task)
        logger.debug("2-邮箱奖励")
        is_mail = image_service.exists(Onmyoji.reward_YX)
        if is_mail:
            logger.debug("点击邮箱")
            image_service.touch_coordinate(is_mail)
            logger.debug("判断是否有全部领取")
            is_get = image_service.exists(Onmyoji.reward_YXQBLQ, wait=3)
            if is_get:
                logger.debug("点击全部领取")
                image_service.touch_coordinate(is_get)
                logger.debug("点击确定")
                image_service.touch(Onmyoji.reward_QD, wait=3)
                logger.debug("获得奖励，退出")
                is_reward = image_service.exists(Onmyoji.reward_HDJL, wait=3)
                if is_reward:
                    image_service.touch_coordinate((1 / 2 * is_reward[0], 1 / 2 * is_reward[1]))
            logger.debug("返回首页")
            image_service.touch(Onmyoji.comm_FH_YSJZDHBSCH, wait=3)
        logger.debug("3-礼包屋奖励")
        is_store = image_service.exists(Onmyoji.store_SDTB)
        if is_store:
            logger.debug("点击商店图标")
            image_service.touch_coordinate(is_store)
            logger.debug("判断是否有右上角返回")
            is_right = image_service.exists(Onmyoji.comm_FH_YSJHDBSCH)
            if is_right:
                image_service.touch_coordinate(is_right)
            logger.debug("点击礼包屋")
            image_service.touch(Onmyoji.store_LBW)
            logger.debug("点击推荐")
            image_service.touch(Onmyoji.store_TJ)
            logger.debug("判断是否有每日领取")
            is_day = image_service.exists(Onmyoji.store_MRLQ, wait=2)
            if is_day:
                image_service.touch_coordinate(is_day)
                logger.debug("获得每日免费奖励，退出")
                is_reward = image_service.exists(Onmyoji.store_HDJL, wait=3)
                if is_reward:
                    image_service.touch_coordinate((1 / 2 * is_reward[0], 1 / 2 * is_reward[1]))
            else:
                logger.debug("无每日免费奖励")
            logger.debug("返回首页")
            image_service.touch(Onmyoji.comm_FH_ZSJHKHSXYH)
            image_service.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
        logger.debug("4-花合战奖励")
        is_flower_battle = image_service.exists(Onmyoji.reward_HHZTB, is_click=True)
        if is_flower_battle:
            logger.debug("点击右侧任务")
            image_service.touch(Onmyoji.reward_YCRW)
            logger.debug("点击全部领取")
            image_service.exists(Onmyoji.reward_HHZQBLQ, is_click=True)
            logger.debug("获得奖励")
            complex_service.get_reward(Onmyoji.reward_HDJL)
            logger.debug("返回首页")
            image_service.touch(Onmyoji.comm_FH_ZSJLDBKBSXYH)
        time_end = time.time() - time_start
        logger.info("每日奖励,用时{}秒", round(time_end))

    @staticmethod
    def encounter_demons(game_task: []):
        """
        逢魔之时
        :param game_task: 任务信息
        :return:
        """
        # 开始时间
        time_start = time.time()
        # 账号信息
        game_account = GameAccount(game_task[2])
        logger.debug(game_account.game_name)
        now = datetime.datetime.now()
        current_hour = now.hour
        is_gathering = False
        if 17 <= current_hour <= 22:
            logger.debug("进入町中")
            image_service.touch(Onmyoji.home_DZ)
            logger.debug("判断是否有庭院")
            is_courtyard = image_service.exists(Onmyoji.demon_TY)
            if is_courtyard:
                logger.debug("旧版町中，点击旧版逢魔之时入口")
                image_service.touch(Onmyoji.demon_JBFMZSRK)
            logger.debug("判断是否已领取现世奖励")
            is_get_reward = image_service.exists(Onmyoji.demon_FMLD, wait=5)
            if is_get_reward:
                logger.debug("未点击现时逢魔，开始点击")
                for i_present in range(2):
                    image_service.touch(Onmyoji.demon_XSFM, wait=3)
                    image_service.touch(Onmyoji.demon_XSFM, wait=3)
                    image_service.touch(Onmyoji.demon_QD, wait=3)
                    image_service.touch(Onmyoji.demon_XSFM, wait=3)
                    image_service.touch(Onmyoji.demon_XSFM, wait=3)
                    logger.debug("重新判断是否已领取现世奖励")
                    is_get_reward = image_service.exists(Onmyoji.demon_FMLD, wait=1)
                    if not is_get_reward:
                        break
                logger.debug("领取奖励")
                image_service.touch(Onmyoji.demon_HSDM, wait=3)
                logger.debug("识别获得奖励")
                is_reward = image_service.exists(Onmyoji.store_HDJL, wait=3)
                if is_reward:
                    image_service.touch_coordinate((1 / 2 * is_reward[0], 1 / 2 * is_reward[1]))
            #  逢魔boss
            logger.debug("逢魔boss")
            logger.debug("判断是否有首领极")
            is_extremely = image_service.exists(Onmyoji.demon_SLJ)
            for i_boss in range(20):
                if is_extremely and game_account.account_class == 0 and i_boss < 10:
                    logger.debug("有首领极，且是大号,打首领极")
                    image_service.touch(Onmyoji.demon_SLJ)
                else:
                    logger.debug("无首领极或是小号，打首领")
                    image_service.touch(Onmyoji.demon_SL)
                logger.debug("点击左下集结")
                is_left_gathering = image_service.touch(Onmyoji.demon_ZXJJ)
                if is_left_gathering:
                    logger.debug("判断是否有集结挑战")
                    is_fight = image_service.exists(Onmyoji.demon_JJTZ)
                    if is_fight:
                        logger.debug("连点5次")
                        for i_click in range(5):
                            image_service.touch_coordinate(is_fight, wait=1)
                    logger.debug("判断是否有一天一层")
                    is_one = image_service.exists(Onmyoji.demon_YTYC, wait=0)
                    if is_one:
                        logger.debug("当日已完成挑战")
                        image_service.touch(Onmyoji.demon_YSJYXHDBSCH, wait=2)
                        break
                    logger.debug("判断是否有集结")
                    is_gathering = image_service.exists(Onmyoji.demon_ZCJJ)
                    if is_gathering:
                        logger.debug("已进入逢魔集结")
                        break
                    else:
                        logger.debug("返回到逢魔页面")
                        image_service.touch(Onmyoji.demon_YSJYXHDBSCH, wait=2)
                else:
                    logger.debug("未找到首领")
            if is_gathering:
                logger.debug("进入boss战,十分钟战斗时间")
                time_start = time.time()
                while time.time() - time_start < 10 * 60:
                    image_service.exists(Onmyoji.demon_ZB, is_click=True)
                    image_service.exists(Onmyoji.demon_ZDSL, is_click=True)
                    is_again = image_service.exists(Onmyoji.demon_ZCTZ, timeouts=1)
                    if is_again:
                        image_service.touch(Onmyoji.demon_ZDSB)
                    image_service.exists(Onmyoji.demon_TCTZ, is_click=True)
                    image_service.exists(Onmyoji.demon_YJHD, is_click=True)
                    is_achievements = image_service.exists(Onmyoji.demon_ZCZJ)
                    if is_achievements:
                        logger.debug("已有战绩，尝试退出")
                        logger.debug("点击退出集结场景")
                        image_service.touch(Onmyoji.comm_FH_ZSJZKDZSHXJT)
                        logger.debug("点击确定")
                        image_service.touch(Onmyoji.demon_QD)
                    is_boss = image_service.exists(Onmyoji.demon_SL)
                    if is_boss:
                        logger.debug("逢魔之时首页，已退出逢魔boss战")
                        break
                    time.sleep(10)
            logger.debug("退出逢魔之时")
            image_service.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
            logger.debug("退出町中")
            if is_courtyard:
                logger.debug("旧版町中，点击庭院")
                image_service.touch(Onmyoji.demon_TY)
        else:
            logger.debug("不在逢魔时间内")
        time_end = time.time() - time_start
        logger.info("逢魔之时,用时{}秒", round(time_end))

    @staticmethod
    def ghost_king(game_task: []):
        # 开始时间
        time_start = time.time()
        # 账号信息
        game_account = GameAccount(game_task[2])
        logger.debug(game_account.game_name)
        now = datetime.datetime.now()
        current_hour = now.hour
        if 6 <= current_hour <= 24:
            logger.debug("进入探索")
            image_service.touch(Onmyoji.home_TS, wait=2)
            logger.debug("进入地域鬼王")
            image_service.touch(Onmyoji.ghost_DYGWTB, wait=2)
            logger.debug("点击今日挑战")
            image_service.touch(Onmyoji.ghost_JRTZ, wait=2)
            logger.debug("判断是否有未挑战")
            is_select = image_service.exists(Onmyoji.ghost_WXZ, cvstrategy=Cvstrategy.default, wait=3)
            if is_select:
                logger.debug("收藏鬼王")
                for i in range(6):
                    logger.debug("点击筛选")
                    image_service.touch(Onmyoji.ghost_SX, wait=3)
                    logger.debug("点击收藏")
                    is_collection = image_service.touch(Onmyoji.ghost_SC, wait=2)
                    if not is_collection:
                        logger.debug("无收藏，重新点击筛选")
                        image_service.touch(Onmyoji.ghost_SX, wait=2)
                        logger.debug("点击收藏")
                        image_service.touch(Onmyoji.ghost_SC, wait=2)
                    if i in [0, 3]:
                        logger.debug("鸟巢")
                        image_service.touch(Onmyoji.ghost_SCGW_NC, wait=2)
                    elif i in [1, 4]:
                        logger.debug("少林寺藏经阁")
                        image_service.touch(Onmyoji.ghost_SCGW_SLSCJG, wait=2)
                    elif i in [2, 5]:
                        logger.debug("黄鹤楼")
                        image_service.touch(Onmyoji.ghost_SXGW_HHL, wait=2)
                    logger.debug("进入鬼王挑战页面")
                    if game_account.account_class == "0":
                        logger.debug("大号，挑战极地域鬼王")
                        logger.debug("判断是否有极标志")
                        is_ordinary = image_service.exists(Onmyoji.ghost_JBZ)
                        if is_ordinary:
                            logger.debug("点击极标志，切换成极地域鬼王")
                            image_service.touch_coordinate(is_ordinary)
                    if game_account.account_class != "0":
                        logger.debug("小号，挑战等级一的地域鬼王")
                        is_first = image_service.exists(Onmyoji.ghost_DJY)
                        if not is_first:
                            logger.debug("不是等级一,点击减号")
                            is_minus = image_service.exists(Onmyoji.ghost_JH)
                            for i_minus in range(60):
                                image_service.touch_coordinate(is_minus)
                                is_first = image_service.exists(Onmyoji.ghost_DJY)
                                if is_first:
                                    logger.debug("检查到等级一")
                                    break
                    logger.debug("判读是否有无字")
                    is_no_word = image_service.exists(Onmyoji.ghost_W)
                    if is_no_word:
                        logger.debug("挑战")
                        image_service.touch(Onmyoji.ghost_TZ, wait=3)
                        logger.debug("准备一次")
                        image_service.touch(Onmyoji.ghost_ZB, wait=3)
                        logger.debug("准备两次")
                        image_service.touch(Onmyoji.ghost_ZB, wait=3)
                        logger.debug("等待战斗结果")
                        complex_service.fight_end(Onmyoji.ghost_ZDSL, Onmyoji.ghost_ZDSB, Onmyoji.ghost_ZCTZ,
                                                  Onmyoji.ghost_TCTZ, Onmyoji.ghost_TZ, 10 * 60, 1)
                    logger.debug("已挑战,返回到鬼王首页")
                    image_service.touch(Onmyoji.comm_FH_YSJHDBSCH)
                    logger.debug("点击今日挑战")
                    image_service.touch(Onmyoji.ghost_JRTZ)
                    logger.debug("判断是否有未挑战")
                    is_select = image_service.exists(Onmyoji.ghost_WXZ)
                    if not is_select:
                        logger.debug("结束地域鬼王")
                        break
            else:
                logger.debug("无未选择，退出地域鬼王")
            logger.debug("返回首页")
            image_service.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH, wait=3)
            image_service.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH, wait=3)
            image_service.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH, wait=3)
        time_end = time.time() - time_start
        logger.info("地域鬼王,用时{}秒", round(time_end))

    @staticmethod
    def friends_manage(game_task: []):
        # 开始时间
        time_start = time.time()
        # 账号信息
        game_account = GameAccount(game_task[2])
        logger.debug(game_account.game_name)
        logger.debug("进入好友界面")
        is_friends = image_service.touch(Onmyoji.friends_HYTB)
        for i_fetter in range(5):
            logger.debug("判断有无好友羁绊提升")
            is_fetter = image_service.exists(Onmyoji.friends_HYJBTS)
            if is_fetter:
                image_service.touch(Onmyoji.comm_FH_YSJHDBSCH)
            else:
                break
        logger.debug("好友友情点收取")
        if is_friends:
            logger.debug("点击好友-右侧好友")
            image_service.touch(Onmyoji.friends_YCHY)
            logger.debug("点击左下好友")
            image_service.touch(Onmyoji.friends_ZXHY)
            logger.debug("点击一键收取")
            is_collect = image_service.exists(Onmyoji.friends_YJSQ, is_click=True)
            if is_collect:
                logger.debug("获得奖励")
                complex_service.get_reward(Onmyoji.friends_HDJL)
            else:
                logger.debug("无一键收取")
        logger.debug("吉闻祝福")
        image_service.touch(Onmyoji.friends_JW)
        logger.debug("一键祝福")
        is_blessing = image_service.exists(Onmyoji.friends_YJZF, is_click=True)
        if is_blessing:
            logger.debug("祝福按钮")
            image_service.touch(Onmyoji.friends_ZFAN)
            logger.debug("获得奖励")
            complex_service.get_reward(Onmyoji.friends_HDJL)
        else:
            logger.debug("无一键祝福")
        logger.debug("返回到好友界面")
        image_service.touch(Onmyoji.comm_FH_YSJZDHBSCH)
        logger.debug("好友添加")
        is_friend_is_full = image_service.exists(Onmyoji.friends_HYYM)
        if not is_friend_is_full:
            logger.debug("好友不满200，进入添加")
            image_service.touch(Onmyoji.friends_YCTJ)
            for i_add in range(20):
                logger.debug("点击添加好友")
                is_add = image_service.touch(Onmyoji.friends_TJHY, cvstrategy=Cvstrategy.default)
                if is_add:
                    logger.debug("申请")
                    image_service.touch(Onmyoji.friends_SQ)
                else:
                    logger.debug("无添加按钮")
                    break
        logger.debug("返回首页")
        image_service.touch(Onmyoji.comm_FH_YSJZDHBSCH)
        time_end = time.time() - time_start
        logger.info("好友管理,用时{}秒", round(time_end))

    @staticmethod
    def friends_fight(game_task: []):
        """
        好友协战
        :param game_task:
        :return:
        """
        impl_friends.friends_fight(game_task)

    @staticmethod
    def foster_care(game_task: []):
        """
        式神寄养
        :param game_task:
        :return:
        """
        impl_house.foster_care(game_task)

    @staticmethod
    def region_border(game_task: []):
        """
        阴阳寮突破
        :param game_task: 任务信息
        :return:
        """
        impl_border.region_border(game_task)

    @staticmethod
    def shack_house(game_task: []):
        """
        阴阳寮管理
        :param game_task: 阴阳寮管理
        :return:
        """
        impl_house.shack_house(game_task)
