# @Time: 2023年09月11日 10:30
# @Author: orcakill
# @File: impl_explore.py
# @Description: 探索
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
    resolution = ImageService.resolving_power()
    logger.debug("章节探索-开始")
    for i in range(1, fight_times + 1):
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
        for i_fight in range(1, 10):
            logger.debug("第{}次点击小怪", i_fight)
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
                ComplexService.fight_end(Onmyoji.explore_ZDSL, Onmyoji.explore_ZDSB, Onmyoji.explore_ZCTZ,
                                         Onmyoji.explore_TCTZ, Onmyoji.explore_XGZD, None, 30, 2)
                logger.debug("退出循环")
                break
            logger.debug("等待战斗结果")
            ComplexService.fight_end(Onmyoji.explore_ZDSL, Onmyoji.explore_ZDSB, Onmyoji.explore_ZCTZ,
                                     Onmyoji.explore_TCTZ,
                                     Onmyoji.explore_XGZD, None, 30, 2)
        logger.debug("判断是否有奖励小纸人")
        is_reward = ImageService.exists(Onmyoji.explore_JLXZR)
        if is_reward:
            logger.debug("有小纸人，点击左上角返回")
            ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
            logger.debug("确认")
            ImageService.touch(Onmyoji.explore_QR)
        else:
            logger.debug("无小纸人")
