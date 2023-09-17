# @Time: 2023年09月11日 10:30
# @Author: orcakill
# @File: impl_explore.py
# @Description: 探索
import time

from src.model.enum import Onmyoji
from src.model.models import GameProjectsRelation
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.utils.my_logger import logger


def explore_chapters(game_task: [], chapter: int = 28):
    """
    章节探索
    默认选择28章困难
    自动添加候补式神
    全打 打3次，有小怪打小怪，有boss打boss，都没有左右移动，检查不到小怪和boss，退出探索
    :param chapter: 默认28章
    :param game_task:
    :return:
    """
    # 项目组项目关系
    game_projects_relation = GameProjectsRelation(game_task[1])
    # 开始时间
    time_start = time.time()
    # 战斗胜利次数
    num_win = 0
    # 战斗失败次数
    num_false = 0
    # 战斗用时列表
    time_fight_list = []
    # 章节首页
    chapter_home = None
    # 章节层数
    chapter_layers = None
    # 战斗次数
    fight_times = 20
    if game_projects_relation.project_num_times and game_projects_relation.project_num_times > 0:
        fight_times = game_projects_relation.project_num_times
    if chapter == 28:
        # 章节首页
        chapter_home = Onmyoji.explore_ZJSY_28
        # 章节层数
        chapter_layers = Onmyoji.explore_ZJ_28
    # 获取设备分辨率
    resolution = ImageService.resolution_ratio()
    logger.debug("章节探索-开始")
    for i in range(1, fight_times + 1):
        time_fight_start = time.time()
        logger.debug("判断是否是章节首页")
        is_home = ImageService.exists(chapter_home)
        if not is_home:
            ComplexService.refuse_reward()
            logger.debug("首页-判断是否有探索")
            is_explore = ImageService.exists(Onmyoji.home_TS)
            if is_explore:
                logger.debug("点击探索")
                ImageService.touch(Onmyoji.home_TS)
                logger.debug("选择章节")
                ImageService.touch(chapter_layers)
                logger.debug("选择困难")
                ImageService.touch(Onmyoji.explore_ZJNDKN)
            logger.debug("探索界面-判断是否是探索界面")
            is_explore = ImageService.exists(Onmyoji.soul_BQ_YHTB)
            if is_explore:
                logger.debug("探索界面，判断左侧宝箱")
                is_treasure_chest = ImageService.touch(Onmyoji.explore_ZCBX)
                if is_treasure_chest:
                    logger.debug("领取奖励")
                    ImageService.touch(Onmyoji.explore_TCTZ)
                logger.debug("选择章节")
                ImageService.touch(chapter_layers)
                logger.debug("选择困难")
                ImageService.touch(Onmyoji.explore_ZJNDKN)
        logger.debug("进入章节探索")
        ImageService.touch(Onmyoji.explore_ZJTS)
        if i == 1:
            logger.debug("第一次-锁定阵容")
            ImageService.touch(Onmyoji.explore_SDZR)
            logger.debug("第一次-自动轮换")
            ImageService.touch(Onmyoji.explore_ZDLH)
            logger.debug("判断是否锁定阵容")
            is_lock = ImageService.exists(Onmyoji.explore_JSZR)
            if is_lock:
                logger.debug("第一次-重新点击自动轮换")
                ImageService.touch(Onmyoji.explore_ZDLH)
        logger.debug("准备完成，开始战斗")
        # 默认无boss
        is_boss = False
        for i_fight in range(1, 10):
            logger.debug("第{}次探索战斗", i_fight)
            is_little_monster = ImageService.touch(Onmyoji.explore_XGZD)
            if not is_little_monster:
                logger.debug("没有小怪，点击首领")
                is_boss = ImageService.touch(Onmyoji.explore_SLZD)
                if not is_boss:
                    logger.debug("没有小怪，没有首领，右移")
                    ImageService.swipe((0.9 * resolution[0], 0.5 * resolution[1]),
                                       (0.5 * resolution[0], 0.5 * resolution[1]))
                    logger.debug("进入下一轮循环")
                    continue
            logger.debug("等待战斗结果")
            is_result = ComplexService.fight_end(Onmyoji.explore_ZDSL, Onmyoji.explore_ZDSB, Onmyoji.explore_ZCTZ,
                                                 Onmyoji.explore_TCTZ, Onmyoji.explore_XGZD, None, 30, 2)
            if is_result in [Onmyoji.explore_ZDSL, Onmyoji.explore_TCTZ]:
                num_win = num_win + 1
            elif is_result in [Onmyoji.explore_ZCTZ, Onmyoji.explore_ZDSB]:
                num_false = num_false + 1
            time_fight_end = time.time()
            time_fight = time_fight_end - time_fight_start
            logger.debug("本次探索-战斗结束，用时{}秒", round(time_fight, 3))
            time_fight_list.append(time_fight)
            if is_boss:
                break
        logger.debug("判断是否有奖励小纸人")
        is_reward = ImageService.exists(Onmyoji.explore_JLXZR)
        if is_reward:
            logger.debug("有小纸人，点击左上角返回")
            ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
            logger.debug("确认")
            ImageService.touch(Onmyoji.explore_QR)
        else:
            logger.debug("无小纸人")
    # 探索-战斗次数
    len_time_fight_list = len(time_fight_list)
    # 探索-战斗总用时
    time_fight_all = round(sum(time_fight_list))
    # 探索-结束时间
    time_end = time.time()
    # 探索-总用时
    time_all = time_end - time_start
    # 探索-平均战斗用时
    time_fight_avg = 0
    if len_time_fight_list > 0:
        time_fight_avg = round(sum(time_fight_list) / len(time_fight_list), 3)
    logger.debug("本次{}章探索挑战，共{}轮，总用时{}秒，战斗总用时{}秒,平均战斗用时{}秒，挑战{}次，胜利{}次，失败{}次",
                 chapter, fight_times, round(time_all, 3), time_fight_all, time_fight_avg,
                 len_time_fight_list, num_win, num_false)
