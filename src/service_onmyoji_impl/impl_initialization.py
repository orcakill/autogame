# @Time: 2023年09月01日 18:22
# @Author: orcakill
# @File: impl_initialization.py
# @Description: 当前状态初始化
import os
import time

from src.dao.mapper import Mapper
from src.model.enum import Onmyoji, Cvstrategy
from src.model.models import GameAccount, GameProject, GameProjectLog, GameDevices, GameProjectsRelation
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
    # 首页
    is_index = False
    # 探索
    is_explore = False
    # 项目信息
    (game_projects_relation, game_account,
     game_project, game_devices) = (GameProjectsRelation(game_task[1]), GameAccount(game_task[2]),
                                    GameProject(game_task[3]), GameDevices(game_task[4]))
    # 服务器信息
    server = os.path.join(Onmyoji.login_FWQ, game_account.role_region)
    # 账号首页信息
    account_index = os.path.join(Onmyoji.user_SYTX, game_account.id)
    # 判断是否是待登录账号首页
    logger.debug("初始化-判断当前状态")
    # 当前状态 账号首页 1，2,3，4
    #        其它，不在账号首页
    logger.debug("排除悬赏")
    ComplexService.refuse_reward()
    logger.debug("排除缓存过多")
    ComplexService.refuse_cache()
    logger.debug("检查失联掉线")
    is_loss = ComplexService.loss_connection()
    if is_loss:
        logger.debug("重新登录")
    else:
        logger.debug("首页账号")
        is_index = ImageService.exists(account_index)
        logger.debug("首页探索")
        is_explore = ImageService.exists(Onmyoji.home_TS)
    if not is_index or not is_explore and is_loss:
        # sys.exit()
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
                logger.debug("接受协议")
                ImageService.touch(Onmyoji.login_JSXY, timeouts=1)
                logger.debug("重新判断适龄提示")
                is_ageAppropriateReminder = ImageService.exists(Onmyoji.login_SLTS)
                if is_ageAppropriateReminder:
                    break
                logger.debug("等待10秒")
                time.sleep(10)
        logger.debug("登录账号")
        if login_type == 0:
            for i_account in range(5):
                logger.debug("第{}次切换账号", i_account + 1)
                logger.debug("点击可能存在的登录")
                ImageService.touch(Onmyoji.login_DLAN, cvstrategy=Cvstrategy.default, wait=3)
                logger.debug("点击可能存在选择区域")
                ComplexService.get_reward(Onmyoji.login_XZQY)
                logger.debug("用户中心")
                ImageService.touch(Onmyoji.login_YHZX, wait=2)
                logger.debug("切换账号")
                ImageService.touch(Onmyoji.login_QHZH, cvstrategy=Cvstrategy.default, wait=2)
                logger.debug("常用")
                ImageService.touch(Onmyoji.login_CY, cvstrategy=Cvstrategy.default, wait=2)
                logger.debug("选择账号")
                account = os.path.join(Onmyoji.user_XZZH, game_account.account_name)
                is_account = ImageService.touch(account, wait=4)
                logger.debug("登录")
                ImageService.touch(Onmyoji.login_DLAN, cvstrategy=Cvstrategy.default, wait=4)
                logger.debug("接受协议")
                ImageService.touch(Onmyoji.login_JSXY, wait=3)
                logger.debug("切换服务器")
                ImageService.touch(Onmyoji.login_QHFWQ, cvstrategy=Cvstrategy.default, wait=3)
                logger.debug("点击小三角,获 取特邀测试和注销角色坐标")
                pos_TCS = ImageService.exists(Onmyoji.login_TYCS, wait=2)
                pos_JSX = ImageService.exists(Onmyoji.login_ZXJS, wait=2)
                if pos_TCS and pos_JSX:
                    logger.debug("有小三角")
                    ImageService.touch_coordinate((pos_TCS[0], pos_JSX[1]))
                logger.debug("选择服务器:{}", game_account.role_region)
                is_server = ImageService.touch(server, wait=2)
                logger.debug("账号选择：{},服务器选择：{}", is_account, is_server)
                if is_account and is_server:
                    logger.debug("开始游戏")
                    is_login = ImageService.touch(Onmyoji.login_KSYX, wait=2)
                    if is_login:
                        break
        else:
            logger.debug("开始游戏")
            ImageService.touch(Onmyoji.login_KSYX, wait=5)
        time.sleep(15)
    logger.debug("{}首页,判断底部菜单", game_account.role_name)
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
            logger.debug("开始游戏")
            ImageService.touch(Onmyoji.login_KSYX, wait=3)
            logger.debug("点击可能存在的悬赏封印")
            ComplexService.refuse_reward()
            logger.debug("点击可能存在的右上角返回")
            ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH, timeouts=3)
            logger.debug("点击可能存在的左上角返回")
            ImageService.touch(Onmyoji.comm_FH_ZSJHKZDHSXYH, timeouts=3)
            logger.debug("检查下载")
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
    time.sleep(5)
    logger.debug("重新判断是否在账号首页")
    is_index = ImageService.exists(account_index)
    # 结束时间
    time_end = time.time()
    # 总用时
    time_all = time_end - time_start
    # 记录项目执行结果
    game_project_log = GameProjectLog(project_id=game_project.id, role_id=game_account.id, devices_id=game_devices.id,
                                      result='当前状态初始化', cost_time=int(time_all))
    if login_type == 1:
        game_project_log.result = game_project_log.result + ",快速登录"
    if is_index:
        game_project_log.result = game_project_log.result + ",成功"
        logger.debug("初始化当前状态成功:{}，用时{}", game_account.role_name, UtilsTime.convert_seconds(time_all))
        Mapper.save_game_project_log(game_project_log)
        return True
    else:
        game_project_log.result = game_project_log.result + ",失败"
        Mapper.save_game_project_log(game_project_log)
        logger.debug("初始化当前状态失败:{}，用时{}", game_account.role_name, UtilsTime.convert_seconds(time_all))
        return False


def return_home(game_task: []):
    game_account = GameAccount(game_task[2])

    game_project = GameProject(game_task[3])
    # 判断是否是待登录账号首页
    logger.debug("返回首页-拒接协战")
    # 当前状态 账号首页 1，2,3，4，5
    #        其它，不在账号首页
    ComplexService.refuse_reward()
    logger.debug("返回首页-检查首页账号")
    account_index = os.path.join(Onmyoji.user_SYTX, game_account.id)
    is_index = ImageService.exists(account_index)
    logger.debug("返回首页-检查探索")
    is_explore = ImageService.exists(Onmyoji.home_TS)
    if not is_index or not is_explore:
        ImageService.snapshot("不在首页", True)
        logger.info("不在账号首页，重新快速登录 {}:{}", game_account.role_name, game_project.project_name)
        initialization(game_task, 1)
    else:
        logger.debug("有探索，有账号，在首页")
        return True
    return False
