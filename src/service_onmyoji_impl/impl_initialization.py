# @Time: 2023年09月01日 18:22
# @Author: orcakill
# @File: impl_initialization.py
# @Description: 当前状态初始化
import os
import time

from src.model.enum import Onmyoji, Cvstrategy
from src.model.models import GameAccount
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.utils.my_logger import logger
from src.utils.utils_time import UtilsTime


def initialization(game_task: [], login_type: int = 0):
    """
    项目1 当前状态初始化
    :param login_type: 登录类型 默认 0 按账号登录 1 快速登录
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
    # 服务器信息
    server = os.path.join(Onmyoji.login_FWQ, game_account.game_region)
    # 账号首页信息
    account_index = os.path.join(Onmyoji.user_SYTX, game_account.id)
    is_index = ImageService.exists(account_index)
    is_explore = ImageService.exists(Onmyoji.home_TS)
    if not is_index or not is_explore:
        logger.debug("不在账号首页")
        # 不在账号首页的其它，重启app，根据账号选择用户、服务器、开始游戏
        logger.debug("启动阴阳师app")
        ImageService.restart_app("com.netease.onmyoji")
        logger.debug("判断是否存在适龄提示")
        is_ageAppropriateReminder = ImageService.exists(Onmyoji.login_SLTS, timeouts=30)
        # 不存在适龄提示
        if not is_ageAppropriateReminder:
            logger.debug("不存在适龄提示")
            for i_ageAppropriateReminder in range(5):
                logger.debug("点击可能存在的重新打开应用")
                ImageService.touch(Onmyoji.login_CXDKYY)
                logger.debug("点击左上角，防止有开场动画")
                ImageService.touch_coordinate((10, 10))
                logger.debug("接受协议")
                ImageService.touch(Onmyoji.login_JSXY, timeouts=1)
                logger.debug("点击公告返回")
                ImageService.touch(Onmyoji.comm_FH_YSJGGCH)
                logger.debug("重新判断适龄提示")
                is_ageAppropriateReminder = ImageService.exists(Onmyoji.login_SLTS)
                if is_ageAppropriateReminder:
                    break
                logger.debug("等待10秒")
                time.sleep(10)
        logger.debug("接受协议")
        ImageService.touch(Onmyoji.login_JSXY, timeouts=1)
        logger.debug("登录账号")
        if login_type == 0:
            logger.debug("判断当前账号选择")
            is_account_select = ImageService.exists(Onmyoji.login_WYYX)
            if not is_account_select:
                logger.debug("用户中心")
                ImageService.touch(Onmyoji.login_YHZX, wait=2)
                logger.debug("切换账号")
                ImageService.touch(Onmyoji.login_QHZH, cvstrategy=Cvstrategy.default, wait=2)
            logger.debug("常用")
            is_used = ImageService.touch(Onmyoji.login_CY, cvstrategy=Cvstrategy.default, wait=2)
            if not is_used:
                logger.debug("用户中心")
                ImageService.exists(Onmyoji.login_YHZX, wait=2, is_click=True)
                logger.debug("再次切换账号")
                ImageService.touch(Onmyoji.login_QHZH, cvstrategy=Cvstrategy.default, wait=2)
                logger.debug("再次点击常用")
                ImageService.touch(Onmyoji.login_CY, cvstrategy=Cvstrategy.default, wait=2)
            logger.debug("选择账号")
            account = os.path.join(Onmyoji.user_XZZH, game_account.account_name)
            ImageService.touch(account, cvstrategy=Cvstrategy.default, wait=4)
            logger.debug("登录")
            ImageService.touch(Onmyoji.login_DLAN, cvstrategy=Cvstrategy.default, wait=4)
            logger.debug("接受协议")
            ImageService.touch(Onmyoji.login_JSXY, wait=3)
            logger.debug("切换服务器")
            ImageService.touch(Onmyoji.login_QHFWQ, cvstrategy=Cvstrategy.default, wait=3)
            logger.debug("点击小三角")
            pos_TCS = ImageService.exists(Onmyoji.login_TYCS, wait=2)
            pos_JSX = ImageService.exists(Onmyoji.login_ZXJS, wait=2)
            if not pos_TCS or not pos_JSX:
                logger.debug("没找到小三角，重新判断是否已点击切换服务器")
                for i_triangle in range(5):
                    logger.debug("点击切换服务器")
                    ImageService.touch(Onmyoji.login_QHFWQ, cvstrategy=Cvstrategy.default, wait=3)
                    logger.debug("判断是否有小三角")
                    pos_TCS = ImageService.exists(Onmyoji.login_TYCS, wait=2)
                    pos_JSX = ImageService.exists(Onmyoji.login_ZXJS, wait=2)
                    if pos_TCS and pos_JSX:
                        break
            if pos_TCS and pos_JSX:
                logger.debug("有小三角")
                ImageService.touch_coordinate((pos_TCS[0], pos_JSX[1]))
            logger.debug("选择服务器:{}", game_account.game_region)
            is_select = ImageService.touch(server, wait=2)
            if not is_select:
                logger.debug("未选择服务器")
            logger.debug("开始游戏")
            is_start = ImageService.touch(Onmyoji.login_KSYX, wait=2)
            if not is_start:
                logger.debug("未开始游戏，点击服务器")
                ImageService.touch(server, wait=2)
                logger.debug("再次点击开始游戏")
                ImageService.touch(Onmyoji.login_KSYX, wait=3)
        else:
            logger.debug("开始游戏")
            ImageService.touch(Onmyoji.login_KSYX, wait=3)
        time.sleep(15)
    logger.debug("{}首页,判断底部菜单", game_account.game_name)
    is_openBottom = ImageService.exists(Onmyoji.home_DBCDDK)
    if not is_openBottom:
        for i_openBottom in range(4):
            logger.debug("当前页面无底部菜单打开")
            logger.debug("点击可能存在的底部菜单")
            ImageService.touch(Onmyoji.home_DBCD, timeouts=3)
            is_openBottom = ImageService.exists(Onmyoji.home_DBCDDK)
            if is_openBottom:
                logger.debug("底部菜单已打开")
                break
            logger.debug("点击可能存在的悬赏封印")
            ComplexService.refuse_reward()
            logger.debug("点击可能存在的右上角返回")
            ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH, timeouts=3)
            logger.debug("点击可能存在的左上角返回")
            ImageService.touch(Onmyoji.comm_FH_ZSJHKZDHSXYH, timeouts=3)
            logger.debug("点击可能存在的下载")
            is_download = ImageService.exists(Onmyoji.home_XZ, timeouts=3)
            if is_download:
                logger.debug("点击不再提示")
                ImageService.touch(Onmyoji.home_BZTS)
                logger.debug("点击下载")
                ImageService.touch(Onmyoji.home_XZ)
            logger.debug("点击可能存在的取消，不打开加成")
            ImageService.touch(Onmyoji.home_QX, timeouts=3)
            logger.debug("点击可能存在的底部菜单")
            ImageService.touch(Onmyoji.home_DBCD, timeouts=3)
            logger.debug("重新判断是否存在底部菜单打开")
            is_openBottom = ImageService.exists(Onmyoji.home_DBCDDK)
            if is_openBottom:
                logger.debug("底部菜单已打开")
                break
    logger.debug("重新判断是否在账号首页")
    is_index = ImageService.exists(account_index)
    # 结束时间
    time_end = time.time()
    # 总用时
    time_all = time_end - time_start
    if is_index:
        logger.debug("初始化当前状态完成:{}，用时{}", game_account.game_name, UtilsTime.convert_seconds(time_all))
        return True
    else:
        logger.debug("初始化当前状态失败:{}，用时{}", game_account.game_name, UtilsTime.convert_seconds(time_all))
        return False


def return_home(game_task: []):
    game_account = GameAccount(game_task[2])
    # 判断是否是待登录账号首页
    logger.debug("返回首页-判断当前状态")
    # 当前状态 账号首页 1，2,3，4，5
    #        其它，不在账号首页
    account_index = os.path.join(Onmyoji.user_SYTX, game_account.id)
    is_index = ImageService.exists(account_index, timeouts=1)
    is_explore = ImageService.exists(Onmyoji.home_TS, timeouts=1)
    if not is_index or not is_explore:
        logger.debug("不在账号首页，重新快速登录")
        initialization(game_task, 1)
    else:
        logger.debug("有探索，有账号，在首页")
        return True
    return False
