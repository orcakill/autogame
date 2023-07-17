# @Time    : 2023年05月31日 17:51
# @Author  : orcakill
# @File    : onmyoji_service.py
# @Description : 服务接口
import os
import time

from src.model.enum import Onmyoji, Cvstrategy
from src.model.models import GameAccount, GameProjectsRelation, GameProject
from src.service.airtest_service import AirtestService
from src.service.image_service import ImageService
from src.utils.junk.my_logging import logger

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
            image_service.touch(Onmyoji.login_CY,interval=1)
            logger.debug("选择账号")
            account = os.path.join(Onmyoji.user_XZZH, game_account.id)
            image_service.touch(account,interval=1)
            logger.debug("登录")
            image_service.touch(Onmyoji.login_DLAN,interval=1)
            logger.debug("切换服务器")
            image_service.touch(Onmyoji.login_QHFWQ, cvstrategy=Cvstrategy.default)
            logger.debug("点击小三角")
            image_service.touch(Onmyoji.login_XSJ, cvstrategy=Cvstrategy.default)
            logger.debug("选择服务器:{}", game_account.game_region)
            server = os.path.join(Onmyoji.login_FWQ, game_account.game_region)
            image_service.touch(server)
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
        game_account = GameAccount(game_task['GameAccount'])
        game_projects_relation = GameProjectsRelation(game_task['GameProjectsRelation'])
        game_project = GameProject(game_task['GameProject'])
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
            is_soul_one = image_service.exists(Onmyoji.soul_HONE)
            if is_soul_one is None:
                logger.debug("当前无魂一")
                # 获取层字的横坐标，向上滑动3次
                layer_coordinates = image_service.exists_coordinate(Onmyoji.soul_CZ)
                airtest_service.swipe(layer_coordinates[0], 1 / 2 * layer_coordinates[1])
                airtest_service.swipe(layer_coordinates[0], 1 / 2 * layer_coordinates[1])
                airtest_service.swipe(layer_coordinates[0], 1 / 2 * layer_coordinates[1])
        if game_project.project_name in ["魂十", "魂十一"]:
            logger.debug(game_project.project_name)
            is_soul_one = image_service.exists(Onmyoji.soul_HELEVEN)
            if is_soul_one is None:
                logger.debug("当前无{}", game_project.project_name)
                # 获取层字的横坐标，向下滑动3次
                layer_coordinates = image_service.exists_coordinate(Onmyoji.soul_CZ)
                airtest_service.swipe(layer_coordinates[0], 2 * layer_coordinates[1])
                airtest_service.swipe(layer_coordinates[0], 2 * layer_coordinates[1])
                airtest_service.swipe(layer_coordinates[0], 2 * layer_coordinates[1])
        logger.debug("准备完成，开始御魂挑战循环")
        project_start_time = time.time()
        for i in range(1, game_projects_relation.project_num):
            start_time = time.time()
            logger.debug("第{}次{}挑战", i, game_project.project_name)
            image_service.touch(Onmyoji.soul_TZ)
            logger.debug("退出挑战-角色头像、宝箱、失败")
            time.sleep(15)
            for j in (1, 30):
                logger.debug("第{}次识别", j)
                image_service.touch(Onmyoji.soul_JSTX, timeout=1)
                is_win = image_service.touch(Onmyoji.soul_TCTZ)
                if not is_win:
                    image_service.touch(Onmyoji.soul_ZDSB)
            end_time = time.time()
            logger.debug("本次{}战斗结束，用时{}秒", game_project.project_name, end_time - start_time)
        project_end_time = time.time()
        logger.debug("本轮{}战斗结束，总用时{}秒，平均用时{}秒", game_project.project_name,
                     project_end_time - project_start_time,
                     (project_end_time - project_start_time) / game_projects_relation.project_num)
        if game_account.account_class == 0:
            logger.debug("关闭加成")
        logger.debug("返回首页")
        image_service.touch(Onmyoji.comm_FH_LSYXBSXYH)
        image_service.touch(Onmyoji.comm_FH_LSYXBSXYH)
