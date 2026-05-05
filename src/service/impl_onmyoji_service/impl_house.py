"""
# @Time: 2023年08月31日01:34
# @Author: orcakill
# @File: impl_house.py
# @Description: 式神寄养
"""
import concurrent.futures
import datetime
import time

from src.dao.mapper import Mapper
from src.model.enum import Onmyoji
from src.model.models import GameAccount, GameProjectLog, GameProjectsRelation, GameProject, GameDevice
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.impl_onmyoji_service import impl_initialization
from src.service.impl_onmyoji_service.impl_house_optimized import ImplHouseOptimized
from src.service.ocr_service import OcrService
from src.utils.my_logger import logger
from src.utils.utils_time import UtilsTime


def foster_care(game_task: list):
    """
    式神寄养
    :param game_task:
    :return:
    """
    # 寄养开始时间
    time_start = time.time()
    # 项目信息
    (game_projects_relation, game_account,
     game_project, game_devices) = (GameProjectsRelation(game_task[1]), GameAccount(game_task[2]),
                                    GameProject(game_task[3]), GameDevice(game_task[4]))
    # 寄养结果
    foster_result = None
    # 是否无寄养标志
    is_foster = False
    logger.debug("式神寄养")
    for i_time in range(3):
        for i_growing in range(3):
            logger.debug("点击阴阳寮图标")
            ImageService.touch(Onmyoji.foster_YYLTB)
            logger.debug("点击寮首页结界")
            ImageService.touch(Onmyoji.foster_JJTB, timeouts=10)
            logger.debug("点击结界-式神育成")
            is_growing = ImageService.touch(Onmyoji.foster_SSYC, wait=6, timeouts=10)
            if is_growing:
                break
            else:
                logger.debug("点击可能存在的返回，如枫树等级提升")
                ImageService.touch(Onmyoji.comm_FH_YSJZKHSLJSCH)
                ComplexService.refuse_reward()
        logger.debug("判断是否可寄养")
        is_foster = ImageService.exists(Onmyoji.foster_KJYBZ)
        if is_foster:
            logger.debug("寄养检查，按六星到三星太鼓，再到六星到三星太鼓")
            faster_place = ImplHouseOptimized.get_optimal_card()
            logger.debug(faster_place)
            if is_foster and faster_place:
                logger.debug("最优结界卡,进入好友结界")
                faster_name = game_account.role_name + faster_place.replace("阴阳寮\\式神寄养\\结界卡\\", '_')
                # 截图打印
                ImageService.snapshot(faster_name, True)
                logger.debug("进入好友结界")
                ImageService.touch(Onmyoji.foster_JRJJ)
                logger.debug("点击达摩,优先大吉达摩")
                is_dharma = ImageService.touch(Onmyoji.foster_DMDJDM)
                if not is_dharma:
                    is_dharma = ImageService.touch(Onmyoji.foster_DMFWDM)
                    if not is_dharma:
                        ImageService.touch(Onmyoji.foster_DMZFDM)
                logger.debug("确定")
                is_ture = ImageService.touch(Onmyoji.foster_QD)
                if is_ture:
                    foster_result = faster_place
            else:
                logger.debug("不可寄养或寄养结果为空")
        logger.debug("返回首页")
        ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
        ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
        ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
        ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
        ImageService.touch(Onmyoji.comm_FH_ZSJHKZDHSXYH)
        ImageService.touch(Onmyoji.comm_FH_ZSJHKZDHSXYH)
        logger.debug("确认返回首页")
    logger.debug("确认返回首页")
    impl_initialization.return_home(game_task)
    time_end = time.time()
    time_all = time_end - time_start
    # 记录项目执行结果
    game_project_log = GameProjectLog(project_id=game_project.id, account_id=game_account.id, device_id=game_devices.id,
                                      result='', cost_time=int(time_all))
    # 有寄养结果，无寄养标志则寄养成功
    if foster_result:
        game_project_log.result = foster_result
        logger.debug("寄养用时{},寄养结果{}", UtilsTime.convert_seconds(time_all), foster_result)
    elif not foster_result and not is_foster:
        game_project_log.result = '已寄养'
        logger.debug("已寄养，无需寄养,用时{}秒", UtilsTime.convert_seconds(time_all))
    elif is_foster:
        game_project_log.result = '寄养异常，未寄养成功'
    Mapper.save_game_project_log(game_project_log)


