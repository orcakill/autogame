# @Time: 2023年05月31日 17:51
# @Author: orcakill
# @File: onmyoji_service.py
# @Description: 服务接口
import os
import time

from src.model.enum import Onmyoji, Cvstrategy
from src.model.models import GameAccount, GameProjectsRelation, GameProject
from src.service.airtest_service import AirtestService
from src.service.image_service import ImageService
from src.utils.my_logger import logger

# airtest服务接口
airtest_service = AirtestService()
image_service = ImageService()


class OnmyojiService:

    @staticmethod
    def initialization(game_account: GameAccount):
        """
        当前状态初始化
        :param game_account: 用户信息
        :return:
        """
        # 判断是否是待登录账号首页
        logger.debug("判断当前状态")
        # 当前状态 账号首页 1，2,3，4
        #        其它，不在账号首页
        account_index = os.path.join(Onmyoji.user_SYTX, game_account.id)
        is_index = image_service.exists(account_index)
        if not is_index:
            logger.debug("不在账号首页")
            # 不在账号首页的其它，重启app，根据账号选择用户、服务器、开始游戏
            logger.debug("启动阴阳师app")
            airtest_service.restart_app("com.netease.onmyoji")
            logger.debug("等待20秒")
            time.sleep(20)
            logger.debug("判断是否存在适龄提示")
            is_ageAppropriateReminder = image_service.exists(Onmyoji.login_SLTS, timeout=5)
            # 不存在适龄提示
            if not is_ageAppropriateReminder:
                logger.debug("不存在适龄提示")
                for i_ageAppropriateReminder in range(5):
                    logger.debug("点击左上角，防止有开场动画")
                    airtest_service.touch_coordinate([10, 10])
                    logger.debug("点击公告返回")
                    image_service.touch(Onmyoji.login_FH)
                    logger.debug("重新判断适龄提示")
                    is_ageAppropriateReminder = image_service.exists(Onmyoji.login_SLTS)
                    if is_ageAppropriateReminder:
                        break
                    logger.debug("等待10秒")
                    time.sleep(10)
            logger.debug("登录账号")
            logger.debug("判断当前账号选择")
            is_account_select = image_service.exists(Onmyoji.login_WYYX)
            if not is_account_select:
                logger.debug("用户中心")
                image_service.touch(Onmyoji.login_YHZX)
                logger.debug("切换账号")
                image_service.touch(Onmyoji.login_QHZH)
            logger.debug("常用")
            image_service.touch(Onmyoji.login_CY, interval=1)
            logger.debug("选择账号")
            account = os.path.join(Onmyoji.user_XZZH, game_account.id)
            image_service.touch(account, interval=1)
            logger.debug("登录")
            image_service.touch(Onmyoji.login_DLAN, interval=1)
            logger.debug("切换服务器")
            image_service.touch(Onmyoji.login_QHFWQ, cvstrategy=Cvstrategy.default, interval=1)
            logger.debug("点击小三角")
            image_service.touch(Onmyoji.login_XSJ, cvstrategy=Cvstrategy.default, interval=1)
            logger.debug("选择服务器:{}", game_account.game_region)
            server = os.path.join(Onmyoji.login_FWQ, game_account.game_region)
            image_service.touch(server, interval=1)
            logger.debug("开始游戏")
            image_service.touch(Onmyoji.login_KSYX)
            time.sleep(15)
        logger.debug("当前账号首页,判断底部菜单")
        is_openBottom = image_service.exists(Onmyoji.home_DBCDDK)
        if not is_openBottom:
            for i_openBottom in range(4):
                logger.debug("当前页面无底部菜单打开")
                logger.debug("点击可能存在的右上角返回")
                image_service.touch(Onmyoji.comm_FH_SYHDBSCH, timeout=3)
                logger.debug("点击可能存在的下载")
                image_service.touch(Onmyoji.home_XZ, timeout=3)
                logger.debug("点击可能存在的底部菜单")
                image_service.touch(Onmyoji.home_DBCD, timeout=3)
                logger.debug("重新判断是否存在底部菜单打开")
                is_openBottom = image_service.exists(Onmyoji.home_DBCDDK)
                if is_openBottom:
                    logger.debug("底部菜单已打开")
                    break
        logger.info("初始化当前状态完成")

    @staticmethod
    def soul_fight(game_task: []):
        """
        御魂战斗  魂一、魂八、魂十、魂十一
        大号   魂十一   开启加成
        小号   魂十    开启加成
        协战号 魂一    不开加成
        :param game_task: 项目组信息
        :return:
        """
        game_projects_relation = GameProjectsRelation(game_task[1])
        game_account = GameAccount(game_task[2])
        game_project = GameProject(game_task[3])
        logger.debug("进入探索")
        image_service.touch(Onmyoji.home_TS)
        logger.debug("进入御魂")
        image_service.touch(Onmyoji.soul_YHTB)
        logger.debug("进入八岐大蛇")
        image_service.touch(Onmyoji.soul_BQXZ)
        if game_account.account_class == 0:
            logger.debug("开启加成")
        logger.debug("选择层数")
        if game_project.project_name == "魂一":
            logger.debug("魂一")
            is_soul = image_service.exists(Onmyoji.soul_HONE)
            if not is_soul:
                logger.debug("循环3次")
                for i_soul in range(3):
                    logger.debug("当前无{}，向上滑动三次", game_project.project_name)
                    # 获取层字的横坐标，向上滑动3次
                    layer_coordinates = image_service.exists_coordinate(Onmyoji.soul_CZ, cvstrategy=Cvstrategy.default)
                    if layer_coordinates:
                        xy1 = (layer_coordinates[0], layer_coordinates[1])
                        xy2 = (layer_coordinates[0], 2 * layer_coordinates[1])
                        airtest_service.swipe(xy1, xy2)
                        airtest_service.swipe(xy1, xy2)
                        airtest_service.swipe(xy1, xy2)
                        is_soul = image_service.exists(Onmyoji.soul_HONE)
                        if is_soul:
                            break
                logger.debug("结束循环")
                image_service.touch(Onmyoji.soul_HONE)
        if game_project.project_name in ["魂十", "魂十一"]:
            logger.debug(game_project.project_name)
            is_soul = image_service.exists(Onmyoji.soul_HTEN)
            if not is_soul:
                logger.debug("循环3次")
                for i_soul in range(3):
                    logger.debug("当前无{}，向下滑动三次", game_project.project_name)
                    # 获取层字的横坐标，向下滑动3次
                    layer_coordinates = image_service.exists_coordinate(Onmyoji.soul_CZ, cvstrategy=Cvstrategy.default)
                    if layer_coordinates:
                        xy1 = (layer_coordinates[0], layer_coordinates[1])
                        xy2 = (layer_coordinates[0], 1 / 4 * layer_coordinates[1])
                        airtest_service.swipe(xy1, xy2)
                        airtest_service.swipe(xy1, xy2)
                        airtest_service.swipe(xy1, xy2)
                        is_soul = image_service.exists(Onmyoji.soul_HTEN)
                        if is_soul:
                            break
                logger.debug("结束循环")
                if game_project.project_name == "魂十":
                    image_service.touch(Onmyoji.soul_HTEN)
                if game_project.project_name == "魂十一":
                    image_service.touch(Onmyoji.soul_HELEVEN)
        logger.debug("准备完成，开始御魂挑战循环{}次", game_projects_relation.project_num)
        project_start_time = time.time()
        for i in range(game_projects_relation.project_num):
            start_time = time.time()
            logger.debug("第{}次{}挑战", i + 1, game_project.project_name)
            image_service.touch(Onmyoji.soul_TZ)
            logger.debug("退出挑战-角色头像、宝箱、失败")
            if i == 0:
                time.sleep(2)
                logger.debug("第一次战斗，判断是否需要喂食")
                is_food = image_service.touch(Onmyoji.soul_WSXSJ)
                if is_food:
                    logger.debug("喂食")
                    image_service.touch(Onmyoji.soul_WS)
            time.sleep(15)
            # 循环30次
            for j in range(30):
                logger.debug("御魂战斗第{}次识别", j + 1)
                # 如果是大号，走角色头像大号，小号则走角色头像小号
                if game_account.account_class == 0:
                    logger.debug("御魂战斗-点击角色头像大号")
                    image_service.touch(Onmyoji.soul_JSTXDH, timeout=1)
                else:
                    logger.debug("御魂战斗-点击角色头像小号")
                    image_service.touch(Onmyoji.soul_JSTXXH, timeout=1)
                logger.debug("御魂战斗-判断退出挑战")
                is_win = image_service.exists_coordinate(Onmyoji.soul_TCTZ, timeout=5)
                if is_win:
                    time.sleep(1)
                    airtest_service.touch_coordinate(is_win)
                    logger.debug("御魂战斗-战斗胜利")
                    break
                else:
                    image_service.touch(Onmyoji.soul_ZDSB)
                time.sleep(1)
            end_time = time.time()
            logger.debug("本次{}战斗结束，用时{}秒", game_project.project_name, end_time - start_time)
        project_end_time = time.time()
        logger.debug("本轮{}战斗结束，总用时{}秒，平均用时{}秒", game_project.project_name,
                     round(project_end_time - project_start_time, 3),
                     round((project_end_time - project_start_time) / game_projects_relation.project_num), 3)
        if game_account.account_class == 0:
            logger.debug("关闭加成")
        logger.debug("返回首页")
        image_service.touch(Onmyoji.comm_FH_LSYXBSXYH)
        image_service.touch(Onmyoji.comm_FH_LSYXBSXYH)

    @staticmethod
    def border_fight(game_task: []):
        """
        结界突破 border
        :param game_task: 项目信息
        :return:
        """
        game_account = GameAccount(game_task[2])
        logger.debug("进入探索")
        image_service.touch(Onmyoji.home_TS)
        logger.debug("进入结界突破")
        image_service.touch(Onmyoji.border_JJTPTB)
        logger.debug("判断是存在结界")
        is_border = image_service.exists(Onmyoji.border_GRJJ)
        if not is_border:
            logger.debug("不存在个人结界，有意外情况")
            for i_border in range(3):
                logger.debug("点击呱太入侵")
                image_service.touch(Onmyoji.border_GTRQ, timeout=5)
                logger.debug("点击退出挑战")
                image_service.touch(Onmyoji.border_TCTZ, timeout=5)
                is_border = image_service.exists(Onmyoji.border_GRJJ)
                if is_border:
                    break
        logger.debug("判断是否存在结界突破劵0/30")
        is_securities = image_service.exists(Onmyoji.border_WJJTZJ)
        # 当前战斗次数计数
        num_fight = 0
        # 当前退级次数
        num_retirement = 0
        #  战斗等待时间
        num_wait = 10
        time_start_border = time.time()
        time_fight_list = []
        while is_border and not is_securities:
            logger.debug("结界循环挑战")
            logger.debug("点击个人结界")
            image_service.touch(Onmyoji.border_GRJJ)
            logger.debug("点击进攻")
            image_service.touch(Onmyoji.border_JG)
            time_fight_start = time.time()
            time.sleep(num_wait)
            if num_fight % 9 == 0 and num_retirement < 9:
                logger.debug("当前每9次战斗，退级次数小于9")
                logger.debug("点击返回")
                logger.debug("确定退出")
                num_retirement = num_retirement + 1
            else:
                time.sleep(2)
                logger.debug("点击准备")
                image_service.touch(Onmyoji.border_ZB, timeout=5)
                num_retirement = 0
                logger.debug("不退级，等待战斗结束")
                # 循环30次
                for j in range(30):
                    logger.debug("结界突破战斗第{}次识别", j + 1)
                    # 如果是大号，走角色头像大号，小号则走角色头像小号
                    if game_account.account_class == 0:
                        logger.debug("点击结界突破-角色头像大号")
                        image_service.touch(Onmyoji.border_JSTXDH, timeout=1)
                    else:
                        logger.debug("点击结界突破-角色头像小号")
                        image_service.touch(Onmyoji.border_JSTXXH, timeout=1)
                    logger.debug("判断结界突破-退出挑战")
                    is_win = image_service.exists_coordinate(Onmyoji.border_TCTZ, timeout=5)
                    if is_win:
                        time.sleep(1)
                        airtest_service.touch_coordinate(is_win)
                        logger.debug("结界突破-战斗胜利")
                        break
                    else:
                        image_service.touch(Onmyoji.soul_ZDSB)
                    time.sleep(1)
                time_fight_end = time.time()
                time_fight = time_fight_end - time_fight_start
                logger.debug("本次结界突破战斗结束，用时{}秒", time_fight)
                time_fight_list.append(time_fight)
                # 重新赋值等待时间
                num_wait = time_fight_end - time_fight_start
            # 重新判断是否存在个人结界
            is_border = image_service.exists(Onmyoji.border_GRJJ)
            # 重新判断是否存在无结界挑战劵
            is_securities = image_service.exists(Onmyoji.border_WJJTZJ)
        logger.debug("返回首页")
        time_end_border = time.time()
        logger.debug("本轮结界突破战斗结束，总用时{}秒，战斗总用时{}秒,平均用时{}秒",
                     round(time_end_border - time_start_border, 3),
                     sum(time_fight_list),
                     sum(time_fight_list) / len(time_fight_list)
                     )
