# @Time: 2023年09月01日 18:22
# @Author: orcakill
# @File: impl_initialization.py
# @Description: 当前状态初始化
import os
import time

from src.dao.mapper import Mapper
from src.dao.mapper_extend import MapperExtend
from src.model.enum import Onmyoji, Cvstrategy
from src.model.models import GameAccount, GameProject, GameProjectLog, GameDevice, GameProjectsRelation
from src.service.airtest_service import AirtestService
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.utils.my_logger import logger
from src.utils.utils_mail import UtilsMail
from src.utils.utils_time import UtilsTime


def initialization(game_task: [], login_type: int = 0):
    """
    项目1 当前状态初始化
    :param device_name: 设备信息
    :param login_type: 登录类型 默认 0 按账号登录 1 快速登录
    :param game_task: 任务信息
    :return:
    """
    # 开始时间
    time_start = time.time()
    # 项目信息
    (game_projects_relation, game_account, game_devices) = (
        GameProjectsRelation(game_task[1]), GameAccount(game_task[2]), GameDevice(game_task[4]))
    # 登录，每次重置项目信息为登录
    game_project = GameProject(MapperExtend.select_game_project("", "1")[0])
    # 服务器信息
    server = str(os.path.join(Onmyoji.login_FWQ, game_account.role_region))
    # 账号首页信息
    account_index = str(os.path.join(Onmyoji.user_SYTX, str(game_account.account_num)))
    # 重新登录
    str_login = ''
    # 判断是否是待登录账号首页
    logger.debug("初始化-判断当前状态")
    # 当前状态 账号首页 1，2,3，4
    #        其它，不在账号首页
    logger.debug("首页账号")
    is_index = ImageService.exists(account_index)
    logger.debug("首页探索")
    is_explore = ImageService.exists(Onmyoji.home_TS, rgb=True)
    logger.debug("首页町中")
    is_courtyard = ImageService.exists(Onmyoji.home_DZ)
    if not is_index or not is_explore or not is_courtyard:
        logger.debug("不在账号首页")
        str_login = '重新登录'
        # 不在账号首页的其它，重启app，根据账号选择用户、服务器、开始游戏
        logger.debug("启动阴阳师app")
        ImageService.restart_app("com.netease.onmyoji")
        logger.debug("判断是否存在适龄提示")
        is_age_appropriate_reminder = ImageService.exists(Onmyoji.login_SLTS, timeouts=30)
        # 不存在适龄提示
        if not is_age_appropriate_reminder:
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
                is_age_appropriate_reminder = ImageService.exists(Onmyoji.login_SLTS)
                if is_age_appropriate_reminder:
                    break
                logger.debug("等待10秒")
                time.sleep(10)
        logger.debug("登录账号")
        if login_type == 0:
            for i_account in range(5):
                logger.debug("第{}次切换账号", i_account + 1)

                logger.debug("点击可能存在的登录")
                ImageService.touch(Onmyoji.login_DLAN, wait=3, rgb=True)
                logger.debug("检查可能存在的其他账号登录")
                is_exception = ImageService.exists(Onmyoji.login_YCDL)
                if is_exception:
                    logger.debug("点击异常登录界面的退出")
                    ImageService.touch(Onmyoji.comm_FH_YSJBDHSCH)
                logger.debug("点击可能存在选服指引")
                ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH)
                logger.debug("点击可能存在选择区域")
                ComplexService.get_reward(Onmyoji.login_XZQY)
                logger.debug("点击可能存在同意并登录")
                ImageService.exists(Onmyoji.login_TYBDL)
                logger.debug("点击可能存在的右上角白底黑色叉号")
                ImageService.exists(Onmyoji.comm_FH_YSJBDHSCH)
                logger.debug("用户中心")
                is_YHZX = ImageService.touch(Onmyoji.login_YHZX, wait=2)
                if not is_YHZX:
                    logger.debug("未识别用户中心，启用ocr识别点击用户中心")
                    for i_switch in range(3):
                        logger.debug("第{}次识别用户中心", i_switch + 1)
                        is_switch = ImageService.ocr_touch(
                            ["用户中心"])
                        if is_switch:
                            break
                logger.debug("切换账号")
                ImageService.touch(Onmyoji.login_QHZH, cvstrategy=Cvstrategy.default, wait=2)
                logger.debug("常用")
                ImageService.touch(Onmyoji.login_CY, cvstrategy=Cvstrategy.default, wait=2)
                logger.debug("选择账号")
                account = str(os.path.join(Onmyoji.user_XZZH, game_account.account_name))
                is_account = ImageService.touch(account, wait=4)
                logger.debug("登录")
                ImageService.touch(Onmyoji.login_DLAN, wait=4, rgb=True)
                logger.debug("接受协议")
                ImageService.touch(Onmyoji.login_JSXY, wait=3)
                logger.debug("点击切换")
                is_switch = ImageService.touch(Onmyoji.login_QHFWQ)
                if not is_switch:
                    logger.debug("未识别切换，启用ocr识别点击切换")
                    for i_switch in range(3):
                        logger.debug("第{}次识别切换", i_switch + 1)
                        is_switch = ImageService.ocr_touch(
                            ["切换", "缥缈之旅", "相伴相随", "桃映春馨", "两情相悦", "遥远之忆", "抢先体验服"])
                        if is_switch:
                            break
                logger.debug("点击小三角,获 取特邀测试和注销角色坐标")
                pos_tcs = ImageService.exists(Onmyoji.login_TYCS, wait=2)
                pos_jsx = ImageService.exists(Onmyoji.login_ZXJS, wait=2)
                if pos_tcs and pos_jsx:
                    logger.debug("有小三角")
                    ImageService.touch_coordinate((pos_tcs[0], pos_jsx[1]))
                else:
                    logger.debug("特邀测试{}，注销角色{}", pos_tcs, pos_jsx)
                logger.debug("选择服务器:{}", game_account.role_region)
                is_server = ImageService.touch(server, wait=2)
                logger.debug("账号选择：{},服务器选择：{}", is_account, is_server)
                if is_account and is_server:
                    logger.debug("开始游戏")
                    is_login = ImageService.touch(Onmyoji.login_KSYX, wait=2)
                    if is_login:
                        break
                if i_account + 1 == 5:
                    send_screenshot = AirtestService.snapshot()
                    send_text = "账号：" + game_account.account_name + "\n\r账号选择：" + str(
                        is_account) + "\n\r服务器选择：" + str(is_server)
                    logger.debug("第五次尝试登录失败,邮件发送")
                    UtilsMail.send_email("阴阳师脚本", "登录失败5次", send_text, [send_screenshot])
        else:
            logger.debug("开始游戏")
            ImageService.touch(Onmyoji.login_KSYX, wait=5)
        time.sleep(15)
    logger.debug("{}首页,判断底部菜单", game_account.role_name)
    is_open_bottom = ImageService.exists(Onmyoji.home_DBCDDK)
    if not is_open_bottom:
        for i_openBottom in range(4):
            logger.debug("当前页面无底部菜单打开")
            logger.debug("点击可能存在的底部菜单")
            ImageService.touch(Onmyoji.home_DBCD, timeouts=3)
            is_open_bottom = ImageService.exists(Onmyoji.home_DBCDDK)
            if is_open_bottom:
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
            is_open_bottom = ImageService.exists(Onmyoji.home_DBCDDK)
            if is_open_bottom:
                logger.debug("底部菜单已打开")
                break
    time.sleep(5)
    logger.debug("重新判断是否在账号首页")
    is_index = ImageService.exists(account_index)
    # 结束时间
    time_end = time.time()
    # 总用时
    time_all = time_end - time_start
    if time_all >= 60 * 5:
        logger.info("当前状态初始化，用时超5分钟，实际用时{}", UtilsTime.convert_seconds(time_all))
        # 超5分钟，判定为初始化失败，云手机重启设备，重新授权ADB，
    # 记录项目执行结果
    game_project_log = GameProjectLog(project_id=game_project.id, account_id=game_account.id, device_id=game_devices.id,
                                      result='当前状态初始化', cost_time=int(time_all))
    if str_login != '':
        game_project_log.result = game_project_log.result + "," + str_login
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
    account_index = str(os.path.join(Onmyoji.user_SYTX, str(game_account.account_num)))
    is_index = ImageService.exists(account_index)
    logger.debug("返回首页-检查探索")
    is_explore = ImageService.exists(Onmyoji.home_TS)
    logger.debug("返回首页-检查町中")
    is_courtyard = ImageService.exists(Onmyoji.home_DZ)
    if not is_index or not is_explore or not is_courtyard:
        if not is_index:
            logger.debug("首页账号{}未识别成功", account_index)
        if not is_explore:
            logger.debug("首页探索{}未识别成功", Onmyoji.home_TS)
        if not is_courtyard:
            logger.debug("首页町中{}未识别成功", Onmyoji.home_DZ)
        ImageService.snapshot(game_account.role_name + '_' + game_project.project_name + "_非首页", True)
        logger.info("不在账号首页，重新快速登录 {}:{}", game_account.role_name, game_project.project_name)
        initialization(game_task, 1)
    else:
        logger.debug("有探索，有账号，在首页")
        return True
    return False
