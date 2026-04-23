# @Time: 2023年09月01日 18:22
# @Author: orcakill
# @File: impl_initialization.py
# @Description: 当前状态初始化
import os
import time

from src.dao.mapper import Mapper
from src.dao.mapper_extend import MapperExtend
from src.model.enum import Onmyoji, Cvstrategy, Switch
from src.model.models import GameAccount, GameProject, GameProjectLog, GameDevice, GameProjectsRelation
from src.service.airtest_service import AirtestService
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.utils.my_logger import logger
from src.utils.utils_mail import UtilsMail
from src.utils.utils_time import UtilsTime


def initialization(game_task: list, login_type: int = 0):
    """
    项目1 当前状态初始化
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

    # 判断是否在账号首页
    if not is_on_account_homepage(account_index):
        str_login = '重新登录'
        # 重启app并处理登录流程
        if not restart_app_and_login(game_account, server, login_type):
            # 登录失败处理
            game_project_log = create_project_log(game_project, game_account, game_devices, time_start,
                                                  f"当前状态初始化,{str_login},失败")
            Mapper.save_game_project_log(game_project_log)
            return False

    # 处理底部菜单
    if not ensure_bottom_menu_open():
        # 底部菜单处理失败
        game_project_log = create_project_log(game_project, game_account, game_devices, time_start,
                                              f"当前状态初始化,{str_login},失败")
        Mapper.save_game_project_log(game_project_log)
        return False

    # 验证是否在账号首页
    is_index = ImageService.exists(account_index)
    time_end = time.time()
    time_all = time_end - time_start

    # 记录执行结果
    result = f"当前状态初始化,{str_login}"
    if login_type == 1:
        result += ",快速登录"
    if is_index:
        result += ",成功"
        logger.info("初始化当前状态成功:{}，用时{}", game_account.role_name, UtilsTime.convert_seconds(time_all))
    else:
        result += ",失败"
        logger.info("初始化当前状态失败:{}，用时{}", game_account.role_name, UtilsTime.convert_seconds(time_all))

    game_project_log = create_project_log(game_project, game_account, game_devices, time_start, result)
    Mapper.save_game_project_log(game_project_log)
    return is_index


def is_on_account_homepage(account_index):
    """检查是否在账号首页"""
    logger.debug("初始化-判断当前状态")
    is_index = ImageService.exists(account_index)
    is_explore = ImageService.exists(Onmyoji.home_TS, rgb=True)
    is_courtyard = ImageService.exists(Onmyoji.home_DZ)
    return is_index and is_explore and is_courtyard


def restart_app_and_login(game_account, server, login_type):
    """重启应用并登录"""
    logger.debug("启动阴阳师app")
    ImageService.restart_app("com.netease.onmyoji")

    # 处理适龄提示
    handle_age_verification()

    # 根据登录类型处理登录
    if login_type == 0:
        return login_with_account(game_account, server)
    else:
        return quick_login()


def handle_age_verification():
    """处理适龄提示"""
    logger.debug("判断是否存在适龄提示")
    is_age_appropriate_reminder = ImageService.exists(Onmyoji.login_SLTS, timeouts=30)

    # 不存在适龄提示，尝试处理其他弹窗
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


def login_with_account(game_account, server):
    """使用账号登录"""
    # 账号登录信息
    account_login = str(os.path.join(Onmyoji.user_DLTX, str(game_account.account_num)))

    # 步骤执行状态记录
    step_status = {}
    failure_screenshots = []

    def log_step(step_name, status):
        """记录步骤执行状态"""
        status_symbol = "✓" if status else "✗"
        logger.info(f"[{status_symbol}] {step_name}: {status}")
        step_status[step_name] = status
        return status

    def analyze_login_failure(step_status):
        """分析登录失败的主要原因"""
        failure_reasons = []

        if not step_status.get("点击用户中心", False):
            failure_reasons.append("无法进入用户中心")

        if not step_status.get("切换账号", False):
            failure_reasons.append("无法切换账号")

        if not step_status.get("选择具体账号", False):
            failure_reasons.append("无法选择账号")

        if not step_status.get("选择服务器", False):
            failure_reasons.append("无法选择服务器")

        if not step_status.get("开始游戏", False):
            failure_reasons.append("无法开始游戏")

        if not failure_reasons:
            failure_reasons.append("未知原因")

        return failure_reasons

    for i_account in range(5):
        logger.debug("第{}次切换账号", i_account + 1)

        # 1. 点击可能存在的登录
        log_step("点击登录按钮", ImageService.touch(Onmyoji.login_DLAN, wait=3, rgb=True))
        if not step_status.get("点击登录按钮", False):
            failure_screenshots.append(AirtestService.snapshot())

        # 2. 检查可能存在的其他账号登录
        is_exception = ImageService.exists(Onmyoji.login_YCDL)
        if is_exception:
            log_step("处理异常登录", ImageService.touch(Onmyoji.comm_FH_YSJBDHSCH))
            if not step_status.get("处理异常登录", False):
                failure_screenshots.append(AirtestService.snapshot())

        # 3. 点击可能存在选服指引
        ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH)

        # 4. 点击左上角，防止有开场动画
        ImageService.touch_coordinate((10, 10))

        # 5. 点击可能存在同意并登录
        ImageService.touch(Onmyoji.login_TYBDL)

        # 6. 点击可能存在的右上角白底黑色叉号
        ImageService.touch(Onmyoji.comm_FH_YSJBDHSCH)

        # 7. 用户中心
        log_step("点击用户中心", ImageService.touch(Onmyoji.login_YHZX, timeouts=10))
        if not step_status.get("点击用户中心", False):
            failure_screenshots.append(AirtestService.snapshot())

        # 8. 切换账号
        log_step("切换账号", ImageService.touch(Onmyoji.login_QHZH, cvstrategy=Cvstrategy.default, wait=2))
        if not step_status.get("切换账号", False):
            failure_screenshots.append(AirtestService.snapshot())

        # 9. 常用
        log_step("选择常用账号", ImageService.touch(Onmyoji.login_CY, cvstrategy=Cvstrategy.default, wait=2))
        if not step_status.get("选择常用账号", False):
            failure_screenshots.append(AirtestService.snapshot())

        # 10. 选择账号
        account = str(os.path.join(Onmyoji.user_XZZH, game_account.account_name))
        logger.debug("选择账号拼接:{}", account)
        log_step("选择具体账号", ImageService.touch(account, wait=4))
        if not step_status.get("选择具体账号", False):
            failure_screenshots.append(AirtestService.snapshot())

        # 11. 登录,不能包括其他账号,开启ORC识别文字登录
        is_login_ocr = ImageService.touch(Onmyoji.login_DLAN, wait=4)
        if not is_login_ocr:
            for i_login_ocr in range(5):
                log_step("OCR识别登录", ImageService.ocr_touch(["登录"], ['其他']))
                if not step_status.get("OCR识别登录", False):
                    failure_screenshots.append(AirtestService.snapshot())
                is_login_ocr = ImageService.exists(Onmyoji.login_DLAN, wait=4, rgb=True)
                if not is_login_ocr:
                    break

        # 12. 接受协议
        log_step("接受协议", ImageService.touch(Onmyoji.login_JSXY, wait=3))
        if not step_status.get("接受协议", False):
            failure_screenshots.append(AirtestService.snapshot())

        # 13. 点击切换
        logger.debug("点击切换")
        log_step("切换服务器", switch())
        if not step_status.get("切换服务器", False):
            failure_screenshots.append(AirtestService.snapshot())

        # 14. 选择服务器
        logger.debug("选择服务器，直接点击角色名称:{}", game_account.role_region)
        log_step("选择服务器", ImageService.touch(account_login, wait=2))
        if not step_status.get("选择服务器", False):
            failure_screenshots.append(AirtestService.snapshot())

        # 15. 开始游戏
        if step_status.get("选择服务器", False):
            log_step("开始游戏", ImageService.touch(Onmyoji.login_KSYX, wait=2))
            if step_status.get("开始游戏", False):
                time.sleep(15)
                return True
            else:
                failure_screenshots.append(AirtestService.snapshot())

        # 第五次尝试失败，发送详细邮件
        if i_account + 1 == 5:
            # 最终截图
            final_screenshot = AirtestService.snapshot()
            failure_screenshots.append(final_screenshot)

            # 分析失败原因
            failure_reasons = analyze_login_failure(step_status)

            # 生成详细的步骤执行状态报告
            step_report = "登录步骤执行状态:\n"
            for step, status in step_status.items():
                step_report += f"  - {step}: {status}\n"

            failure_reason_str = "失败原因分析:\n"
            for reason in failure_reasons:
                failure_reason_str += f"  - {reason}\n"

            send_text = "账号：" + game_account.account_name + "\n\r\n\r" + step_report + "\n\r" + failure_reason_str

            logger.debug("第五次尝试登录失败,邮件发送")
            # 限制截图数量，避免邮件过大
            UtilsMail.send_email("阴阳师脚本", "登录失败5次", send_text, failure_screenshots[:5])

    return False


def quick_login():
    """快速登录"""
    logger.debug("开始游戏")
    is_login = ImageService.touch(Onmyoji.login_KSYX, wait=5)
    time.sleep(15)
    return is_login


def ensure_bottom_menu_open():
    """确保底部菜单打开"""
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
    return is_open_bottom


def create_project_log(game_project, game_account, game_devices, time_start, result):
    """创建项目日志"""
    time_end = time.time()
    time_all = time_end - time_start
    if time_all >= 60 * 5:
        logger.info("当前状态初始化，用时超5分钟，实际用时{}", UtilsTime.convert_seconds(time_all))
    return GameProjectLog(
        project_id=game_project.id,
        account_id=game_account.id,
        device_id=game_devices.id,
        result=result,
        cost_time=int(time_all)
    )


def switch():
    """切换服务器"""
    logger.debug("切换服务器，图片识别")
    # 尝试通过图片识别切换
    if ImageService.touch(Onmyoji.login_QHFWQ):
        if not ImageService.touch(Onmyoji.login_QHFWQ):
            return True

    # 尝试通过OCR识别切换
    logger.debug("切换服务器，图片文字ocr识别")
    if ImageService.ocr_touch(Switch.switch, similarly=0.8):
        return True

    # 尝试基于分辨率强制坐标
    logger.debug("切换服务器，基于分辨率强制坐标")
    is_start = ImageService.exists(Onmyoji.login_KSYX, wait=2)
    if is_start:
        ratio_x, ratio_y = AirtestService.resolution_ratio()
        if ratio_x == 1280 and ratio_y == 720:
            logger.debug("强制坐标")
            ImageService.touch_coordinate((640, 520))
            return True

    return False


def return_home(game_task: list):
    """返回游戏首页"""
    game_account = GameAccount(game_task[2])
    game_project = GameProject(game_task[3])

    # 拒绝协战
    logger.debug("返回首页-拒接协战")
    ComplexService.refuse_reward()

    # 首页返回
    logger.debug("首页返回")
    ImageService.exists(Onmyoji.comm_FH_SYFH)

    # 检查是否在首页
    if not is_on_account_homepage(str(os.path.join(Onmyoji.user_SYTX, str(game_account.account_num)))):
        logger.debug("不在账号首页，重新快速登录 {}:{}", game_account.role_name, game_project.project_name)
        ImageService.snapshot(game_account.role_name + '_' + game_project.project_name + "_非首页", True)
        return initialization(game_task, 1)
    else:
        logger.debug("有探索，有账号，在首页")
        return True