def get_card_type(target_type: str, not_placed: int = 0):
    """
    获取当前结界卡,判断当前结界卡类型和等级
    :return:
    """

    def check_image(image, threshold, rgb):
        if image:
            confidence = ImageService.exists(image, threshold=threshold, rgb=rgb)
            return confidence
        return 0

    def check_image_confidence(image, threshold, rgb):
        if image:
            confidence = ImageService.cv_match(image, threshold=threshold, rgb=rgb, x1=0.5)
            if confidence:
                return confidence['confidence']
        return 0

    card_types = [target_type]
    if not_placed == 1:
        card_types.append(Onmyoji.foster_JJK_WFZ)
    else:
        card_types.append("")

    # 太鼓和未放置
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(check_image, image_path, 0.7, False) for image_path in card_types]

    results = [future.result() for future in futures]

    if results[0]:
        logger.debug("当前有{}，判断星级", target_type)
        if target_type == Onmyoji.foster_JJK_TG:
            card_types = [Onmyoji.foster_JJK_LXTG, Onmyoji.foster_JJK_WXTG, Onmyoji.foster_JJK_SXTG1,
                          Onmyoji.foster_JJK_SXTG]
        else:
            card_types = [Onmyoji.foster_JJK_LXDY, Onmyoji.foster_JJK_WXDY, Onmyoji.foster_JJK_SXDY1,
                          '']

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(check_image_confidence, image_path, 0.8, True) for image_path in card_types]
        results = [future.result() for future in futures]
        max_value = max(results)
        results = [False if x != max_value else x for x in results]
        if results[0]:
            logger.debug("检查结果：{},相似度：{}", card_types[0], results[0])
            return card_types[0]
        elif results[1]:
            logger.debug("检查结果：{},相似度：{}", card_types[1], results[1])
            return card_types[1]
        elif results[2]:
            logger.debug("检查结果：{},相似度：{}", card_types[2], results[2])
            return card_types[2]
        elif results[3]:
            logger.debug("检查结果：{},相似度：{}", card_types[3], results[3])
            return card_types[3]
    elif results[1]:
        logger.debug("检查结果：{}", Onmyoji.foster_JJK_WFZ)
        return Onmyoji.foster_JJK_WFZ
    logger.debug("检查结果：其他情况")
    return None


def get_card_type_word(target_type: str, target_word, not_placed: int = 0):
    logger.debug("获取文字")
    result = OcrService.get_word(target_word)
    if result:
        if result in ['67', '76'] and target_type in [Onmyoji.foster_JJK_LXTG, Onmyoji.foster_JJK_WXTG]:
            logger.debug("检查结果：{}", target_type)
            return target_type
        if result in ['59', '67'] and target_type in [Onmyoji.foster_JJK_WXTG]:
            logger.debug("检查结果：{}", target_type)
            return target_type
        if result in ['50'] and target_type in [Onmyoji.foster_JJK_SXTG1]:
            logger.debug("检查结果：{}", target_type)
            return target_type
        if result in ['42', '50'] and target_type in [Onmyoji.foster_JJK_SXTG1, Onmyoji.foster_JJK_SXTG]:
            logger.debug("检查结果：{}", target_type)
            return target_type
    if not_placed == 1:
        is_placed = ImageService.exists(Onmyoji.foster_JJK_WFZ)
        if is_placed:
            logger.debug("检查结果：{}", Onmyoji.foster_JJK_WFZ)
            return Onmyoji.foster_JJK_WFZ
    logger.debug("检查结果：其他情况")
    return None


