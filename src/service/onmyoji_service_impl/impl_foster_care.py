"""
# @Time: 2023年08月31日01:34
# @Author: orcakill
# @File: impl_foster_care.py
# @Description: 式神寄养
"""
import time

from src.model.enum import Onmyoji
from src.model.models import GameAccount
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.onmyoji_service_impl import impl_return_home
from src.utils.my_logger import logger


def foster_care(game_task: []):
    """
    式神寄养
    :param game_task:
    :return:
    """
    # 寄养开始时间
    time_start = time.time()
    # 寄养轮次
    num_round = 0
    # 寄养检查好友
    num_friend = 0
    # 连续类型判断失败次数
    num_type_fail = 0
    # 寄养结果
    foster_result = None
    # 账号信息
    game_account = GameAccount(game_task[2])
    # 默认未找到目标
    is_target = False
    # 获取设备分辨率
    resolution = ImageService.resolving_power()
    logger.debug(game_account.game_name)
    logger.debug("式神寄养")
    for i_time in range(2):
        logger.debug("点击阴阳寮")
        ImageService.touch(Onmyoji.foster_YYLTB)
        logger.debug("点击结界")
        ImageService.touch(Onmyoji.foster_JJTB)
        logger.debug("点击式神育成")
        is_growing = ImageService.touch(Onmyoji.foster_SSYC)
        if not is_growing:
            logger.debug("式神育成点击失败，重新点击")
            ImageService.touch(Onmyoji.foster_SSYC)
        logger.debug("判断是否可寄养")
        is_foster = ImageService.exists(Onmyoji.foster_KJYBZ)
        if is_foster:
            logger.debug("可寄养")
            logger.debug("开始寄养，从六星太鼓到四星斗鱼")
            # 结界卡，默认六星太鼓
            target_type = Onmyoji.foster_JJK_TG
            target_card = Onmyoji.foster_JJK_LXTG
            for i_type in range(7):
                num_round = num_round + 1
                logger.debug("初始化目标结界卡")
                if i_type == 0:
                    target_type = Onmyoji.foster_JJK_TG
                    target_card = Onmyoji.foster_JJK_LXTG
                elif i_type == 1:
                    target_type = Onmyoji.foster_JJK_TG
                    target_card = Onmyoji.foster_JJK_WXTG
                elif i_type == 2:
                    target_type = Onmyoji.foster_JJK_TG
                    target_card = Onmyoji.foster_JJK_SXTG1
                elif i_type == 3:
                    target_type = Onmyoji.foster_JJK_TG
                    target_card = Onmyoji.foster_JJK_SXTG
                elif i_type == 4:
                    target_type = Onmyoji.foster_JJK_DY
                    target_card = Onmyoji.foster_JJK_LXDY
                elif i_type == 5:
                    target_type = Onmyoji.foster_JJK_DY
                    target_card = Onmyoji.foster_JJK_WXDY
                elif i_type == 6:
                    target_type = Onmyoji.foster_JJK_DY
                    target_card = Onmyoji.foster_JJK_SXDY1
                logger.debug("目标结界卡：{}", target_card)
                ImageService.touch(Onmyoji.foster_KJYBZ)
                logger.debug("确定上方好友坐标")
                coordinate_friend = ImageService.exists(Onmyoji.foster_SFHY)
                logger.debug("确定上方跨区坐标")
                coordinate_region = ImageService.exists(Onmyoji.foster_SFKQ)
                logger.debug("计算位置1,测试系数0.9")
                coordinate_difference = 0.9 * (coordinate_region[0] - coordinate_friend[0])
                coordinate_start = (coordinate_region[0], coordinate_region[1] + coordinate_difference)
                logger.debug("计算位置2")
                coordinate_end = (coordinate_region[0], coordinate_region[1] + 2 * coordinate_difference)
                if coordinate_start and coordinate_end and coordinate_end[1] - coordinate_start[1] > 0:
                    for i_friends in range(100):
                        num_friend = num_friend + 1
                        logger.debug("当前第{}个好友", i_friends + 1)
                        logger.debug("点击位置1")
                        ImageService.touch_coordinate(coordinate_start)
                        logger.debug("判断结界卡是否是目标类型:{}", target_type)
                        is_type = ImageService.exists(target_type)
                        if is_type:
                            logger.debug("判断结界卡是否是目标结界卡:{}", target_card)
                            is_target = ImageService.exists(target_card, threshold=0.8)
                            if is_target and is_target[0] > 1 / 2 * resolution[0]:
                                # sys.exit()
                                # 截图,记录识别结果
                                name = game_account.game_name
                                name = name + "_" + target_card.replace("阴阳寮\\式神寄养\\结界卡\\", "")
                                ImageService.snapshot(name, print_image=True)
                                foster_result = target_card
                                logger.debug("已找到目标结界卡,且X坐标在右侧,跳出一层循环,进入好友结界")
                                break
                        else:
                            num_type_fail = num_type_fail + 1
                        logger.debug("好友数大于10，且连续3次不是太鼓和斗鱼，判断是否是未放置")
                        if i_friends > 10 and num_type_fail % 3 == 0:
                            is_place = ImageService.exists(Onmyoji.foster_JJK_WFZ)
                            if is_place:
                                logger.debug("未放置,跳出一层循环，更换目标结界卡或结束寄养查找")
                                ComplexService.get_reward(Onmyoji.foster_SFHY)
                                break
                        else:
                            is_place = False
                        if not is_target and not is_place:
                            logger.debug("没找到目标，且当前不是未放置，向下滑动")
                            ImageService.swipe(coordinate_end, coordinate_start)
                if is_target and foster_result:
                    logger.debug("已找到目标结界卡,跳出二层循环")
                    break
            if is_target and foster_result:
                logger.debug("进入好友结界")
                ImageService.touch(Onmyoji.foster_JRJJ)
                logger.debug("点击达摩")
                is_dharma = ImageService.touch(Onmyoji.foster_DMDJDM)
                if not is_dharma:
                    is_dharma = ImageService.touch(Onmyoji.foster_DMFWDM)
                    if not is_dharma:
                        ImageService.touch(Onmyoji.foster_DMZFDM)
                logger.debug("确定")
                ImageService.touch(Onmyoji.foster_QD)
            logger.debug("返回首页")
            ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
            ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
            ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
            ImageService.touch(Onmyoji.comm_FH_ZSJHKZDHSXYH)
        else:
            logger.debug("返回首页")
            ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
            ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
            ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
            ImageService.touch(Onmyoji.comm_FH_ZSJHKZDHSXYH)
        logger.debug("确认返回首页")
        impl_return_home.return_home(game_task)
        time_end = time.time()
        time_time = round(time_end - time_start, 3)
        time_avg_friend = 0
        if num_friend > 0:
            time_avg_friend = round(time_time / num_friend)
        if is_foster:
            logger.debug("寄养用时{}秒,检查好友{}轮{}个，平均用时{}秒，寄养结果{}", time_time, num_round, num_friend,
                         time_avg_friend, foster_result)
        else:
            logger.debug("已寄养，无需寄养,用时{}秒", time_time)