def get_card_left_type(target_card: str):
    """
    获取当前结界卡,直接判断左侧是否有目标结界卡
    :return:
    """

    def check_image_confidence(image, threshold, rgb):
        if image:
            if image == Onmyoji.foster_JJK_WFZ:
                result = ImageService.cv_match(image, threshold=threshold, rgb=rgb, x1=0.5)
            else:
                result = ImageService.cv_match(image, threshold=threshold, rgb=rgb, x2=0.5)
            return result
        return 0

    card_types = [target_card, Onmyoji.foster_JJK_WFZ]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(check_image_confidence, image_path, 0.6, False) for image_path in card_types]
    results = [future.result() for future in futures]
    if results[0]:
        logger.debug("检查结果：{},相似度：{}", target_card, results[0]['confidence'])
        return [target_card, results[0]['result'], results[0]['confidence']]
    elif results[1]:
        logger.debug("检查结果：{}", Onmyoji.foster_JJK_WFZ)
        return [Onmyoji.foster_JJK_WFZ, None, 0]
    logger.debug("检查结果：其他情况")
    return None


def shack_house(game_task: list):
    """
    寮管理
    1.寮资金纸人
    2.寮体力纸人
    3.集体任务
    4.体力食盒和经验酒壶
    5.结界卡奖励领取
    6.寄养奖励领取
    7.结界卡放置
    8.式神育成
    :param game_task: 任务信息
    :return:
    """
    # 寮管理开始时间
    time_start = time.time()
    # 获取当前日期
    today = datetime.date.today()
    # 获取本日是周几（周一为0，周日为6）
    weekday = today.weekday() + 1
    # 项目信息
    (game_projects_relation, game_account,
     game_project, game_devices) = (GameProjectsRelation(game_task[1]), GameAccount(game_task[2]),
                                    GameProject(game_task[3]), GameDevice(game_task[4]))
    logger.debug("进入阴阳寮")
    ImageService.touch(Onmyoji.shack_YYLTB)
    ImageService.touch(Onmyoji.shack_YCFH)
    logger.debug("1.寮资金纸人")
    is_capital = ImageService.touch(Onmyoji.shack_ZJLQ)
    if is_capital:
        logger.debug("领取按钮")
        ImageService.touch(Onmyoji.shack_LQAN)
        logger.debug("获得奖励")
        ComplexService.get_reward(Onmyoji.shack_HDJL)
    logger.debug("2.寮体力纸人")
    is_strength = ImageService.touch(Onmyoji.shack_TLXZR)
    if is_strength:
        logger.debug("获得奖励")
        ComplexService.get_reward(Onmyoji.shack_HDJL)
    logger.debug("3.集体任务")
    is_collective = ImageService.touch(Onmyoji.shack_ZCJTRW)
    if is_collective:
        logger.debug("集体任务，判断是否有觉醒任务")
        is_awaken = ImageService.exists(Onmyoji.shack_JXRW)
        if is_awaken:
            logger.debug("集体任务，判断是否提交")
            is_commit = ImageService.exists(Onmyoji.shack_TJ)
            if is_awaken and is_commit:
                coordinate_commit = (is_awaken[0], is_commit[1])
                logger.debug("确定有觉醒任务和提交,{}", coordinate_commit)
                ImageService.touch_coordinate(coordinate_commit)
                logger.debug("四种觉醒材料的坐标")
                is_fire = ImageService.exists(Onmyoji.shack_RWCLYHL)
                is_mine = ImageService.exists(Onmyoji.shack_RWCLTLG)
                is_water = ImageService.exists(Onmyoji.shack_RWCLSLL)
                is_wind = ImageService.exists(Onmyoji.shack_RWCLFZF)
                logger.debug("任务滚轮坐标")
                is_roller = ImageService.exists(Onmyoji.shack_RWGL)
                logger.debug("任务加号坐标")
                is_plus = ImageService.exists(Onmyoji.shack_RWJH)
                logger.debug("滑动四个滚轮，加满材料")
                if is_mine and is_roller and is_plus and weekday in [4, 5, 6, 7]:
                    logger.debug("天雷鼓")
                    v1 = (is_roller[0], is_mine[1])
                    v2 = (is_plus[0], is_mine[1])
                    ImageService.swipe(v1, v2)
                if is_fire and is_roller and is_plus and weekday == 1:
                    logger.debug("业火轮")
                    v1 = (is_roller[0], is_fire[1])
                    v2 = (is_plus[0], is_fire[1])
                    ImageService.swipe(v1, v2)
                if is_water and is_roller and is_plus and weekday == 2:
                    logger.debug("水灵鲤")
                    v1 = (is_roller[0], is_water[1])
                    v2 = (is_plus[0], is_water[1])
                    ImageService.swipe(v1, v2)
                if is_wind and is_roller and is_plus and weekday == 3:
                    logger.debug("风转符")
                    v1 = (is_roller[0], is_wind[1])
                    v2 = (is_plus[0], is_wind[1])
                    ImageService.swipe(v1, v2)
                logger.debug("判断是否获取到所需全部坐标")
                if is_roller and is_plus and is_mine and is_fire and is_water and is_wind:
                    logger.debug("提交")
                    ImageService.touch(Onmyoji.shack_TJCL)
                    logger.debug("获取奖励，2次")
                    ComplexService.get_reward(Onmyoji.shack_HDJL)
                    ComplexService.get_reward(Onmyoji.shack_HDJL)
                else:
                    logger.debug("全部坐标获取失败，尝试返回首页")
                    ComplexService.get_reward(is_fire)
                    ImageService.touch_coordinate((10, 10))
                    logger.debug("返回到寮首页")
                    ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH)
        logger.debug("返回到寮首页")
        ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH)
        logger.debug("返回到首页")
        ImageService.touch(Onmyoji.comm_FH_ZSJHKZDHSXYH)
        logger.debug("确认返回首页")
        impl_initialization.return_home(game_task)
    logger.debug("返回到首页")
    ImageService.touch(Onmyoji.comm_FH_ZSJHKZDHSXYH)
    logger.debug("确认返回首页")
    impl_initialization.return_home(game_task)
    logger.debug("4.体力食盒和经验酒壶")
    is_border = ImageService.touch(Onmyoji.shack_YYLTB)
    if is_border:
        logger.debug("进入结界")
        ImageService.touch(Onmyoji.shack_JJTB)
        ImageService.touch(Onmyoji.shack_YCFH)
        logger.debug("判断是否有体力待领取")
        is_food_box = ImageService.touch(Onmyoji.shack_TLSH)
        if is_food_box:
            logger.debug("领取体力")
            ImageService.touch(Onmyoji.shack_QCTL)
            logger.debug("获得奖励")
            ComplexService.get_reward(Onmyoji.shack_HDJL)
            logger.debug("点击可能存在的返回")
            ImageService.touch(Onmyoji.comm_FH_YSJZDHBSCH, rgb=True)
        logger.debug("判断是否有经验待领取")
        is_wine_pot = ImageService.touch(Onmyoji.shack_JYJH)
        if is_wine_pot:
            logger.debug("领取经验")
            ImageService.touch(Onmyoji.shack_TQJY)
            logger.debug("点击可能存在的确定")
            ImageService.touch(Onmyoji.shack_QD)
            logger.debug("点击可能存在的返回")
            ImageService.touch(Onmyoji.comm_FH_YSJZDHBSCH, rgb=True)
    logger.debug("5.结界卡奖励领取")
    is_card_rewards = ImageService.touch(Onmyoji.shack_JJKJLLQ)
    if is_card_rewards and game_account.account_name not in [1, '1']:
        logger.debug("小号获得奖励")
        ComplexService.get_reward(Onmyoji.shack_HDJL)
    logger.debug("6.寄养奖励领取")
    is_faster_rewards = ImageService.touch(Onmyoji.shack_JYJLLQ)
    if is_faster_rewards:
        logger.debug("获得奖励")
        ComplexService.get_reward(Onmyoji.shack_HDJL)
    logger.debug("7.结界卡放置")
    is_border_card = ImageService.touch(Onmyoji.shack_JJK, timeouts=10)
    if is_border_card:
        logger.debug("判断是否无结界卡")
        is_border_card = ImageService.touch(Onmyoji.shack_JJKDQ)
        if is_border_card:
            logger.debug("点击全部")
            ImageService.touch(Onmyoji.shack_JJKQBXL)
            logger.debug("点击下拉太鼓")
            ImageService.touch(Onmyoji.shack_XLTG)
            logger.debug("点击太鼓")
            is_place = ImageService.touch(Onmyoji.shack_TG)
            if is_place:
                logger.debug("激活")
                ImageService.touch(Onmyoji.shack_JH)
                logger.debug("确定")
                ImageService.touch(Onmyoji.shack_JHQD)
                logger.debug("返回")
                ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH)
            else:
                logger.debug("点击全部")
                ImageService.touch(Onmyoji.shack_JJKQBXL)
                logger.debug("点击下拉斗鱼")
                ImageService.touch(Onmyoji.shack_XLDY)
                logger.debug("点击斗鱼")
                is_place = ImageService.touch(Onmyoji.shack_DY)
                if is_place:
                    logger.debug("激活")
                    ImageService.touch(Onmyoji.shack_JH)
                    logger.debug("返回")
                    ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH)
                else:
                    logger.debug("点击全部")
                    ImageService.touch(Onmyoji.shack_JJKQBXL)
                    logger.debug("点击下拉太阴")
                    ImageService.touch(Onmyoji.shack_XLTY)
                    logger.debug("点击太阴")
                    ImageService.touch(Onmyoji.shack_TY)
                    logger.debug("返回")
                    ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH)
        else:
            logger.debug("已有结界卡，返回")
            ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH)
    logger.debug("8.式神育成")
    is_care = ImageService.touch(Onmyoji.shack_SSYC)
    if is_care:
        logger.debug("判断是否有满")
        is_full = ImageService.exists(Onmyoji.shack_MZ)
        if is_full:
            for i_full in range(8):
                logger.debug("点击满字，去掉已满的式神")
                is_full = ImageService.touch(Onmyoji.shack_MZ)
                if not is_full:
                    logger.debug("已无经验已满的式神")
                    break
        logger.debug("判断是否有放入式神")
        is_insert = ImageService.exists(Onmyoji.shack_FRSS)
        if is_insert:
            logger.debug("点击左下的全部")
            ImageService.touch(Onmyoji.shack_ZXQB)
            logger.debug("点击左下的素材")
            ImageService.touch(Onmyoji.shack_XZSC)
            logger.debug("判断有无红蛋，无红蛋则放弃")
            is_growing = ImageService.exists(Onmyoji.shack_HD)
            if is_growing:
                logger.debug("点击红蛋，6次")
                for i_growing in range(8):
                    logger.debug("点击1级素材")
                    ImageService.touch_coordinate(is_growing)
            else:
                logger.debug("没找红蛋")
    logger.debug("返回首页")
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    ImageService.touch(Onmyoji.comm_FH_ZSJHKZDHSXYH)
    logger.debug("确认返回首页")
    impl_initialization.return_home(game_task)
    time_end = time.time()
    time_all = time_end - time_start
    # 记录项目执行结果
    game_project_log = GameProjectLog(project_id=game_project.id, account_id=game_account.id, device_id=game_devices.id,
                                      result='阴阳寮管理', cost_time=int(time_all))
    Mapper.save_game_project_log(game_project_log)
    logger.debug("本次寮管理，用时{}秒", UtilsTime.convert_seconds(time_all))
